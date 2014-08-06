import matplotlib.pyplot as plt 
import numpy as np  
import pickle


fpath = "/home/seanqian/Desktop/dev/cs221/repo-221proj/cs221-parking/src/newDEV/classification/allk720centroids.pickle"

fpath2 = "/home/seanqian/Desktop/dev/cs221/repo-221proj/cs221-parking/src/newDEV/classification/top20k2032centroids.pickle"
fpathLabel = "/home/seanqian/Desktop/dev/cs221/repo-221proj/cs221-parking/src/newDEV/classification/sortedCoverage.pickle"
fpath3 ="/home/seanqian/Desktop/dev/cs221/repo-221proj/cs221-parking/src/newDEV/classification/top20k1136centroids.pickle"
# plot 
##########################
# read pickle file 
##########################
def getpickleFile(fname):
	with open(fname, 'rb') as handle:
		b = pickle.load(handle)

	return b


def plotLabelSetHist(fpickle):
	labels = getpickleFile(fpickle)
	#print labels[:21];

	#for val in labels:
		
	#print val 
	i = 0 
	for val in labels:
		i +=1
		plt.figure()
		plt.plot(val)
		#plt.show()
		plt.savefig("centroid_"+str(i)+".png")




plotLabelSetHist(fpath3)

#plotLabelSetHist(fpathLabel)	