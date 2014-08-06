import rpy2.robjects as robjects
from rpy2.robjects import FloatVector
from rpy2.robjects.packages import importr
import array, pickle
import numpy as np 
import matplotlib.pyplot as plt 

stats = importr('stats')
base = importr('base')
akmean = importr('akmeans')
####################################
# code here to call R - package / algorithm 
####################################

def runAkmean(data):

	#print data 
	print "length of data frame ", len(data)

	#return 

	mtx = None
	bigRowVector = None
	for i, r in enumerate(data):
		#print r 
		if bigRowVector == None:
			bigRowVector = r 
		else:
			bigRowVector = np.append(bigRowVector, r)

		#rRow = robjects.FloatVector(r)
		#print "--------\n", rRow

		#print "r vector \n", robjects.FloatVector(bigRowVector)

	
	mtx =  robjects.r.matrix(robjects.FloatVector(bigRowVector), nrow = len(data))	
	robjects.globalenv["x"] = mtx
	print robjects.r("dim(x)")
	ret = robjects.r("result=akmeans(x, max.k=700)")


	robjects.r('''
		label = result$cluster
		vTable = sort(table(label), decreasing=TRUE)
		top20 = vTable[1:20]
		coverage = sum(top20)/length(vTable)
		allcover=vTable/length(label)
		centroids = result$centers 
		corr=cor(t(centroids))
		
		vcorr=c()
		for (i in 1:(length(vTable)-1) ){
			vcorr = c(vcorr, corr[(i+1):length(vTable),i]) 
			}	
		''')

	coverageAllsorted = np.array(robjects.r("allcover"))

	###################################
	# generate correlation matrix 
	corrVector = np.array(robjects.r("vcorr"))
	
	plt.hist(corrVector, bins=100)
	plt.title("Histogram of correlation among cluster centroids")
	plt.xlabel("Correlation")
	plt.ylabel("Frequency")
	
	plt.savefig('fig1hr/histogramCorr.png')

	#raise "*********exception**********"

	centroidSet = []
	for i in range(1,21):
		rcode1 = "labelIndex = names(top20)[%d]" % i
		robjects.r(rcode1)
		robjects.r("idx = as.numeric(labelIndex)")
		centroid = robjects.r("c=centroids[idx,]")
		#print "***", centorid, "---", len(centorid)
		#print "+++++++"
		#print np.array(centorid)

		#break
		centroidSet.append(np.array(centroid))

	coverage = robjects.r("coverage")[0]
	kVal = robjects.r("length(centroids[,1])")[0]

	#################################
	labelSet = robjects.r("label")
	labels = np.array(labelSet)
		
	#################################



	allCentroids = np.array(robjects.r("centroids"))



	with open('top20k'+str(kVal)+'centroids.pickle', 'wb') as handle:
		pickle.dump(centroidSet, handle)	

	with open('allk'+str(kVal)+'labelSet.pickle', 'wb') as handle2:
		pickle.dump(labels, handle2)

	with open('allk'+str(kVal)+'centroids.pickle', 'wb') as handle3:
		pickle.dump(allCentroids, handle3)	

	#print centroidSet
	with open('sortedCoverage.pickle', 'wb') as handle4:
		pickle.dump(coverageAllsorted, handle4)

	print coverage



	#print ret 
	#fitObj = robjects.r(" x = matrix(rnorm(1000), 100, 10)  ")
	#robjects.r("akmeans(x)")

	#labels = ret.rx2("cluster") 
	#centroids = ret.rx2("centers")

	#print "***label***\n", labels
	#print "---centroids---\n", centroids

	raise "*********exception**********"


#########################################
# hierarchy cluster #
#########################################
def hierarchyCluster(k, target, labels, centers):

	objects.r( " hclust(dist(centers)^2, method=\"cen\", ) " )