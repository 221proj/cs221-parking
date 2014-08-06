# reclustering based on 
#
#
import matplotlib.pyplot as plt 
import numpy as np  
import pickle
import rpyAlg
import scipy.cluster.hierarchy as hcluster


fpath2 = "/home/seanqian/Desktop/dev/cs221/repo-221proj/cs221-parking/src/newDEV/classification/top20k2032centroids.pickle"
fpath3 = "/home/seanqian/Desktop/dev/cs221/repo-221proj/cs221-parking/src/newDEV/classification/try3/allk2032centroids.pickle"
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
	#i = 0 
	#for val in labels:
	rpyAlg.runAkmean(labels)
		#i +=1
		#plt.figure()
		#plt.plot(val)
		#plt.show()
		#plt.savefig("centroid_"+str(i)+".png")





def runHierarchy(fpickle):
	centroidsData = getpickleFile(fpickle);
	for i in range(10, 50):
		thresh = float(i/100.0);
		clusters = hcluster.fclusterdata(centroidsData, thresh, criterion='distance', metric='euclidean', depth =2 ) #, metric = 'euclidean', depth=1, method= 'centroid')
		print "threshold : %f, number of clusters %d " % (thresh, len(set(clusters)))
		#print len(set(clusters)
		if len(set(clusters)) < 30: 
			break

	#print clusters.shape	
	#print set(clusters)
	#np.array(clusters)
	ua, indices = np.unique(clusters, return_inverse=True)
	#print ua, indices
	count = np.bincount(indices)
	print count

	mostFreqIdx = np.argmax(count)
	print mostFreqIdx
	freqQ = np.argsort(count)
	print freqQ

	#print freqQ[-1]



	for k in range(1,17):
		a = None
		_c = 0 
		print "----processing: ", k, "---"
		for i, val in enumerate(indices):
		#print i, val 
			if val == freqQ[-k]:
				_c +=1
				if a is None:
					a = centroidsData[i]
				else:
					a = a + centroidsData[i]	
		#print a, _c				
		avg = a/_c
		avgOCC = np.mean(avg)
		avgOCC = round(avgOCC, 4)
		plt.figure()
		plt.plot(avg, 'ro-', linewidth=2.5)
		#plt.title("#"+str(k)+", avg occ: "+ str(avgOCC*100) +"%")

		plt.xlim(0,24)
		#plt.ylim(0,1)
		plt.xlabel("Hour")
		plt.ylabel("Ratio")
		plt.savefig('MostFreq'+str(k)+"DenShape.png")
		print "--- fig generated ---"




runHierarchy(fpath3)
#plotLabelSetHist(fpath3)