# Model part 
# clean model part 
# 
#
import numpy as np 
# import rAkmean as akm 
import cPickle as pickle
import time
#####################
# parameters 
#	dat, is the data - a dictionary of the compressed time series occ 
# 	thers, is the preportion the seperate training & testing data  
#   
def runAnalysis(dat, thres=0.1):
	dvec = reshaping(dat)
	numTest = len(dvec)*thres;
	TrainData = dvec[:(len(dvec)-numTest)];
	TestData = dvec[(len(dvec)-numTest):];
	order = None;
	try:
		import rSARIMA 
		order = rSARIMA.runIdentifyModel(TrainData)
	except:
		raise NotImplementedError("call R SARIMA program <runIdentifyModel()> error...")
		pass	

	return 	order;


def runAnalysisV2(dat, thres=0.1):

	print "before call identify model arma "
	dvec = dat;
	numTest = len(dvec)*thres;
	print len(dvec), numTest
	TrainData = dvec[:(len(dvec)-numTest)]
	TestData = dvec[len(dvec)-numTest]
	order = None;
	print "seperate training data "
	# time.sleep(5)
	try:
		import rSARIMA
		order = rSARIMA.runIdentifyModel(TrainData) 
	except:
		raise NotImplementedError("call R SARIMA program <runIdentifyModel() function--runAnalysisV2> ")	
		pass
	return order	

def runTSAprediction(dat, thres=0.1):
	print ">>inside time series<<"
	dvec = reshaping(dat)
	numTest = int(np.floor(len(dvec)*thres));
	print ">>inside time series after <<"
	# TrainData = dvec[:(len(dvec)-numTest)];
	# TestData = dvec[(len(dvec)-numTest):];
	if numTest == 0:
		raise ValueError("TestData is empty...")	

	print "run TSA prediction"
	# print len(TrainData)

	try: 
		import rSARIMA
		# rSARIMA.runForecast(TrainData, 2,1,1,0,0,0)
		# 
		# predictV = rSARIMA.runForecast(TrainData, 2,1,1,0,0,0)
		truncateBound = len(dvec)-numTest;
		predVector = []
		print numTest

		for i in range(24):		#range(numTest):
			TrainData = dvec[:(truncateBound+i)];

			predictVal = rSARIMA.runForecast(TrainData, 1,0,0,0,0,0, "iter "+str(i) )   #2,0,1,1,1,0  / 3,0,2,1,1,0 
			predVector.append(predictVal)
			
		predVector = np.array(predVector)
		# TestData = dvec[truncateBound:]
		TestData = dvec[truncateBound:truncateBound+24]
		print len(predVector), len(TestData)
		# print "show: ",(predictV, TestData[0], dvec[(len(dvec)-numTest)], TrainData[-1])
		
		######################
		# calculate the error
		######################
		errVector = np.subtract(predVector, TestData)
		errRatioV = abs(errVector/TestData)
		
		print np.mean(errRatioV)

		MAPE = np.mean(errRatioV)
		######################
		# plot the prediction 
		######################
		# import matplotlib.pyplot as plt
		# #
		# plt.figure()
		# plt.plot(np.arange(len(predVector)), predVector);
		# plt.plot(np.arange(len(TestData)), TestData )
		# plt.show()

		return MAPE

	except:
		raise ValueError("call function in R <runForecast> ... error")	
		pass


# here the dat is a vector 
def runTSApredictionV2(dat, thres=0.1):

	dvec = dat
	numTest = int(np.floor(len(dvec)*thres));

	if numTest == 0:
		raise ValueError("TestData is empty...")

	truncateBound = len(dvec)-numTest;	
	predVector=[]
	print "inside version 2 of ts prediction"
	try:
		import rSARIMA
		for i in range(24):		
			TrainData = dvec[:(truncateBound+i)];
			# predictVal = rSARIMA.runARIMA(TrainData, 1,0,0, "iter "+str(i) )
			predictVal = rSARIMA.runForecast(TrainData, 2,0,2,1,0,0, "iter "+str(i) ) 
			predVector.append(predictVal)
			
		predVector = np.array(predVector)
		# TestData = dvec[truncateBound:]
		TestData = dvec[truncateBound:truncateBound+24]
		# print len(predVector), len(TestData)	

		######################
		# calculate the error
		######################
		errVector = np.subtract(predVector, TestData)
		# print errVector, TestData
		# time.sleep(1)

		for j in xrange(len(TestData)):
			print "check", j 
			if TestData[j] < 0.0001 and TestData[j]> -0.0001:
				print "condition success"
				TestData[j] = 1;

		# print "modify test data: " , TestData		
		errRatioV = abs(errVector/TestData)
		
		print np.mean(errRatioV)

		MAPE = np.mean(errRatioV)
		# time.sleep(6)
		return MAPE
	except:
		pass 	


