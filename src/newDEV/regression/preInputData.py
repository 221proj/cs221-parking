### this script prepare the input data format
#
# 
# 
import os, datetime, re
import numpy as np 
import sortLotbyGeo 
from operator import itemgetter, attrgetter
from collections import OrderedDict
import matplotlib.pyplot as plt
from collections import Counter

#########################
# mal-function lot 
#########################

fault_Lot_pool = ["359051", "202001","701022","549201","720241","720052"]
fault_date = ['2013_09_20', '2013_09_19']

PATH = "../../../refineData/WeekDay/OCC/1_Hr/"

T_15 = 67  
T_60 = 18 # 60 minutes resolution... 
#
# val here is the value of parking lot
#

def readInFile(pth, desc, fal_l_pool):
	lotStack = None;
	fpth = pth + desc +"/"
	for val in os.listdir(fpth):
		lotFpth = fpth+val+"/"
		if len(val) < 5:
			continue
		elif val in fal_l_pool:  
			continue

		lotM = readInLot(lotFpth)		
		#print lotFpth 		

		if lotM is not None:
			if lotStack is None:    
				lotStack = lotM   
			else: 
				lotStack = np.vstack((lotStack, lotM))		
		
		if lotM != None:
			print lotM, val

	return lotStack

#process file according to Lot  
def readInLot(pth):
	# print pth
	# process each ren
	# plt.figure()
	vecStack = None; 

	for val in os.listdir(pth):
		#print val 
		spth = pth+val 
		if (re.match(".*"+fault_date[0], val) is None) and (re.match(".*"+fault_date[1], val) is None):  
			#print 
			vec = processSingleFile(spth)
		else:
			print val 
			a1= re.match(".*"+fault_date[0], val)
			a2= re.match(".*"+fault_date[1], val) 
			print a1 ,"more detail on ver1..."
			print a2 , "more detail on ver2..."
			raise NameError("file is invalid date ")

		if vec != None:
			return vec 
		"""
		if vec is not None:
			
			#plt.plot(vec)

			if vecStack is None:    
				vecStack = vec   
			else: 
				vecStack = np.vstack((vecStack, vec))		
		"""		
	#print vecStack.shape
	#plt.show()

	#rows = vecStack.shape[0]
	#if rows < 20:
	"""
	if vecStack is None: 
		print pth 
	
		#print vecStack
	"""
	#print vec 
	#	print vecStack.shape
		

	return vecStack	


# reading candidate parking list
def readInLotWithCandi(pth, desc, candi):
	
	vecStack = None; 
	vecDict = {}
	#following loop over lot id 
	for val in candi:
		spth = pth+desc +"/"+ str(val)+"/"
		# following loop over date 
		for val2 in os.listdir(spth):
			#print val2
			if (re.match(".*"+fault_date[0], val2) is None) and (re.match(".*"+fault_date[1], val2) is None):  
				#print 
				val2 = val2.rstrip("~")
				_name_term = val2.split("_");
				date_key = _name_term[1]+_name_term[2]+_name_term[3][:-4]
				
				#print _name_term[1],_name_term[2],_name_term[3][:-4]
				
				sfpth = spth+val2	# single file path 
				vec = processSingleFile(sfpth)
				if vec is not None:
					# print "DEBUG...",vec 
					# print val2
					occVec, tc = vec; 
					_v = np.append(occVec, tc)
				elif vec is None:
					print "...vector of daily occ is incorrect...",val2
					continue
					# raise ValueError("incorrect file ")	

				if date_key not in vecDict:					
					vecDict[date_key]= _v
				else:
					curr = vecDict[date_key] 
					#print curr.shape, _v.shape
					#print _v.shape
					new_v = np.vstack((curr, _v))
					vecDict[date_key]= new_v
					#print new_v

			else:
				print val2

		#print spth
	# print vecDict 
	dictTimeSerieDat = compressAggregation(vecDict)
	
	# print dictTimeSerieDat	

	return dictTimeSerieDat



