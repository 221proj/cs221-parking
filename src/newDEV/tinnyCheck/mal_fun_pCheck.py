### this script check the parking lot mal-function###
#
# 
# 
import os, datetime, re
import numpy as np 

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

# for sanity check 
def processSingleFile(pth):
	# print pth
	fp = open(pth, "r")
	dayStack = []
	tc = 0 
	for line in fp:
		_temp = line.split(",")
		ratio = _temp[-1][0:-1]
		r = float(ratio)
		
		tc = max(int(_temp[-2]), tc)

		#print "total cap...",tc, pth[-19:] 
		if r < 0 or r > 1 :
			print r 
			raise ValueError("ratio is out of bound")

		if tc < 0 :
			#print r 
			#print pth[-19:]	# display the file name  
			return tc
			#raise ValueError("the capacity is not valid ")
		dayStack.append(float(ratio))	
	


			

DWK = ["monday", "tuesday", "wendesday","thursday","friday"] 

#test = readInFile(PATH, "monday")
#test = readInFile(PATH, "tuesday")
#test = readInFile(PATH, DWK[4], fault_Lot_pool)

for _d in DWK:
	test = readInFile(PATH, _d, fault_Lot_pool)
	

	