def runClassification(dat):
	datVector = reshaping(dat)
	# print "shape of the reformated data vector...",datVector.shape
	# akm.runAkmean(datVector)
	########################
	# use - customized k-mean
	length = datVector.shape[0]
	if isinstance(length/24, int):	
		datMatrix = datVector.reshape(length/24, 24)

		############### 
		# normalize the matrix  
		##############
		# 
		# 
		sumVector = np.sum(datMatrix, axis =1)
		x = datMatrix;
		for j in range(datMatrix.shape[0]):
			x[j,:] = datMatrix[j,:]/sumVector[j]

		datMatrix = x	

		#############
		# call run kmean 
		# - input a numpy matrix with each row is the observation
		runKmean(datMatrix)

	else:
		raise ValueError("length is not a integer")	


#################
#%%%%%% internal call %%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%
# run k-mean 
#################
def runKmean(patchs):
	# print patchs.shape
	try:
		from scipy.cluster.vq import kmeans,vq, kmeans2
		from scipy.spatial.distance import cdist,pdist
		# setup the k-mean range 
		K_MAX = 30
		KK = range(1,K_MAX+1)
		KM = [kmeans(patchs,k, thresh=0.15) for k in KK]
		centroids = [cent for (cent,var) in KM]

		D_k = [cdist(patchs, cent, 'euclidean') for cent in centroids]
		cIdx = [np.argmin(D,axis=1) for D in D_k]
		dist = [np.min(D,axis=1) for D in D_k]

		tot_withinss = [sum(d**2) for d in dist]  # Total within-cluster sum of squares
		totss = sum(pdist(patchs)**2)/patchs.shape[0]       # The total sum of squares
		betweenss = totss - tot_withinss   


		##### plots #####
		import matplotlib.pyplot as plt
		from matplotlib import cm

		###### plot the elbow curve #########
		kIdx = 5        # K=6
		clr = cm.spectral( np.linspace(0,1,10) ).tolist()
		mrk = 'os^p<dvh8>+x.'
		
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.plot(KK, betweenss/totss*100, 'b*-')
		ax.plot(KK[kIdx], betweenss[kIdx]/totss*100, marker='o', markersize=12, 
			markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
		ax.set_ylim((0,100))
		plt.grid(True)
		plt.xlabel('Number of clusters')
		plt.ylabel('Percentage of variance explained (%)')
		plt.title('Elbow for KMeans clustering')

		# plt.show()
		####### plot data #########
		fig = plt.figure()
		# ax = fig.add_subplot(121)
		# for i in range(10):
		# 	# ind = (t==i)
		# 	# ax.scatter(X[ind,0],X[ind,1], s=35, c=clr[i], marker=mrk[i], label='%d'%i)
		# 	plt.legend()
		# 	plt.title('Actual Daily Pattern')
		
		############################
		# add labled centroid 
		############################
		idxLabels, _ = vq(patchs, centroids[5])

		# print "show...\n", patchs[idxLabels==0];

		# for i in range()


		# ax = fig.add_subplot(111);
		#####
		# plot the raw data 
		# 
		#####
		# for p in range(patchs.shape[0]):
			# ax.plot(np.linspace(0, 23, 24), patchs[p,:], '--')

			
		#######
		# plot each cluster shape with centroid 
		#######
		colorSetlabel = ['r--','b--','g--','c--','m--','b-.']
		
		for i in range(kIdx+1):
			# ind = (cIdx[kIdx]==i)
			# ax.scatter(X[ind,0],X[ind,1], s=35, c=clr[i], marker=mrk[i], label='C%d'%i)
			# figDim = 2*100 + 3*10+kIdx+1
			ax = fig.add_subplot(2,3,i+1)
			for j in xrange(patchs[idxLabels==i].shape[0]): 
				ax.plot(np.linspace(0, 23, 24),patchs[idxLabels==i][j,:], colorSetlabel[i])

			ax.plot(np.linspace(0, 23, 24),centroids[kIdx][i,:],'k',linewidth=6.5)
			ax.set_title('cluster %d '%(i+1))
		# plt.legend()
		# plt.title('K=%d clusters'%KK[kIdx])
			
		plt.tight_layout()

		###########
		# plot histogram 
		###########
		fig2, ax2= plt.subplots()
		hist, bin_edge = np.histogram(idxLabels)
		# plt.bar(idxLabels)
		reform_hist =[]
		for countval in hist:
			if countval >= 1:
				reform_hist.append(countval)

		print reform_hist, "\n", bin_edge
		bar_width = 0.5
		bar_x_labels = np.arange(kIdx+1);
		ax2.bar([i for i in range(kIdx+1)], reform_hist, bar_width)
		ax2.set_xticks(bar_x_labels+bar_width/2) 
		ax2.set_xticklabels([i+1 for i in range(kIdx+1)])
		plt.show()




		#################
		#

		#################
		#######
		# centroids,_ = kmeans2(patchs,4);
		# print "what:\n", _
		# idx,_ = vq(patchs,centroids)
		# print "vq 2nd arg...\n",_
		#################
		# tuning the k parameters
		#################
		#vq(patchs, centroids)


		# print centroids
		# print centroids.shape



		# plt.figure()
		# for i in range(centroids.shape[0]):
		# 	plt.plot(np.linspace(0, 23, 24), centroids[i,:],'-', linewidth=2)
		# plt.show()
	except ValueError:
		pass


############

####################
# run svm regression
#   - this function call svmUitl
# 	   to run the svm Prediction	
####################
def runSVMprediction(dat, thres=0.1):
	dvec = reshaping(dat)

	print "::::in svm prediction::::", len(dvec)

	numTest = int(np.floor(len(dvec)*thres));

	# TrainData = dvec[:(len(dvec)-numTest)];
	# TestData = dvec[(len(dvec)-numTest):];
	if numTest == 0:
		raise ValueError("TestData is empty...")	

	print "run SVM prediction"
	# print len(TrainData)

	try: 
		import svmUtil 
		# errVector = [];

		# print "show ->->->";
		truncateBound = len(dvec)-numTest;
		# for i in range(5):
		TrainData = dvec[:truncateBound];
		TestData = dvec[truncateBound:truncateBound+numTest]
		errTrain, errTest = svmUtil.svrLearn(TrainData,TestData)
		# if isinstance(err, (int, float,long)):
		# errVector.append(err)
		# print err  
		# raise ValueError("DEBUG >>>>>>>>>.break point");		
		# MAPE = np.mean(np.array(errVector));		
		# return MAPE
		print "training error:", errTrain, " ; testing error: ", errTest
		# return errTrain
		return errTest
	except: 	
		print "...excption in svm learning "; 
		# pass

	# raise NotImplementedError("SVM model error")	

##############
# run nerual networks 
# 	- call ffnetUtil module 
#
##############
def runFFNNprediction(dat, thres=0.1):
	print "inside Feed Forward Neural Nets";

	print "input data shape"
	time.sleep(5)
	dvec = reshaping(dat); 
	print "::::in FFNN prediction::::", len(dvec)

	numTest = int(np.floor(len(dvec)*thres));

	try:
		import ffnetUtil 
		truncateBound = len(dvec) - numTest
		print "****************", truncateBound
		TrainData = dvec[:truncateBound];
		TestData = dvec[truncateBound:truncateBound+numTest];

		print "before real call>>>>>"
		time.sleep(2)
		print "test data...",len(TestData)
		trainErr, testErr = ffnetUtil.nnLearn(TrainData, TestData)

		# return trainErr
		return testErr
	except:	
		time.sleep(3)
		raise NotImplementedError("Neural Net Work is Failed")

#################

################
# run simple average alg
# 
################
#
def runAVGprediction(dat, thres=0.1):
	dvec = reshaping(dat);
	print "::in average predictor::";
	numTest = int(np.floor(len(dvec)*thres));
	truncateBound = len(dvec) - numTest;
	print ">>> truncate bound>>>",truncateBound
	print dvec.shape
	#################################
	####### plot out the series######
	try:
		import matplotlib.pyplot as plt 



		plt.figure();



		for i in range(24):
			for j in range(12,7,-1):
				x = dvec[len(dvec)-24*j:len(dvec)-24*(j-1)]
				
		# plt.plot(dvec);
		plt.show();

	except:
		raise NotImplementedError("figure plot in average prediction wrong");


	# truncate bound 
	



	try:
		errVector = []
		for i in xrange(truncateBound, truncateBound-240, -1):
			s = 0
			for j in range(1,6):	# previous 5 days 
				# print dvec[i-j*24]
				s += dvec[i-j*24];
				# print s 
			predVal=s/5.0	
			err = abs(predVal - dvec[i])/dvec[i] ;
			errVector.append(err);
		



		return np.mean(np.array(errVector))	
	except:
		raise NotImplementedError("****simple average predictor****")

#################
# 
# pass in dat 2D array
################# 
def runPCAonDays(dat,start,end):
	print "in pca :::"
	i = 0;
	time.sleep(2)
	dayMatrix = None;
	daysLabel = [];
	nextDay = None;
	
	for k, v in dat.items():
		i+=1
		# print k, v;
		if i < start:
			continue

		if i >= end: 
			nextDay = (k[0],v[0]);
			break;		
		print k, v;
		if dayMatrix is None:
			dayMatrix = v[0];
		else:
			dayMatrix = np.vstack((dayMatrix, v[0]));

		daysLabel.append(k[0])	

	# print dayMatrix.shape
	print dayMatrix
	try: 
		from sklearn.decomposition import PCA 
		data = np.transpose(dayMatrix)
		print data.shape
		pca = PCA(n_components=(end-start))
		pca.fit(data)
		print(pca.explained_variance_ratio_)

		import matplotlib.pyplot as plt
		ind = np.arange(end-start)
		width = 0.55		
		xDisplay = [i+1 for i,v in enumerate(daysLabel)] 

		plt.figure()
		plt.bar(ind, pca.explained_variance_ratio_, width)
		plt.xticks(ind+width/2, xDisplay, fontsize=16 )
		plt.yticks(fontsize=16)
		plt.show()


	except:	
		pass


	raise NotImplementedError("break");

#################
# calculate previous value average based on lags number 
#################

def deTranding(datVector, i, t=24, lags=5):
	# print len(datVector);
	# i = len(datVector);
	# print "data point detranding ----";
	# print datVector.shape
	# print datVector[100]

	TIME_GAP =t;
	j = 1;
	ptiltArr = []   

	# print "inside the detranding ::: ";

	while True :
		# print "index in vector ",i-TIME_GAP*j 
		
		if i-TIME_GAP*j < 0 :
			break

		if j > lags:
			break

		val = datVector[i-TIME_GAP*j] 
		ptiltArr.append(val)
		j = j+1


	# print "length of the array:", len(ptiltArr);
		
	ptiltArr = np.array(ptiltArr)	

	ptilt = np.mean(ptiltArr)
	# print ptilt
	return ptilt


def deTrandingV2(datVector, i, t1, t2=24, lags=5):
	TIME_GAP =t2;
	j = 1;
	ptiltArr = [] 
	if i-t1 > 0:
		ptiltArr.append(datVector[i-t1])  
	else: 
		raise ValueError("index out of bounds")	

	while True :
		# print "index in vector ",i-TIME_GAP*j 	
		if i-TIME_GAP*j < 0 :
			break

		if j > lags:
			break

		val = datVector[i-TIME_GAP*j] 
		ptiltArr.append(val)
		j = j+1
	ptiltArr = np.array(ptiltArr)	

	ptilt = np.mean(ptiltArr)
	# print ptilt
	return ptilt





#################
# reshape the data (dictionary)
#################
 
def reshaping(data):	
	print ":::inside the reshaping:::";
	vals = None;
	for k, v in data.items():
		# print k, v
		# time.sleep(2)
		if np.ndarray.min(v) <= 0.05:
			print v 
			continue

		if vals is None:
			vals = v 	
		else:
			vals = np.append(vals, v)

	# print vols 	
	return vals 


###############
# write to pickle file
###############
# data: any data 
# desc: key word description
# fpath: default fpath is point to /interim/ folder
def outputPicklefile(data, desc, fpath=None):
	# try:
	# 	import cPickle as pickle
	# except:
	# 	import pickle 	 

	print "dump in the content", type(desc) 
	if fpath is None:
		fp = open('../regression/interim/'+desc+'occ2.p', 'wb')
		pickle.dump(data, fp)
	else:
		fp = open(fpath, 'wb')
		pickle.dump(data, fp)

	print "output pickle file finished"



#####################
# Ordinary Least Squre 
#####################
# import package 
#####################
from datetime import datetime
import pandas as pd 
####################
# stats model 
import statsmodels.formula.api as smf 
####################
import statsmodels.api as sm

def runOLSregression(dat):
	print ":: inside the reconstruction ::"
	vals = None	# occupancy values 
	catHvals = None # categorical hour index 
	catWeekday = None # categorical day index 

	for k, v in dat.items():
		weekday = identifyDayOfWeek(k)		
		cateHour = np.linspace(0,23,24)  # categorical data 
		# print np.ones(24)*weekday
		# print v 
		# print cateHour
		if np.ndarray.min(v) <= 0.05: 
			continue

		if vals is None:
			vals = v
			catHvals = cateHour
			catWeekday = np.ones(24)*weekday			
		else:
			vals = np.append(vals, v)		
			catHvals = np.append(catHvals, cateHour)
			catWday = np.ones(24)*weekday;
			catWeekday = np.append(catWeekday, catWday)

	# X = np.c_[v[0], cateHour, np.ones(24)*weekday];
	y_true = vals[1:]
	X = np.c_[y_true, vals[:-1], catHvals[1:], catWeekday[1:]]
	# y_true = vals[1:]
	# print len(X[:,0]), len(X[:,1]), len(X[:,2])
	print X.shape
	dframe = pd.DataFrame({ 'y_true': X[:,0], 'preHour': X[:,1], 'HourIdx': X[:,2], 'weekOfday': X[:,3]})
	# print dframe.preHour

	result = smf.ols(formula='y_true ~ preHour + C(HourIdx) + C(weekOfday)', data=dframe).fit() 

	# print result.params.T
	beta = result.params.T 
	print "shape of beta", beta.shape
	try:
		nsample = X.shape[0]
	except:
		nsample = len(X)	 
	hIdx = np.array(X[:,2])	
	# print hIdx
	dummy = (hIdx[:,None] == np.unique(hIdx)).astype(float)
	wdayIdx = np.array(X[:,3])  
	dummy2 = (wdayIdx[:, None] == np.unique(wdayIdx)).astype(float)
	# print dummy, dummy2

	# X_test = [np.,  ]
	XX = np.c_[np.ones(nsample), dummy[:,1:], dummy2[:,1:], vals[:-1]]
	# print XX.shape
	vec = XX.dot(beta)
	# print vec

	s = 24*30+6
	t = 26*30+20 
	errRvals = abs(np.subtract(y_true[s:t], vec[s:t])/y_true[s:t])  
	print np.mean(errRvals)
	err = np.mean(errRvals)
	# print (result.summary())
	# print XX.shape
	
	# plt.figure()
	# plt.plot(y_true[s:t])
	# plt.plot(vec[s:t])
	# plt.show()
	return err 

def identifyDayOfWeek(dictkey):
	datekey, sumVal, idx = dictkey 
	y = int(datekey[:4])
	m = int(datekey[4:6])
	d = int(datekey[6:])

	# print y, m, d 
	# notice that 
	weekday = datetime(y, m, d).weekday()

	return weekday+1












#################
# reconstruct the data by detrending 
# - using indicate function  
#################

# def deTrendingIndicate(data):
#	# print ":::inside the indicate detrending:::"
	
#	# with open('../interim/')
#	# print data 



