# before runing the aggregation
# extract the nearby lots according to (lat, lng) input  
# 
import math, os, datetime
import numpy as np

#print setp_hight, setp_width

##################################
# private functions - internal call
#
#####################################
#
fault_Lot_pool_id = [359051, 202001, 701022, 549201,720241, 720052]

#########################
#
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
# generated capacity map 
LOT_CAP_PATH = '../LOT_CAP.txt';
#####################################

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
# "../cs221-parking/idLocation/helloLocation.txt" 
LOCATION_ID_PATH = '../../../idLocation/helloLocation.txt'
#####################################

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

# generate lot list - a static unsorted map
def getLocListMap(pth): 
	LOC_LIST = genLocMap(pth)
	return LOC_LIST
# 


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
	# print _m
	print "***************"
	r, c = _m.shape
	# print _m[_m[:, c-1].argsort()];

	return _m[_m[:,c-1].argsort()]

#######
# add more parking lot based on sorted list and the threshold 
# 
#######
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
		if _id in fault_Lot_pool_id: 
			i=i+1
			continue
			 
		capV = capMap[_id]
		if capV > 0 and _id > 1000:
			aggV = aggV+capV
			nearbyLots.append(_id)
		
		i = i+1

	return (nearbyLots, aggV)	

###################################
# public part 
# 
##########################
#1. load lot capacity map
#2. pass in (lat, lng) to sort the parking locations
#3. aggregate up to 150 
#4. generate the matrix   


# public function allowing other script to call following func
def generateSortedLot(pos, thres):
	# read in the unsorted map 
	unsort_lotlistMap = getLocListMap(LOCATION_ID_PATH);
	sortedLots = appendDistCol(pos, unsort_lotlistMap)
	
	# generated capacity map 
	# LOT_CAP_PATH = '../LOT_CAP.txt';
	locCapMap = getLotCapDict(LOT_CAP_PATH)
	
	# get list of sorted candidate lots , togethor with its total volume of capacity

	sLotCandi, tv = addpLots(sortedLots, locCapMap, thres)

	# print sLotCandi, unsort_lotlistMap
	# for j in xrange(len(sLotCandi)):
	# 	for i in xrange(unsort_lotlistMap.shape[0]):
	# 		LotID = int(unsort_lotlistMap[i,0:1]);
	# 	# print LotID
		
	# 		if int(sLotCandi[j]) == LotID:
	# 			_lotGeo = [unsort_lotlistMap[i,1], unsort_lotlistMap[i,2]];
	# 			# print LotID,unsort_lotlistMap[i,1:3];
	# 			# break
	# 			_distance = calculateDistance(pos, _lotGeo);
	# 			print _distance, _lotGeo		
	# print _distance;


	# raise NotImplementedError("...manully break...");

	return (sLotCandi,tv)

##################
# update addparkLotGarage(sortedLots, locCapMap, thres)
##################
def addpLotsGarage(sLotList, capMap, threshold):
	"""
	sLotList - sorted Lot list -- is 2d nparray, 
	capMap - dictionary, key is lotID, val is capacity
	"""
	try:
		m, n = sLotList.shape
	except:
		m = len(sLotList)

	i = 0
	aggV = 0;

	nearbyLots = []; 
	while i < m and aggV < threshold:

		_id = sLotList[i,0:1] 
		_id=int(_id)
		#print int(_id)
		if _id in fault_Lot_pool_id: 
			i=i+1
			continue
			 
		capV = capMap[_id]
		if capV > 0 :
			aggV = aggV+capV
			nearbyLots.append(_id)
		
		i = i+1

	return (nearbyLots, aggV)	


##################################
## update generate sorted lots 
##################################

def generateSortedLotWithGarage(pos, thres, distanceCheck=0.6):

	unsort_lotlistMap = getLocListMap(LOCATION_ID_PATH);
	sortedLots = appendDistCol(pos, unsort_lotlistMap)
	
	# generated capacity map 
	# LOT_CAP_PATH = '../LOT_CAP.txt';
	locCapMap = getLotCapDict(LOT_CAP_PATH)

	sLotCandi, tv = addpLotsGarage(sortedLots, locCapMap, thres);	# sLotCandi -- sorted lot candidates

	endIdx = len(sLotCandi);
	# get list of sorted candidate lots , togethor with its total volume of capacity
	for j in xrange(len(sLotCandi)):
		for i in xrange(unsort_lotlistMap.shape[0]):
			LotID = int(unsort_lotlistMap[i,0:1]);
			if int(sLotCandi[j]) == LotID:
				_lotGeo = [unsort_lotlistMap[i,1], unsort_lotlistMap[i,2]];
				_distance = calculateDistance(pos, _lotGeo);
				# print _distance
				if _distance > distanceCheck:	# radius 0.65 mile is walking distnace... 
					endIdx = j;
					break;
	
	# print sLotCandi, tv;
	filterdLots, totV = addpLotsGarage(sortedLots[:endIdx],locCapMap, 999)				
	# print filterdLots, totV;
	
	return (filterdLots,totV)




########################
## update - add distance check when doing aggregation
def generateSortedLotV2(pos, thres, distanceCheck = 0.65):
	unsort_lotlistMap = getLocListMap(LOCATION_ID_PATH);
	sortedLots = appendDistCol(pos, unsort_lotlistMap)
	
	# generated capacity map 
	# LOT_CAP_PATH = '../LOT_CAP.txt';
	locCapMap = getLotCapDict(LOT_CAP_PATH)
	
	# get list of sorted candidate lots , togethor with its total volume of capacity

	sLotCandi, tv = addpLots(sortedLots, locCapMap, thres)

	endIdx = len(sLotCandi);
	# get list of sorted candidate lots , togethor with its total volume of capacity
	for j in xrange(len(sLotCandi)):
		for i in xrange(unsort_lotlistMap.shape[0]):
			LotID = int(unsort_lotlistMap[i,0:1]);
			if int(sLotCandi[j]) == LotID:
				_lotGeo = [unsort_lotlistMap[i,1], unsort_lotlistMap[i,2]];
				_distance = calculateDistance(pos, _lotGeo);
				# print _distance
				if _distance > distanceCheck:	# radius 0.65 mile is walking distnace... 
					endIdx = j;
					break;
	
	# print sLotCandi, tv;
	filterdLots, totV = addpLots(sortedLots[:endIdx],locCapMap, 999)				
	# print filterdLots, totV;
	
	return (filterdLots, totV)