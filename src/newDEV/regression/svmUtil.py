### this script utilize the svm ###
# 
# For this particular case 
# 
from sklearn.svm import SVR 
import numpy as np 
import time

def svrLearn(v, vTest):
	# print v
	# raise NotImplementedError("???")
	print "inside...svm learning"
	# time.sleep(2)
	#############################
	########## training #########
	dataframe = None  
	for i in xrange(48, len(v)):
		_r = []
		for j in xrange(1,24):
			# _r.append(v[i-j][0])
			_r.append(v[i-j])
		# _r.append(v[i][0])
		_r.append(v[i])
		#print _r 
		if dataframe is None: 
			dataframe = np.array(_r);
		else:
			dataframe = np.vstack((dataframe, np.array(_r) ))

	#print dataframe.shape			 
	#
	inputTrain = dataframe[:,:24]
	#print inputTrain
	targetVals = dataframe[:,-1]

	# clf = SVR(kernel='sigmoid')
	#############################
	clf = SVR()	# defaultly using radial basis function
	clf.fit(inputTrain, targetVals)
	#print clf.predict(inputTrain)-
	errTrainV = np.divide(abs(clf.fit(inputTrain,targetVals).predict(inputTrain)-targetVals), targetVals)# .max()
	print errTrainV.mean(), "...prediction - training error...";
	#print errV.max()
	######################
	####### testing ######
	dataframeV2 =None; 
	for i in xrange(48, len(vTest)):
		_r = []
		for j in xrange(1,24):
			# _r.append(v[i-j][0])
			_r.append(vTest[i-j])
		# _r.append(v[i][0])
		_r.append(vTest[i])
		#print _r 
		if dataframeV2 is None: 
			dataframeV2 = np.array(_r);
		else:
			dataframeV2 = np.vstack((dataframeV2, np.array(_r) ))

	#print dataframe.shape			 
	#
	inputTest = dataframeV2[:,:48]
	#print inputTrain
	targetValsTest = dataframeV2[:,-1]

 	errTestV = np.divide(abs(clf.predict(inputTest)-targetValsTest), targetValsTest)

	return (errTrainV.mean(), errTestV.mean())