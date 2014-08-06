"""
refine raw data file into n-hour gap data file 

"""

import os, datetime

DIR = "../../train/"

OUTPUT_DIR = "../../refineData/"
#TIME_GAP = 3590 # 3600 is 1 hour gap 
TIME_GAP = 890  # 900 is 15 minutes gap 


def filesInDir(dirpath):
    fileList =[]	
    	
    for filename in os.listdir(dirpath):
	filepath = dirpath+str(filename)	
	fileList.append(filepath)
    fileList.sort()

    return fileList	


files = filesInDir(DIR)

#print files

def readLots(lotFList):
    """
    @param, 'lotFlist' are list of lotIDs
    """
    for _path in lotFList:
    	for filename in os.listdir(_path):
    	    #print filename
    	    _filepath = _path + "/" + filename
    	    #print _filepath
    	    readf(_filepath)
    	#break 	
    #break	


def readf(filepath):
    """
    read single file content 
    """
    fp = open(filepath, 'r')

    lastTS = 0

    folderP = filepath.split('/')
    #print folderP[-1]
    appendF = folderP[-1]
    dwPath = OUTPUT_DIR +"15_MIN" +"/"+folderP[-2]
    fwPath = dwPath+"/"+appendF


    for line in fp:
    	#print line 
    	_temp = line.split(',')
    	ts = _temp[0]
    	#print ts
    	ts = ts[1:-1]

    	t = convertTimestampToDayHourMin(ts) 
        #hourly records 
        if (int(ts)-lastTS) > TIME_GAP :
        	print t 
        	lastTS = int(ts) 
        	writeFile(fwPath, dwPath, line)
     



def convertTimestampToDayHourMin(ts):
    """
    the convert Timestamp to (Day, Hour, Min) tuple

    @param ts - string of timestamp
     
    """ 
    if (ts is not None) and ( int(ts) > 100000):
        dateT = datetime.datetime.fromtimestamp(int(ts)) 
        y = dateT.year
        m = dateT.month
        d = dateT.day
    
        dayInWeek = datetime.date(y, m, d).weekday()   
        hourInDay = dateT.hour
        minInHour = dateT.minute  

        return (dayInWeek, y, m, d, hourInDay, minInHour)
    


def writeFile(wTargetPath, dirPath, line):
    
    #if os.path.exists(dirpath):        
    #    print "exist!!"
    #    return os.path.getsize(wTargetPath)
        
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    #if not os.path.exists(wTargetPath):
    #    os.makedirs(wTargetPath)
    #print dirPath
    #print wTargetPath

    fp = open(wTargetPath,'a')
    fp.write(line)
    fp.close()
    
    



readLots(files)


