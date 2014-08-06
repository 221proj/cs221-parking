import util, os, datetime, math
import numpy as np

import pickle 
from collections import Counter 

import matplotlib.pyplot as plt


from FilterUtil import *

"""
This file generate multiple time plot 


"""

#DIR_PATH = "../train/";
DIR_PATH = "../refineData/1_HOUR/"
LOCATION_PROFILE_PATH = "../idLocation/"

START_TIME = "00:01"
END_TIME = "23:59"


CENTROIDS = [[  37.80674047,   37.75915639,   37.77783732,   37.79128318,   37.78229867,
    37.79388065,   37.79965323,   37.78684646],
 [-122.41744638, -122.42047599, -122.42060377, -122.40172484, -122.39375636,
  -122.39602712, -122.43842723, -122.43269398]]


#####################################
"""
location near Pier39 
"""
OPTIONAL_LOC1_Pier39 = [ [37.806885,   37.807241,  37.807012, 37.806215 ], \
                 [-122.418918,  -122.415624,  -122.412202, -122.416804]  \
                 ]

#####################################
"""
location near Lombard St 
"""
OPTIONAL_LOC2_LombardST  = [ [37.79973, 37.799434,37.800158 ], \
                   [-122.436386, -122.439517 ,-122.441418]  \
                 ]
"""
location near Financial District 
"""
OPTIONAL_LOC3_FinDist =[ [ 37.789709, 37.794728, 37.792524, 37.797441, 37.794542, 37.791829 , 37.788743], \
                    [-122.403924, -122.400233, -122.399804,-122.402036,-122.404541,-122.404114,-122.405208 ]]


"""
location near bush & webuster
"""
OPTIONAL_LOC4_BW = [ [37.78608, 37.785215,  37.789947, 37.786267, 37.781468], \
                    [-122.433026, -122.433252 ,-122.434069,-122.43158,-122.432395 ] ]


"""
location near city hall 
"""
OPTIONAL_LOC5_CITYHALL = [[37.781756,37.78218, 37.779823, 37.780247,37.778093,37.77872 ,37.777533,37.77565 ] , \
                         [-122.42231,-122.419027,-122.421967,-122.418576,-122.421645,-122.416624,-122.417954,-122.421151] ]


"""
location south market st main & howard
"""
OPTIONAL_LOC6_MAINH = [ [37.791295, 37.792533, 37.789201, 37.790031, 37.788047, 37.788556,37.786793,
    37.786148, 37.781434,37.78296, 37.780857] , \
                        [-122.395872,-122.394059,-122.393373,-122.390939 ,-122.393449,-122.396003,-122.398213,
    -122.401864,-122.400448,-122.39371,-122.396242 ]]

"""
location coast pier52 
"""
OPTIONAL_LOC7_P52 = [[37.770579,37.767785] , [-122.389597,-122.390899 ] ]


"""
location MISSION district 
"""

OPTIONAL_LOC8_MissionDist = [[37.765032 ,37.763421,37.758773,37.75331,37.760215 ], \
                            [-122.420167,-122.419561,-122.419073,-122.418576 , -122.420507]] 

############################################

def readDir(dirpath):
    fileList =[]	
    	
    for filename in os.listdir(dirpath):
	filepath = dirpath+str(filename)	
	fileList.append(filepath)
    fileList.sort()

    return fileList			
 
############################################

def calculateDistance(loc1, loc2, unit='mile'):
    """
    Calculating the distance between the location1 and location2 
    show the distance 
    @param loc1, loc2 - tuple (lat, lng)

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

####################################


"""
###############################################
def isInTimeSlot(line, st, et):
    if type(line) is not str:
        raise "incorrect input "
	_tempList = line.split(',') 
        #print _tempList[0] 	    	
	ts_record = _tempList[0].strip("\"")	# current record's time stamp
	day, hr, minute = convertTimestampToDayHourMin(ts_record)
    
    # convert each record time stamp to min format 
    rec_format_mm_day = int(hr)*60 + int(minute)          # first few elements should be around midnight so hr == 0
    # input of st, et should be xx:xx 
    st_hh, st_mm = st.split(':')    
    et_hh, et_mm = et.split(':')

    st_format_mm_day = int(st_hh) * 60 + int(st_mm) 
    et_format_mm_day = int(et_hh) * 60 + int(et_mm)

    #print rec_format_mm_day, st_format_mm_day, et_format_mm_day

    if rec_format_mm_day >= st_format_mm_day and rec_format_mm_day <= et_format_mm_day:
        return True
    else:
        return False     
