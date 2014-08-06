# This file classify the data into several groups 
# 
# @since 04/22/2014
# 

import os
import numpy as np
import matplotlib.pyplot as plt
import rpyAlg  


thr15 = 67 
thr60 = 18

path = "../../../refineData/WeekDay/OCC/15_MIN/" 
path2 = "../../../refineData/WeekDay/OCC/1_Hr/"

def readInFile(pth, desc):
	lotStack = None;
	fpth = pth + desc +"/"
	for val in os.listdir(fpth):
		lotFpth = fpth+val+"/"
		#if len(val) < 5:
		#	continue
		lotM = readInLot(lotFpth)		
		#print lotFpth 		

		if lotM is not None:
			if lotStack is None:    
				lotStack = lotM   
			else: 
				lotStack = np.vstack((lotStack, lotM))		
	
	#print lotStack	
	
	return lotStack
	


def readInLot(pth):
	#print pth
	# process each ren
	#plt.figure()
	vecStack = None; 
	for val in os.listdir(pth):
		spth = pth+val 
		vec = processSingleFile(spth)
		
		if vec is not None:
			
			#plt.plot(vec)

			if vecStack is None:    
				vecStack = vec   
			else: 
				vecStack = np.vstack((vecStack, vec))		
	
	#print vecStack.shape
	#plt.show()

	#rows = vecStack.shape[0]
	#if rows < 20:
	if vecStack is None: 
		print pth 
		#print vecStack
	#print vec 
	#	print vecStack.shape

	return vecStack

def processSingleFile(pth):
	#print pth
	fp = open(pth, "r")
	dayStack = []
	for line in fp:
		_temp = line.split(",")
		ratio = _temp[-1][0:-1]
		r = float(ratio)
		if r < 0 or r > 1 :
			print r 
			raise NotImplementedError("...wrong ratio")
		dayStack.append(float(ratio))
	

	# check if there is enough data entry	
	if len(dayStack)> thr60:
		a = np.array(dayStack)
		#print np.sum(a) 
		a_N = a/np.sum(a)
		#print a_N
		#print len(a)
		if sum(dayStack) < 0.1:
			#print dayStack
			return None	

		return a_N 
	else:
		print "insufficient data..."	
		return None
	



	
occMatrix = readInFile(path2, "monday")


def runClassify(m):
	rpyAlg.runAkmean(m)

runClassify(occMatrix)	