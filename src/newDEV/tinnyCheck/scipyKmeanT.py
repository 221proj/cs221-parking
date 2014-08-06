from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq, kmeans2
import numpy as np 

# data generation
data = vstack((rand(150,2) + array([.5,.5]),rand(150,2)))

print data.shape  

# print data

s = np.sum(data, axis=1)

print s.shape
x = data 
for i in range(data.shape[0]):
	x[i,:] = data[i,:]/s[i];

# print x 
print np.sum(x, axis =1) 
# for i in len(data.shape[0]):
# 	data

"""
# computing K-Means with K = 2 (2 clusters)
centroids,_ = kmeans(data,2)
# assign each sample to a cluster
idx,_ = vq(data,centroids)

# some plotting using numpy's logical indexing
plot(data[idx==0,0],data[idx==0,1],'ob',
     data[idx==1,0],data[idx==1,1],'or')
plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
show()
"""
# # now with K = 3 (3 clusters)
# centroids,_ = kmeans2(data,3)
# idx,_ = vq(data,centroids)

# print centroids
# print centroids.shape

# plot(data[idx==0,0],data[idx==0,1],'ob',
#      data[idx==1,0],data[idx==1,1],'or',
#      data[idx==2,0],data[idx==2,1],'og') # third cluster points
# plot(centroids[:,0],centroids[:,1],'sm',markersize=8)
# show()

"""
from scipy.spatial.distance import cdist,pdist
from matplotlib import cm
import numpy as np 

K_MAX = 20
KK = range(1,K_MAX+1)

KM = [kmeans(data,k) for k in KK]
centroids = [cent for (cent,var) in KM]
D_k = [cdist(data, cent, 'euclidean') for cent in centroids]
cIdx = [np.argmin(D,axis=1) for D in D_k]
dist = [np.min(D,axis=1) for D in D_k]


tot_withinss = [sum(d**2) for d in dist]  # Total within-cluster sum of squares
totss = sum(pdist(data)**2)/data.shape[0]       # The total sum of squares
betweenss = totss - tot_withinss   

##### plots #####
kIdx = 9        # K=10
clr = cm.spectral( np.linspace(0,1,10) ).tolist()
mrk = 'os^p<dvh8>+x.'


from matplotlib import pyplot as plt
# elbow curve
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(KK, betweenss/totss*100, 'b*-')
ax.plot(KK[kIdx], betweenss[kIdx]/totss*100, marker='o', markersize=12, 
    markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
ax.set_ylim((0,100))
plt.grid(True)
plt.xlabel('Number of clusters')
plt.ylabel('Percentage of variance explained (%)')
plt.title('Elbow for KMeans clustering')

plt.show()
"""