# for sanity check 
def processSingleFile(pth):
	# print pth
	fp = open(pth, "r")
	dayStack = []
	tc = 0 
	ratio = None
	for line in fp:
		_temp = line.split(",")
		ratio = _temp[-1][0:-1]
		r = float(ratio)
		
		# int(_temp[-2])
		tc = max(int(_temp[-2]), tc)

		#print "total cap...",tc, pth[-19:] 
		if r < 0 or r > 1 :
			print r 
			raise ValueError("ratio is out of bound")

		if tc < 0 :
			#print r 
			#print pth[-19:]	# display the file name  
			#print "..total cap..",tc 
			return tc
			#raise ValueError("the capacity is not valid ")
		dayStack.append(float(ratio))	

	if (24 - len(dayStack) == 1) and ratio is not None:
		dayStack.append(float(ratio))	

	# check if there is enough data entry	
	if len(dayStack) == 24:
		a = np.array(dayStack)
		#print np.sum(a) 
		# a_N = a/np.sum(a)
		#print a_N
		#print len(a)
		 
		if sum(dayStack) < 0.1:
			#print dayStack
			return None	
		
		# return daily occupancy stack 
		return (a, tc)  
		# normal small 	
		#return a_N 
	else:
		print "insufficient data..."	
		return None			

#######################################
# compress dictionary into aggregated occ   
#
####################################### 
def compressAggregation(occDict):
	cmpDict = dict()
	for i, j in enumerate(occDict):
		# j is the date, also as dictionary key
		# 
		m = occDict[j];
		print j, m.shape;
		# 	k - from 0 to len(dict), where dict contains aggregated lots 
		dsumVec = None 
		tc = 0;
		if len(m.shape)==1:
			dsumVec=m[0:24]
			tc = 1 
			break 
		else:	
			for k in range(m.shape[0]):
		 		#print j, k, m[k:(k+1),0:24];
		 		a = m[k:(k+1),0:24]*(m[k:(k+1),24])	
		 		a = np.ceil(a) #, "with ", (m[k:(k+1),24])	
		 		tc = tc + m[k:(k+1),24]
		 		if dsumVec is None:
		 			dsumVec = a 
		 		elif dsumVec is not None:
		 			dsumVec = dsumVec+a  	
		
		# print dsumVec/tc 
		cmpDict[j] = dsumVec/tc	

	return cmpDict
			
######################################
# main part 
# - start to run 			
###########################################

DWK = ["monday", "tuesday", "wendesday","thursday","friday"] 

#test = readInFile(PATH, "monday")
#test = readInFile(PATH, "tuesday")
#test = readInFile(PATH, DWK[4], fault_Lot_pool)
position = [37.790781, -122.403967]
# generate candidate list of parking lot list 
# a, b = sortLotbyGeo.generateSortedLot(position, 150)  # a == candidate lots , b == total volum

#readInLotWithCandi(PATH, DWK[2], a)
#print a
#print b 

##############
# (PATH, day, a) 
#
##############
def run(pth, dowSet, candi):
	totTS_dict = None;

	for day in dowSet:
		if totTS_dict is None:
			totTS_dict = readInLotWithCandi(pth, day, candi)
		elif totTS_dict is not None:
			_d = readInLotWithCandi(pth, day, candi)
			totTS_dict = dict(totTS_dict.items() + _d.items())

	#dat = sorted(totTS_dict)	
	dat = OrderedDict(sorted(totTS_dict.items(), key=lambda t: t[0]))

	#print dat
	#callseeDataFormat(dat)
	return dat 

###############
# reconstruct dictionary
# 
def reconstruct(dat, vsum, i):
	# the dat sanity check 
	if dat is None:
		raise ValueError("reconstruct dict - ERROR: input data is None")

	mkdict = {} 
	for k, v in dat.iteritems():
		#print type(k)
		mkdict[(k, vsum, i)] = v    

	#print mkdict
	
	# print mkdict


	return mkdict	
# 	
# 




