# read file and aggregate several data
# 
# 
# 

import numpy as np 
import matplotlib.pyplot as plt 
import os 
from collections import Counter

################
PATH = '../../refineData/1_HOUR/'

#
def readinPIDs(path):
	# read from the data path to extract the parking lot IDs
	pIDs = [] 
	for fname in os.listdir(path):
		pIDs.append(fname);

	return sorted(pIDs)	
	#return pIDs


# 
def pIDsubset(pool, i, j):
	#select some parking lots from the pool
	pIDset = []; 
	for k in range(i, j):
		pIDset.append(pool[k]);

	return pIDset;	

def process(pth, pset):
	pIDsdata = None#Counter();
	totalCap = 0 
	for i, val in enumerate(pset):
		#print pth+val
		fpth = pth+val+"/"
		pdlist = readinPIDs(fpth)
		pdat = pIDsubset(pdlist, 14, 18)
		#print pdat
		# loop through all date 
		dataset = None;
		for i, value in enumerate(pdat):
			f  = fpth+value
			arr, cap = readsingleFile(f)
			#print arr.shape
			if(arr.shape[0] == 24):
				if dataset is None:
					dataset = arr;
				else: 
					dataset = np.hstack((dataset, arr))	
		
		dataset = dataset*cap;
		totalCap += cap;
		if pIDsdata is None :
			pIDsdata = dataset;
		else:
			pIDsdata = pIDsdata + dataset 

		#dataset = np.append(dataset, cap)
		#print dataset#.shape
	#print (dataset, cap)
	#print pIDsdata
	#rint totalCap
	aggOCCR = pIDsdata/totalCap
	
	plt.figure()
	plt.plot(aggOCCR, linewidth=2)
	plt.ylim(0,1)
	plt.xlabel(str(len(pset))+" parking lot, " +str(totalCap) + " spots")
	#plt.show()
	print "save figure..."
	plt.savefig(str(len(pset))+'_lots.png', transparent=False, bbox_inches='tight', pad_inches=0)
	print str(len(pset))+'_lots '+ "...done"
	#

def readsingleFile(path):
	occArray = [];
	cap = 0;
	fp = open(path,'r')
	for line in fp:
		#print line
		_t = line.split(", ");
		#print _t[2], _t[3]
		oper = _t[3][1:-1];
		occ = _t[2][1:-1];
		#print oper, occ
		cap = max(int(oper), cap)
		if(int(oper) == 0):
			occr = 0 
		else:
			occr = float(occ)/float(oper);	

		#print occr 
		occArray.append(occr)

	fp.close()	

	return (np.array(occArray), cap)



def run(pth):
	for i in range(11, 51, 5):
		pSet = readinPIDs(pth)
		pSubset = pIDsubset(pSet, 10, i);
		process(pth, pSubset);

	#return pSubset;

#print run(PATH)	
run(PATH)
