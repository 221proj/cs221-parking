# the file convert raw data into
# n min gap of occupancy data type

import os, datetime  

DIR = "../../refineData/WeekDay/"

OUTPUT_DIR = "../../refineData/WeekDay/OCC/"
TIME_GAP = 3590 # 3600 is 1 hour gap 
#TIME_GAP = 890  # 900 is 15 minutes gap 

def readLots(fpath, desc):
	"""
	@param, 'lotFlist' are list of lotIDs
	"""
	pth = fpath +desc+"/"

	fileList =[]	
		
	for filename in os.listdir(pth):
		filepath = pth+str(filename)	
		fileList.append(filepath)
		fileList.sort()

	
	readFiles(fileList, desc)


	#return fileList	


def readFiles(lotFList, desc):
	for _path in lotFList:
		for filename in os.listdir(_path):
			#print filename
			_filepath = _path +"/"+ filename
			#print _filepath
			readf(_filepath, desc)
		#break 	





def readf(filepath, desc):
	"""
	read single file content 
	"""
	fp = open(filepath, 'r')

	lastTS = 0

	folderP = filepath.split('/')
	#print folderP[-1]
	appendF = folderP[-1]
	dwPath = OUTPUT_DIR +"1_Hr/"+desc +"/"+folderP[-2]
	fwPath = dwPath+"/"+appendF

	operSum = 0 
	occSum = 0
	iCount = 0
	oCount = 0
	for line in fp:
		#print line
		iCount +=1  
		_temp = line.split(", ")
		ts = _temp[0]
		#print ts
		ts = ts[1:-1]
		occn = _temp[2][1:-1];
		opern = _temp[3][1:-1];
		   
		operSum += int(opern) 
		occSum += int(occn)
		oCount += 1
		#t = convertTimestampToDayHourMin(ts) 
		#hourly records 
		#print ts
		#print occn, opern, float(occSum)/float(operSum)
		#print oCount
		if operSum <= 0 or occSum < 0:
			occRatio = 0
		elif operSum <= occSum: 
			occRatio = 1.0 	
		else:
			#print occSum, operSum
			occRatio = float(occSum)/float(operSum)

		#print occn, opern, occSum, operSum, occRatio

		if (int(ts)-lastTS) > TIME_GAP :
			 
			lastTS = int(ts)
			#print occSum, operSum
			if occRatio < 0 or occRatio > 1:
				print occRatio
				print line
				print "\nerror in file ", filepath
				raise NotImplementedError(" ratio out of bound...") 

			l = ts+","+occn + "," + opern + "," + str(occRatio)+"\n"; 
			writeFile(fwPath, dwPath, l)
			occSum = 0
			oCount = 0 
			operSum = 0

	print "reformating file - ", filepath, "...done!"		



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


description = ["monday", "tuesday", "wendesday", "thursday", "friday"]

for v in description:
	#readLots(DIR, "monday")
	readLots(DIR, v)