################
# 
def callseeDataPattern(datdict):
	vols = None;
	plt.figure()
	for k,v in datdict.iteritems():
		
		if vols is None:
			vols = v 	
		else:
			vols = np.append(vols, v)	
		#print "v ",v.shape	
		#print "lin", np.linspace(0,23,24).
		#plt.plot(np.linspace(0,23,24).reshape(1,24), v)	
		# plt.plot(np.linspace(0,23,24))	
		# 
		plt.plot(v[0])
		# plt.show()
		#print v[0] 

	####
	# show the figure plot
	####
	
	#plt.plot(vols)
	plt.show()

############

############

#run(PATH, DWK, a)


######################
# position in 
# ../../refineData/

######################
# more general case candidates  
# - pick the centroid position  
# 

#######################
#  			left 						right 
#  SOMA = 37.782566, -122.424210 ; 	37.783685, -122.415928   //up 
#		  37.772424, -122.423695 ; 	37.779852, -122.413353	 //down
#  Mission	37.764672, -122.424232 ; 	37.763553, -122.417666
# 			37.751949, -122.423331 ;	37.752424, -122.416250

# Fillmore	37.794012, -122.436634 ;	37.789476, -122.428706 
# Cal st 	37.779344, -122.433544 ;	37.780081, -122.426946

# Lambard	37.800023, -122.442825 ;	37.800972, -122.434585
# 			37.797310, -122.442310 ;	37.798192, -122.434027

# Fishermans 	37.806330, -122.423685 ;	37.808059, -122.410724
# Wharf	   		37.803312, -122.423213 ;	37.805177, -122.409952
#
# Finice Dist   37.795649, -122.409866 ;	37.797310, -122.397232
#			 	37.786424, -122.407913 ; 	37.791087, -122.395773
#
# ATT park 	 37.794445, -122.394808 ;	37.785746, -122.388177
# 			 37.786085, -122.405472 ;	37.775333, -122.397297 
#
#
#######################
#
REGIONS_DICT = {  'ATT': ([37.794445, -122.394808], [37.775333, -122.397297]), \
			'FD': ([37.795649, -122.409866], [37.791087, -122.395773]),  \
			'FW': ([37.806330, -122.423685], [37.805177, -122.409952]),	\
			'La': ([37.800023, -122.442825], [37.798192, -122.434027]),	\
			'FC': ([37.794012, -122.436634], [37.780081, -122.426946]),	\
			'Mission': ([37.764672, -122.424232], [37.752424, -122.416250]), \
			'SoMa': ([37.782566, -122.424210], [37.779852, -122.413353])	\
			}

#######################
# update REGION Dictionary 
#######################
REGION_DICT_V2 = { 'ATT': ([37.794445, -122.394808], [37.785746, -122.388177], [37.786085, -122.405472], [37.775333, -122.397297] ), \
				'FD': ([37.795649, -122.409866], [37.797310, -122.397232], [37.786424, -122.407913], [37.791087, -122.395773] ), \
				'FW': ([37.806330, -122.423685], [37.808059, -122.410724], [37.803312, -122.423213], [37.805177, -122.409952] ), \
				'La': ([37.800023, -122.442825], [37.800972, -122.434585], [37.797310, -122.442310], [37.798192, -122.434027] ), \
				'FC': ([37.794012, -122.436634], [37.789476, -122.428706], [37.779344, -122.433544], [37.780081, -122.426946] ), \
				'Mission': ([37.764672, -122.424232], [37.763553, -122.417666], [37.751949, -122.423331], [37.752424, -122.416250]), \
				'SoMa': ([37.782566, -122.424210], [37.783685, -122.415928], [37.772424, -122.423695], [37.779852, -122.413353])	\
			}

######################