"""

def isValidTimeRecord(line):
    if type(line) is not str:
        assert "non valid input string"

        




#################################################
# run the script to extract the list of files first 
################################################
allLotLevelDir = readDir(DIR_PATH)


###############################################
# read the location profile
def checkLocation(loc, distance = 0.01):
    
    locationDict = dict() 

    fp = open(LOCATION_PROFILE_PATH+"helloLocation.txt", 'r')    
    for line in fp:
        _str = line.strip("\(|\)|\r|\n")
        _tempList = _str.split(', ')  
            
        offStreetID = _tempList[1].strip("\'") 
        onStreetID = _tempList[2].strip("\'") 

        if int(offStreetID) > 0:        
            locationDict[str(offStreetID)] = ( _tempList[3].strip("\(|\'"), _tempList[4].strip("\'") ) 
            
        elif int(onStreetID) > 0:
            locationDict[str(onStreetID)] = ( _tempList[3].strip("\(|\'"), _tempList[4].strip("\'") )
        

    fp.close()

    #print locationDict 
    def filterNearByLot(loc, locationDict, radius):
        candidates = []
        lat1, lng1 = loc  
        #print lat1, lng1
        for key, val in locationDict.items():
            lat2, lng2 = val
            #print val  
            if calculateDistance( (float(lat1), float(lng1) ) , (float(lat2), float(lng2) ) ) <= radius: 
                candidates.append(key)

        return candidates
    
    nearbyLotList = filterNearByLot(loc, locationDict, distance)

    return nearbyLotList


# then loop over all the sub directory that has each date file  


def runprogram(lat1, lng1, decp='NA'):
    #######################################################
    # radius range
    radiusSt = 5
    radiusEnd = 20

    startD = "07/07/2013"
    endD = "09/10/2013"
    # get candidate lots 
    aggregationStd = []
    aggregationCap = []

    # mission market (Centroid[0][1], Centroid[1][1])
    # pier 39 (Centroid[0][0], Centroid[1][0])
    # AT&T park (Centroid[0][4], Centroid[1][4] )


    for i in xrange(radiusSt, radiusEnd, 1):          #work around mile radius from 0.07 to 0.41
        #candiLots = checkLocation((CENTROIDS[0][7], CENTROIDS[1][7]), float(i)*0.01)     
        """
        # highlight here 
        candiLots = checkLocation((OPTIONAL_LOC2_LombardST[0][2], OPTIONAL_LOC2_LombardST[1][2]), float(i)*0.01)
        """

        candiLots = checkLocation((lat1, lng1), float(i)*0.01)
        #_std, aggreCap = runFiltering(allLotLevelDir, candiLots)


        ##########################################
        # init a class to filter out the data 
        #######################################
        # Filter is the class that we call from FilterUtil
        filter = Filter(DIR_PATH)
        #print candiLots
        filter.setDistance( float(i)*0.01)
        filter.setDescription(decp)
        candi_L = filter.takeInCandidateLots(candiLots)
        print candi_L
        filter.setDateSpan(startD, endD)
        filter.setHourSpan(START_TIME, END_TIME)
        #filter.runAggregatedOCC(candi_L, 2,0)       # runAggregatedOCC(lot_list, dayFirst, lotFirst )


        filter.runAggregatedOCC(candi_L, 0,0,1)
        print "in main script"
    


    #if len(candiLots) > 0 :
    #    break
    #aggregationStd.append(_std)
    #aggregationCap.append(aggreCap)
    
#############################################################
# edit - 02/02/2013
#############################################################
for i in range(len(OPTIONAL_LOC8_MissionDist[0])):
    runprogram(OPTIONAL_LOC8_MissionDist[0][i],OPTIONAL_LOC8_MissionDist[1][i], str('MISSNDist'+str(i)) )




"""


# print candLots

xAxis = [i*0.01 for i in xrange(radiusSt, radiusEnd, 1)]
yAxis = aggregationStd
yPAxis = aggregationCap

print xAxis
print yAxis
print yPAxis
plt.figure()
plt.plot(xAxis, yAxis) 
plt.ylabel('standard deviation')
plt.xlabel('distance (radius)')
plt.title(START_TIME + ' - ' + END_TIME)

########################################################

plt.figure()
plt.plot(yPAxis, yAxis) 
plt.ylabel('standard deviation')
plt.xlabel('spot accumulation')
plt.title(START_TIME + ' - ' + END_TIME)

plt.show()

"""


#####################################
# run filter-out the near by lots - aggregation 

#runFiltering(allLotLevelDir, candiLots)
#runFiltering(allLotLevelDir)

	
'''
for i, val in enumerate(a):
    readSingleFile(val)
		
    break	
'''



"""

Pier39 [0][0]
City Hall [2][2]
Att park [4][4]


"""






