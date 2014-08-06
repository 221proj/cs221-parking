import scipy.cluster.hierarchy as hcluster
#import numpy.random as random 
import numpy as np 
import matplotlib.pyplot as plt 
import util




"""
data = random.randn(2,200)

data[:100, :100] += 10

print data.shape 
for i in range(1, 15):
	thresh = i/10;
	clusters = hcluster.fclusterdata(np.transpose(data), 0.6, criterion='distance' ) #, metric = 'euclidean', depth=1, method= 'centroid')
	print "threshold : %f, number of clusters %d " % (thresh, len(set(clusters)))

print clusters.shape
print clusters	
"""

CenPath = "/home/seanqian/Desktop/dev/cs221/repo-221proj/cs221-parking/src/profileSegment/" 
centroidsData = util.getpickleFile("allk524centroids.pickle")
#print centroids.shape

for i in range(80, 110):
	thresh = float(i/100.0);
	clusters = hcluster.fclusterdata(centroidsData, thresh, criterion='distance', metric='euclidean', depth =2 ) #, metric = 'euclidean', depth=1, method= 'centroid')
	print "threshold : %f, number of clusters %d " % (thresh, len(set(clusters)))
	#print len(set(clusters)
	if len(set(clusters)) < 150: 
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
	plt.title("#"+str(k)+", avg occ: "+ str(avgOCC*100) +"%")
	plt.xlim(0,24)
	plt.ylim(0,1)
	plt.xlabel("Hour")
	plt.ylabel("Occupancy ratio")
	plt.savefig('MostFreq'+str(k)+"DenShape.png")
	print "--- fig generated ---"