# outter loop is the region 
def crossRegionClassification(regions):
	
	aggDD = None	#aggregated dictionary data
	i = 0
	for k,v in regions.iteritems():
		#print k,v 
		r_upleft = v[0]
		r_lowright = v[1]

		r_width = v[0][0] - v[1][0]
		r_hight = v[0][1] - v[1][1] 

		step_w = r_width/5
		step_h = r_hight/5

		# initialize a dictionary 
		#
		# aggDD = None	# store multiple data set  
		
		for _m in range(1,5):
			for _n in range(5):
				pos = [r_upleft[0]+_m*step_w, r_upleft[1]+_n*step_h]
				cand_l, sumV = sortLotbyGeo.generateSortedLot(pos, 150)
				_dd = run(PATH, DWK, cand_l)
				i += 1
				# resue the _dd 
				_dd = reconstruct(_dd, sumV, i) # change the key to reform the dictionary of the aggregated occ data 

				if aggDD is None:
					aggDD = _dd
				else:
					aggDD = dict(aggDD.items() + _dd.items())	
				
				#callseeDataPattern(_dd)	
		
		#######
		# run clustering through out whole city	 		
		try:
			import model
			# model.runAnalysis(dat)
			model.runClassification(aggDD)
		except ImportError:
			pass		


####
# function to call prediction 
def crossRegionPrediction(regions):
	# loop over several regions 
	#	
	aggDD = None	#aggregated dictionary data
	i = 0

	errV_zones = []

	bestOrderArrays = [] 

	for k,v in regions.iteritems():
		#print k,v 
		# r_upleft = v[0]
		# r_lowright = v[1]

		# r_width = v[0][0] - v[1][0]
		# r_hight = v[0][1] - v[1][1] 

		# step_w = r_width/5
		# step_h = r_hight/5
		############################
		# 
		# 
		points = genLocPin(v)
		# print k, points 

		# raise NotImplementedError("not implemented")

		# continue 
		# initialize a dictionary 
		#
		# aggDD = None	# store multiple data set  
		bestO = None 
		for _m in range(1,2):	#range 1 to 5
			# for _n in range(5):
			for pos	in points:

				aggDD = None;
				# pos = [r_upleft[0]-_m*step_w, r_upleft[1]-_n*step_h]
				cand_l, sumV = sortLotbyGeo.generateSortedLotV2(pos, 115)	# tune the aggregation level here
				_dd = run(PATH, DWK, cand_l)
				i += 1
				# resue the _dd 


				_dd = reconstruct(_dd, sumV, i) # change the key to evaluate the 
				
				_dd = resortByTimeseries(_dd)

				if aggDD is None:
					aggDD = _dd
				else:
					aggDD = dict(aggDD.items() + _dd.items())	
				
				#callseeDataPattern(_dd)
				try:
					import model 
					# bestO = model.runAnalysis(aggDD, 0.5)
					# meanERR = model.runTSAprediction(aggDD, 0.05)
					# meanERR = model.runTSAprediction(aggDD, 0.15)
					#######################################
					meanERR = model.runOLSregression(aggDD)
					
					# errV_zones.append(meanERR)
					if np.isnan(meanERR):
						continue

					inputInfo = (tuple(pos), meanERR, sumV)

					writeTofile('err/heatmap/err_gen_heatmap_'+str(k)+'.txt', str(inputInfo))
					#######################################
					model.outputPicklefile(inputInfo, 'errpickle', 'err/heatmap/'+str(k)+str(i)+'OLS_agg_err.p')
				except:	
					# raise NotImplementedError("call prediction analysis error") 
					raise "more information needed ... generate error file "
					pass 

				# break
			# break		
			#	# bestOrderArrays.append(bestO) 

		# print "mape: ",errV_zones	

	# print "Whole MAPE Vector: \n", errV_zones
	# print bestOrderArrays 

