"""
This script is working for grid search and accumulate parking lots 

- so far assuming threshold is 100 spots 

"""
import numpy as np 
import math, os, datetime
from collections import Counter, OrderedDict
import pandas as pd 
import RpyCode as rpycode 
#import RpyCodeNNet as rpynnet
import matplotlib.pyplot as plt
import ffnetUtil 
import svmUtil



BOUND_UpLeft = [37.794423,-122.409374]
BOUND_LowRight = [37.780077,-122.392]
#runDateFirstAggregateMeth
REAGIN_WIDTH = BOUND_UpLeft[0] - BOUND_LowRight[0]
REAGIN_HIGHT = BOUND_UpLeft[1] - BOUND_LowRight[1] # this is negative step 

step_width = REAGIN_WIDTH/10;
step_hight = REAGIN_HIGHT/10;

#print setp_hight, setp_width

#####################################
# shared functions 
def calculateDistance(loc1, loc2, unit='mile'):
	"""
	Calculating the distance between the location1 and location2 
	show the 
	
	"""    
	lat1, lng1 = loc1
	lat2, lng2 = loc2
		
	radius_km = 6371  # km
	radius_mile= 3960 # mile    
	
	
	difflat = math.radians(lat2-lat1)
	difflng = math.radians(lng2-lng1)
	
	a = math.sin(difflat/2) * math.sin(difflat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(difflng/2) * math.sin(difflng/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	if unit == 'mile':    
		d = radius_mile * c
	elif unit == 'km':
		d = radius_km * c
	else:    
		raise "none valid unit "
	
	return d

#####################################
# generate capacity map 
LOT_CAP_PATH = '../LOT_CAP.txt';

def getLotCapDict(fpath):
	_lotCap = {}
	fp = open(fpath, 'r')
	for line in fp:
		#print line
		#_id, _cap = line.split(",")
		_ = line.split(",")
		#print _
		#print _[0], _[1][0:-2]
		_lotCap[int(_[0])] = int(_[1][0:-2])
		#print int(_id), int(_cap)  

	return _lotCap 
		
##### 

#####################################
LOCATION_ID_PATH = '../../../idLocation/helloLocation.txt'

def genLocMap(fpath):
	locMap = None
	fp = open(fpath, 'r')
	for line in fp:
		#print line
		locRow = []
		_t = line.split(', ');
		if int(_t[1][1:-1]) > 0 : 
			# off street parking ID 
			_LID =  int(_t[1][1:-1])
		else: 
			_LID = int(_t[2][1:-1])	
		#print locList
		locRow.append(_LID)
		_lat = float(_t[3][2:-1]);
		_lng = float(_t[4][1:-5])
		locRow.append(_lat)
		locRow.append(_lng)
		if locMap is None:
			locMap = np.array(locRow)
		else:
			locMap = np.vstack((locMap, np.array(locRow))) 
		#print locList
	#print locMap.shape
	return locMap	

# generate 
LOC_LIST = genLocMap(LOCATION_ID_PATH)



def appendDistCol(centroid, locMap):
	"""
	calcuate distance 
	& sorted by nearest dist 
	"""
	_m = None  
	for i, item in enumerate(locMap):
		_lotGeo = [item[1], item[2]] 
		_d = calculateDistance(centroid, _lotGeo)
		_row = np.append(item, _d)
		if _m is None:
			_m = np.array(_row)
		else:	
			_m = np.vstack((_m, np.array(_row)))
		#print _d 
	#print _m.shape	
	#print _m
	r, c = _m.shape

	return _m[_m[:,c-1].argsort()]


###################################

#def sortLot(centroid, )
#print locCapMap

####################################
#
# start to run 
#
####################################


def addpLots(sLotList, capMap, threshold):
	"""
	sLotList - sorted Lot list -- is 2d nparray, 
	capMap - dictionary, key is lotID, val is capacity
	"""
	m, n = sLotList.shape
	i = 0
	aggV = 0;

	nearbyLots = []; 
	while i < m and aggV < threshold:

		_id = sLotList[i,0:1] 
		_id=int(_id)
		#print int(_id)

		capV = capMap[_id]
		if capV > 0 and _id > 1000:
			aggV = aggV+capV
			nearbyLots.append(_id)
		
		i = i+1

	return (nearbyLots, aggV)	



###############################
# start to agg
# 
###############################
REF_DATA_P = "/home/seanqian/Desktop/dev/cs221/repo-221proj/cs221-parking/refineData/1_HOUR/"

##############

def convertFileToDataTable(fpath):
	df = pd.read_csv(fpath, header=None)
	return df 


def extractMonthDay(filename):
	"""
	func to extract the day & month from 
	@param filename = "parkLotID_yy_mm_dd.csv"
	"""
	if type(filename) is not str:
		assert "not pass-in a string as filename"

	_s = filename.strip(".csv")    
	_l = _s.split("_")    
	#print _l[1] 

	return (_l[2], _l[3]) 


##########################
def runDateFirstAggregateMeth(candiList, relroot, step=1):     
		"""
		step = 1 means aggregate lot 1 by 1 
		"""

		lotSizeDict = dict()


		for i, val in enumerate(candiList):
			# each lot 
			#_plID = extractParkLotID(val) # parking lot ID 
			# print val, ">>>>", extractParkLotID(val)  
			_plID = val;
			lotSizeDict[_plID] = None 
			lotIDTimeseries = Counter() 
			val = relroot+str(val)+"/"
			#############################
			#plt.figure()
			lotDayLevelSeries = Counter()

			for fname in os.listdir(val): 
				# each day 
				# print extractMonthDay(fname)
				# print fname
				# create a stack to store the occupancy rate
				dailyStack = None 
				mm, dd = extractMonthDay(fname) 
				

				#if isInTargetDateRange((mm,dd), (self.startMM, self.startDay) , (self.endMM, self.endDay) ):
				if 1>0:	
					pDataFrame = convertFileToDataTable(str(val+fname))
					 
					_operNumInit = pDataFrame[3][0] 
					_operNumInit = _operNumInit.replace('\"','')
					_operNumInit = float(_operNumInit)
				
					if _operNumInit > 100:
						print "garage"
						print fname
						print dailyStack

						continue

					#if len(pDataFrame) < 284: # 284 is for 5 minutes gap data

					if len(pDataFrame) < 16:
						print "incomplete dataset"
						print "current record:", len(pDataFrame)

						continue

					#print sum([ float(pDataFrame[3][i]) for i in range(len(pDataFrame))])   
					#print pDataFrame     

					_soperlist = [] 
					_socclist = []
					#_spricelist =[]

					for j in xrange(len(pDataFrame)):
																	
						_ts = pDataFrame[0][j]

						_price = pDataFrame[4][j]  
						_price = _price.replace('\"', '') 
						
						_occNum = pDataFrame[2][j]
						_occNum = _occNum.replace('\"', '') 
						_occNum = float(_occNum)

						_operNum = pDataFrame[3][j] 
						_operNum = _operNum.replace('\"','')
						_operNum = float(_operNum)
						
						_soperlist.append(_operNum) 
						_socclist.append(_occNum)
						#_spricelist.append(_price)


						#if isInTimeSlotV2(_ts, self.startHr, self.endHr) and float(_price) >= 0 :
							#newV = []
						if float(_price) >= 0 :	
							if _operNum > 0:
								#print "-------------",float(_occNum)/float(_operNum)
								newV = np.array([pDataFrame[0][j], float(_occNum)/float(_operNum), _operNum])
							elif _operNum <= 0:
								print "does not record ----"
								#raise "notlotIDTimeseries in operation"
								continue

							else: 
								print "**********what happend?***********"
								continue


							
							if dailyStack is None:
								dailyStack = newV
							else:    
								dailyStack = np.vstack((dailyStack, newV))
								#print dailyStack

						elif float(_price) < 0:
							continue 

						#print dailyStack    
					###################################
					# val1 is TimeStamp, val2 is occRate, val3 is operNumber
					# lotIDTimeseries store whole time series
					
					#print "*price*", _spricelist

					if _soperlist.count(0) > 10:
						continue 


					if dailyStack is not None:

						for val1, val2, val3 in dailyStack: 
							lotIDTimeseries[val1] = (val2, val3)
						
					#sort 

						lotDayLevelSeries[str(mm+"-"+dd)] = dailyStack

			if len(lotIDTimeseries) < 1:
				assert "calculating occ, oper error!"
				continue

			sortedLotDict = sorted(lotIDTimeseries.items(), key = lambda x: x[0] )
			#print "sorting...",sortedLotDict
			lotSizeDict[_plID] = sortedLotDict

			
		err = aggregateDict(lotSizeDict, step) # radius, locNameDesc )
		#print "show error ", err 
		return err
##
##
##
def aggregateDict(lotDict, step=1, distrange=0, desp='NA'):
	aggDict = Counter()
	_dict_temp = Counter()
	c = []      # list of the aggregated lots 
	accumulatedVolume = 0

	lots = None 

	tnow = datetime.datetime.now()
	fileseed = str(tnow.month)+"_"+str(tnow.day)+"_"+str(tnow.hour)+str(tnow.minute)

	for key1, valDict1 in lotDict.items():
		

		#print ">>>>>>>>>>>>>>>>>>>", valDict1
		if valDict1 is None:
			continue

		c.append(key1)
		aggDict = _dict_temp    

		for key2, val2 in valDict1:
			#key2 = int(key2)
			#print "aggDict at beg of each loop", aggDict
			if not aggDict[key2]:
				aggDict[key2] = (val2[0]*val2[1], val2[1]) 
				   
			elif aggDict[key2]: 
				aggDict[key2] = (aggDict[key2][0] + val2[0]*val2[1] , aggDict[key2][1] + val2[1])
				#print "conti after",key2, aggDict[key2]
			accumulatedVolume = aggDict[key2][1]

			_dict_temp = aggDict.copy() 

		# accumulate parking lot one by one    
		lots, errRate, dat= showAggreationDict(_dict_temp, c)
	
	#print dat
	
	#reshape the data vector 
	datVector = np.reshape(dat, (dat.shape[0]*dat.shape[1], 1))
	
	# error of Feed Forward Nural Nets 
	#errFFNN = nerualNets(datVector, c)
	# error of Support Vector Machine
	#errSVM = svmRegression(datVector)

	#return errSVM  # return back the Support vector Machine error
	return errRate  # return back the AR error  
	#return errFFNN # return back the Nural Net Work Error 
	
	#print dat[1] 
	#plt.figure()
	#plt.plot(dat[1])
	#plt.show()
	#for j in range(dat.shape[0]):
	#	plt.plot(dat[j])
	#plt.show()

def showAggreationDict(aggParkLotDict, aggPList):
	
	aggDict = aggParkLotDict.copy()

	if len(aggDict) < 1:
		assert "error, empty dictionary"
		
	for key, val in aggDict.items():
		#print val[0], " and ", val[1]
		occR = float(val[0]/val[1]) 
		aggDict[key] = (occR, val[1])

	sortedaggDict = OrderedDict(sorted(aggDict.items()))    

	X = [int(key) for key in sortedaggDict]
	Y = [v[0] for key, v in sortedaggDict.items() ]  
	xNew = pd.to_datetime(X, unit='s')

	x_ts_new = xNew.tz_localize("UTC").tz_convert("America/Los_Angeles")
	 
	

	"""
	# here is the function called previously 
	err = timeSeriesAnalysis(x_ts_new, Y, aggPList)
	"""
	dat = reshapeData(Y)

	#nerualNets(x_ts_new, Y, aggPList)

	err = timeSeriesAnalysisV2(x_ts_new, Y, aggPList)

	print err 
	return (aggPList, err, dat)

############################
def timeSeriesAnalysisV2(v1, v2, Plist):
	#print v1
	print "***********"
	# v2 is occ
	#print v2
	#v1 = v1[:-24]
	#v2 = v2[:-24]
	if len(v2) > 48:
		return rpycode.show(v1, v2)
	else:     
		return -1

###################
# call neural networks 
def nerualNets(v2, pList):
	#rpynnet.nnlean(v2)
	print "before neural ...\n"
	
	return ffnetUtil.nnLearn(v2)

####################
# 
def reshapeData(occvals):
	_o = np.array(occvals)
	_length = _o.shape[0]
	col = 24
	row = _length/24 # one hour gap, 24 slots
	a = np.resize(_o, (row,col))

	return a 

####################
# call the svm regression
def svmRegression(v2):
	return svmUtil.svrLearn(v2)


######################
def wirteOutputFile(content, fpath):
	fp = open(fpath, 'a')
	fp.write(content)
	fp.close()



ERR_OUT_AR = 'AR_ERR_OUT.csv'
ERR_OUT_SVM = 'SVM_ERR_OUT.csv'
ERR_OUT_FFNN = 'FFNN_ERR_OUT.csv'
# set a point 
#p1 = [BOUND_UpLeft[0]+step_width,BOUND_UpLeft[1] ];
for m in range(1,10):
	for n in range(10):
		p1 = [BOUND_UpLeft[0]+m*step_width,BOUND_UpLeft[1]+n*step_hight ];

		sortedLots = appendDistCol(p1, LOC_LIST)

		#print sortedLots

		locCapMap = getLotCapDict(LOT_CAP_PATH)

		###############################
		# capapcity loop from 6 to 251  
		for cap in range(6, 251, 10):
			# generate candi list and aggregated volume 
			candidateLots, volume = addpLots(sortedLots, locCapMap, cap)
		
			#print ">>>>>>"
			error = runDateFirstAggregateMeth(candidateLots, REF_DATA_P)
			print "volume - error : ", volume," - ", error 
			strin = str(volume)+','+str(error)+'\r\n'
			wirteOutputFile(strin, ERR_OUT_AR)
			#wirteOutputFile(strin, ERR_OUT_SVM)
			#wirteOutputFile(strin, ERR_OUT_FFNN)
