import util, configSFpark
import matplotlib.pyplot as plt 
import numpy as np  

def plotLabelSetHist(fpickle):
	labels = util.getpickleFile(fpickle)
	#dictionary = dict((i, labels.count(i)) for i in labels)
	#hist, bins = np.histogram(labels, bins=1000)

	ua, uid = np.unique(labels, return_inverse=True)
	count = np.bincount(uid)	
	"""
	print "-----\n", uid 
	print ua
	print "-----"
	print count 
	"""
	hist, bins = np.histogram(count, bins=100)


	#center = (bins[:-1] + bins[1:]) / 2
	width = 0.7
	#print len(labels)
	#print len(hist)
	#print sum(hist)
	

	#np.histtogram 
	#print bins 
	plt.hist(count, bins=25)
	plt.xlabel("Cluster size")
	plt.ylabel("Frequency")
	#plt.bar(hist, align='center', width = width)
	#plt.show()
	#plt.figure()
	plt.savefig('histClusterSize1Hr.png')

	#print len(labels)



plotLabelSetHist("labelSet.pickle")