##########################
# gen Location 
##########################
def genLocPin(region):
	rightBound = max(region[0][1], region[1][1],region[2][1],region[3][1])  # no point 
	leftBound = min(region[0][1], region[1][1],region[2][1],region[3][1])
	upperBound = max(region[0][0], region[1][0],region[2][0],region[3][0])
	lowerBound = min(region[0][0], region[1][0],region[2][0],region[3][0])

	m_lat = np.median([region[0][0], region[3][0]])
	m_lng = np.median([region[0][1], region[3][1]])

	# print (m_lat, m_lng)
	space1 = np.linspace(0, 2, 9)-1
	space2 = np.linspace(0, 2, 9)-1
	# print space1 , space2
	points = [] 
	for val1 in space1:
		for val2 in space2:
			cur_lat = m_lat+0.01*val1
			cur_lng = m_lng+0.01*val2
			# print (m_lat+0.01*val1, m_lng+0.01*val2) 
			# print (cur_lat, cur_lng)

			if cur_lng > leftBound and cur_lng < rightBound and cur_lat < upperBound and cur_lat > lowerBound:
				# print (cur_lat, cur_lng)  
				points.append([cur_lat, cur_lng])

	return points	



###########################
# write content to file 
####
def writeTofile(fpth, content):
	fp = open(fpth,'a');
	fp.write(content+'\r\n');
	fp.close()


#########################
#
#########################
def resortByTimeseries(datDict):
	print "****************"
	# print datDict
	dat =OrderedDict(sorted(datDict.iteritems(), key=lambda k: k[0]))
	# print dat 
	return dat
#
#
#



#####import system time#####
import time

##########################
#
# see the aggregation level increasing vs prediction error 
########################## 

def aggregateVSpredict(regions):
	aggDD = None	#aggregated dictionary data
	i = 0

	# errV_zones = []
	bestOrderArrays = [] 
	for k,v in regions.iteritems():
		#print k,v 
		r_upleft = v[0]
		r_lowright = v[1]

		r_width = v[0][0] - v[1][0]
		r_hight = v[0][1] - v[1][1] 

		step_w = r_width/5
		step_h = r_hight/5

		# initialize a dictionary 
		#
		# aggDD = None	# store multiple data set 

		aggSumLevel = []
		aggErrLevel = [] 
		
		for _m in range(1,5):	# range 1 to 5
			for _n in range(0,5):		# range (0 to 5)		
				# aggDD = None;
				pos = [r_upleft[0]+_m*step_w, r_upleft[1]+_n*step_h]
				aggSumLevel = []
				aggErrLevel = []
				for _nLevel in range(15, 390, 10): 
					aggDD = None;	
					# cand_l, sumV = sortLotbyGeo.generateSortedLot(pos, _nLevel)	# tune the aggregation level here
					cand_l, sumV = sortLotbyGeo.generateSortedLotV2(pos, _nLevel)	# update aggregation with distance range check
					# cand_l, sumV = sortLotbyGeo.generateSortedLotWithGarage(pos, _nLevel)

					# print cand_l 
					# raise NotImplementedError("........debug break point.........")

					_dd = run(PATH, DWK, cand_l)
					i += 1
					# resue the _dd 
					_dd = reconstruct(_dd, sumV, i) # change the key to evaluate the 
					# print _dd 
					_dd = resortByTimeseries(_dd)
					# if i > 1: 
					# raise NotImplementedError("PLEASE --- see more details ---")

					if aggDD is None:
						aggDD = _dd
					else:
						aggDD = dict(aggDD.items() + _dd.items())	
				
					# callseeDataPattern(_dd)
					bestO = None;
					try:
						# print ">>>>>>>>>>>>>>>>>"
						import model 
						############################
						
						# meanERR = model.runOLSregression(aggDD)


						############################ 
						# dvector = model.reshaping(aggDD);
						# print dvector

						# datArr = []
						# for i in xrange(25, len(dvector)):
						# 	# pointavg = model.deTranding(dvector, i, 24, 5)
						# 	# detrandData = dvector[i]-pointavg
						# 	# datArr.append(detrandData);
						# 	pointavg = model.deTrandingV2(dvector, i, 1,24,5);
						# 	detrandData = dvector[i] - pointavg;


						# denoiseSeries = np.array(datArr);

						# print "denoise series:", denoiseSeries
						############################
						# plt.figure()
						# plt.plot(denoiseSeries)
						# plt.show()
						############################
						
						# denoiseSeries2 = [];
						# for i in xrange(2,len(denoiseSeries)):
						# 	point_ma = model.deTranding(denoiseSeries,i, 1, 1)
						# 	maData = denoiseSeries[i]-point_ma;
						# 	denoiseSeries2.append(maData)

						# denoiseSeries2 = np.array(denoiseSeries2)	
						
						#########################
						# plt.figure()
						# plt.plot(denoiseSeries2)
						# plt.show()
						#########################
						# bestO = model.runAnalysisV2(denoiseSeries2, 0.5)
						# print ">>>>>>>>>>>>>>>>>"
						
						# meanERR = model.runTSApredictionV2(denoiseSeries, 0.15)

						# meanERR = model.runSVMprediction(aggDD, 0.15)
						meanERR = model.runFFNNprediction(aggDD,0.15)
						# print meanERR
						# time.sleep(5)
						aggErrLevel.append(meanERR)
						aggSumLevel.append(int(sumV))

					except:	
						# print "call Timeseries...Error "
						print ">>>call ols regression error>>>..."
						# print "call SVM prediction ... error" 
						# print "call FFNN prediction .. Error " 
						time.sleep(1)
						pass 
					###################
					# check to see 	
					if len(aggSumLevel) > 3 :
						if aggSumLevel[-1] == aggSumLevel[-3]:
							break;				

					# writeTofile("bestOrder.txt",str(bestO))		
					# bestOrderArrays.append(bestO)		
				
				# print bestOrderArrays
				# time.sleep(1)
				# print aggSumLevel, aggErrLevel

				#######
				#  
				#  
				############################
				aggSumLevel, aggErrLevel = getuniquepair(aggSumLevel,aggErrLevel)


				#######################
				# write to pickle 
				######################
				model.outputPicklefile([aggSumLevel, aggErrLevel], 'errpickle', 'err/'+str(k)+str(i)+'FFNN_agg_err.p') 
				#######################
				# plot the aggregation vs distance increase 
				#######################

				try:	
					plt.figure()
					plt.plot(aggSumLevel, aggErrLevel, linewidth=2.5)
					plt.xlabel("aggregated spots", fontsize=16)
					plt.ylabel("prediction error ratio", fontsize=16)
					plt.xticks(fontsize=16)
					plt.yticks(fontsize=16)
					plt.ylim(0,0.15)
					# plt.title(str(pos))
					# plt.savefig('fig/'+str(k)+'OLS_err_vs_agg'+str(pos)+'.eps')
					# plt.savefig('fig/TS_new_err_vs_agg'+str(pos)+"_"+str(k)+'.eps')
					plt.savefig('fig/'+str(k)+'FFNN_err_vs_agg'+str(pos)+'.eps')
				# 	# plt.savefig('fig/SVM_new_err_vs_agg'+str(pos)+"_"+str(k)+'.eps')
				# 	plt.savefig('fig/TSA_new_err_vs_agg'+str(pos)+"_"+str(k)+'.eps')
					# plt.show()
				except:	
					raise NotImplementedError("aggregation level increment plot ERROR")

				# break		
			# break	
		# print bestOrderArrays	
#####################






#################
# small function to get nuique (aggregation, error) pair
# 
def getuniquepair(sumLevel, errV): 
	s = [];
	e = [];
	if len(sumLevel) != len(errV):
		raise ValueError("summation level doesn't match the estimation error")

	for i in range(1,len(sumLevel)): 
		if sumLevel[i] == sumLevel[i-1]:
			continue;
		s.append(sumLevel[i]);	
		e.append(errV[i])	

	return (s, e) 




######################

def runSimpleAveragePrediction(regions):

	aggDD = None	#aggregated dictionary data
	i = 0

	# errV_zones = []

	for k,v in regions.iteritems():
		#print k,v 
		r_upleft = v[0]
		r_lowright = v[1]

		r_width = v[0][0] - v[1][0]
		r_hight = v[0][1] - v[1][1] 

		step_w = r_width/5
		step_h = r_hight/5

		# initialize a dictionary 
		#
		# aggDD = None	# store multiple data set 

		aggSumLevel = []
		aggErrLevel = [] 
		
		for _m in range(1,5):	# range 1 to 5
			for _n in range(1,5):		# range (0 to 5)		
				# aggDD = None;
				pos = [r_upleft[0]+_m*step_w, r_upleft[1]+_n*step_h]
				aggSumLevel = []
				aggErrLevel = []
				for _nLevel in range(100, 101): 
					aggDD = None;	
					# cand_l, sumV = sortLotbyGeo.generateSortedLot(pos, _nLevel)	# tune the aggregation level here
					cand_l, sumV = sortLotbyGeo.generateSortedLotV2(pos, _nLevel)	# update aggregation with distance range check
					# cand_l, sumV = sortLotbyGeo.generateSortedLotWithGarage(pos, _nLevel)

					# print cand_l 
					# raise NotImplementedError("........debug break point.........")

					_dd = run(PATH, DWK, cand_l)
					i += 1
					# resue the _dd 
					_dd = reconstruct(_dd, sumV, i) # change the key to evaluate the 
					# print _dd 
					_dd = resortByTimeseries(_dd)
					# if i > 1: 
					# raise NotImplementedError("PLEASE --- see more details ---")

					if aggDD is None:
						aggDD = _dd
					else:
						aggDD = dict(aggDD.items() + _dd.items())	
				
					# callseeDataPattern(_dd)

					# seeDict(aggDD, 8,13);



					# raise NotImplementedError("manual break");
					try:
						import model 

						# model.runPCAonDays(aggDD, 60, 65)
						# model.runAnalysis(aggDD, 0.5)
						# meanERR = model.runTSAprediction(aggDD, 0.15)
						# meanERR = model.runSVMprediction(aggDD, 0.15)
						# 
						dvector = model.reshaping(aggDD);
						# print dvector

						datArr = []
						for i in xrange(24, len(dvector)):

							pointavg = model.deTranding(dvector, i,24, 5)
							detrandData = dvector[i]-pointavg
							datArr.append(detrandData);
						
						denoiseSeries = np.array(datArr);

						print "denoise series:", denoiseSeries

						denoiseSeries2 = [];
						for i in xrange(2,len(denoiseSeries)):
							point_ma = model.deTranding(denoiseSeries,i, 1, 1)
							maData = denoiseSeries[i]-point_ma;
							denoiseSeries2.append(maData)

						denoiseSeries2 = np.array(denoiseSeries2)	
						########################
						# plt.figure()
						# plt.plot(denoiseSeries)
						# plt.plot(denoiseSeries2,'r')
						# plt.show()

						meanERR = model.runTSApredictionV2(denoiseSeries2, 0.15)
						########################
						# print dvector.shape

						# print "average value:", pointavg, " real value ", dvector[100];

						# raise NotImplementedError("not implement")


						# meanERR = model.runAVGprediction(aggDD, 0.15)
						# aggErrLevel.append(meanERR)
						# aggSumLevel.append(int(sumV))

					except:	
						print "run simple average " 
						time.sleep(1)
						raise NotImplementedError("error..........")
						pass 
					###################
					# check to see 	
					if len(aggSumLevel) > 3 :
						if aggSumLevel[-1] == aggSumLevel[-3]:
							break;				

				print aggSumLevel, aggErrLevel
				#######################
				# plot the 
				#######
				# aggSumLevel=set(aggSumLevel)
				# aggErrLevel=set(aggErrLevel)

				try:	
					plt.figure()
					plt.plot(aggSumLevel, aggErrLevel)
					plt.xlabel("aggregated spots", fontsize=16)
					plt.ylabel("prediction error ratio", fontsize=16)

					# plt.title(str(pos))
					# plt.savefig('fig/AVG_new_err_vs_agg'+str(pos)+"_"+str(k)+'.eps')
					plt.savefig('fig/new_err_vs_agg'+str(pos)+"_"+str(k)+'.eps')
					# plt.show()
				except:	
					raise NotImplementedError("aggregation level increment plot ERROR")


##############################
def runOLSPrediction(regions):

	aggDD = None	#aggregated dictionary data
	i = 0
	# errV_zones = []

	for k,v in regions.iteritems():
		#print k,v 
		r_upleft = v[0]
		r_lowright = v[1]

		r_width = v[0][0] - v[1][0]
		r_hight = v[0][1] - v[1][1] 

		step_w = r_width/5
		step_h = r_hight/5

		# initialize a dictionary 
		# aggDD = None	# store multiple data set 

		aggSumLevel = []
		aggErrLevel = [] 
		
		for _m in range(2,3):	# range 1 to 5
			for _n in range(2,3):		# range (0 to 5)		
				# aggDD = None;
				pos = [r_upleft[0]+_m*step_w, r_upleft[1]+_n*step_h]
				aggSumLevel = []
				aggErrLevel = []
				for _nLevel in range(90, 91): 
					aggDD = None;	
					cand_l, sumV = sortLotbyGeo.generateSortedLotV2(pos, _nLevel)	# update aggregation with distance range check
				
					_dd = run(PATH, DWK, cand_l)
					i += 1
					# resue the _dd 
					_dd = reconstruct(_dd, sumV, i) # change the key to evaluate the 
					# print _dd 
					_dd = resortByTimeseries(_dd)
					# if i > 1: 
					# raise NotImplementedError("PLEASE --- see more details ---")

					if aggDD is None:
						aggDD = _dd
					else:
						aggDD = dict(aggDD.items() + _dd.items())	
				
					# callseeDataPattern(_dd)
					# seeDict(aggDD, 8,13);
					# raise NotImplementedError("manual break");
					try:
						import model 
						# dvector = model.reshaping(aggDD);
						# print dvector
						datArr = []
						# model.deTrendingIndicate(aggDD, k)

						# model.outputPicklefile(aggDD, k)
						raise NotImplementedError("suspend..........")
					except:	
						# print "run simple average " 
						time.sleep(1)
						raise NotImplementedError("error..........")
						# pass 
					###################
					# check to see 	
					if len(aggSumLevel) > 3 :
						if aggSumLevel[-1] == aggSumLevel[-3]:
							break;				

				print aggSumLevel, aggErrLevel
				#######################
				# plot the 
				#######
				# aggSumLevel=set(aggSumLevel)
				# aggErrLevel=set(aggErrLevel)

	



 
#############################
# see the average curve 
def seeDict(dicItems, start, end):
	i = 0; 
	dayAVG = None;
	daysLabel = [];
	nextDay = None;
	plt.figure()
	for k, v in dicItems.items():
		i+=1
		if i < start:
			continue

		if i >= end: 
			nextDay = (k[0],v[0]);
			break;

		print k, v;
		plt.plot(v[0], '--', linewidth=1.5)
		
		if dayAVG is None:
			dayAVG = v[0];
		else:
			dayAVG = np.vstack((dayAVG, v[0]));

		daysLabel.append(k[0]);

	avgCurve = np.mean(dayAVG, axis=0);		
	plt.plot(avgCurve, 'k-', linewidth=3);
	
	plt.plot(nextDay[1], 'b-',linewidth=2.5);

	daysLabel.append("average");
	daysLabel.append(nextDay[0]);
	plt.legend(daysLabel, loc="lower right");
	plt.ylim(0,1) 
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	# plt.rc('font', labelsize=40) 
	# plt.rc('ytick', labelsize=33) 

	plt.show()	

#####################


####################
# run classification 
######
# crossRegionClassification(REGIONS_DICT)


# for position in posSet:
# 	a, b = sortLotbyGeo.generateSortedLot(position, 150)  
# 	run(PATH, DWK, a)

#####################
# run prediction
###### 
crossRegionPrediction(REGION_DICT_V2)


#####################
# run aggregation increament 
######
# aggregateVSpredict(REGIONS_DICT)


#####################
# run svm prediction 
#####################



####################
# run simple average
#

# runSimpleAveragePrediction(REGIONS_DICT)	

#####################
# run the detrending function 
###

# runOLSPrediction(REGIONS_DICT)