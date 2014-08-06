import numpy as np




###################################
def runKMeans(k,patches,maxIter):
    tempArray=[]
    for item in patches:
        #print type(item)
        #loc = list(item[0])
        #escalateLoc = [loc[0], loc[1]]
        #tempArray.append(escalateLoc)   # list of all geolocations
        tempArray.append(item)

    #print tempArray

    #raise "not implemented yet"

    trans_patch = np.array(tempArray)
    trans_patch = np.transpose(trans_patch) # n*numPatches, first row is lat, second row is long
    
    # print "trans patch"
    # print trans_patch
    #outputFile(trans_patch)
    #print trans_patch.shape
    
    """
        Runs K-means to learn k centroids, for maxIter iterations.
        
        Args:
        k - number of centroids.
        patches - 2D numpy array of size patchSize x numPatches
        maxIter - number of iterations to run K-means for
        
        Returns:
        centroids - 2D numpy array of size patchSize x k
        """
    # print patches
    # This line starts you out with randomly initialized centroids in a matrix
    # with patchSize rows and k columns. Each column is a centroid.
    
    centroids = trans_patch[:,0:k] #np.random.randn(trans_patch.shape[0],k)
        
    #print centroids
    
    numPatches = trans_patch.shape[1]
    # print numPatches
    
    # patchClusterLabels = collections.Counter()
    patchClusterLabelsV2 = np.zeros(numPatches)     #array to store the cluster label
    
    for i in range(maxIter):
        numCounterInCluster = np.zeros(k)       # initialize the label counter in every iteration
        #print numCounterInCluster

        # find the cluster that each patch belongs to
        for col in range(numPatches):
            _tempDiff = centroids - trans_patch[:,col:col+1]
            _norm = np.sum(_tempDiff*_tempDiff , axis=0)
            _cluster = np.argmin(_norm) # return index          #comment: could merge them together (but error is different)
            
            patchClusterLabelsV2[col] = _cluster
        #print patchClusterLabelsV2
        
        # update centroids
        centroids = np.zeros((trans_patch.shape[0],k))
        for _col in range(numPatches):
            _clusterLabel = patchClusterLabelsV2[_col]
            centroids[:, _clusterLabel:_clusterLabel+1] += trans_patch[:,_col:_col+1]
            numCounterInCluster[_clusterLabel] +=1
        centroids= centroids/numCounterInCluster
    
    #print centroids[1]    
    #print patchClusterLabelsV2 +1   

    # plt.scatter([trans_patch[0]], [trans_patch[1]], 55, patchClusterLabelsV2+1,)    
    return centroids  


###############################
# calucate summation of Euclidean Distance
def errorKMeans(k,patches,centroids):
    tempArray=[]
    for item in patches:
        tempArray.append(item)

    #print tempArray

    #raise "not implemented yet"

    trans_patch = np.array(tempArray)
    trans_patch = np.transpose(trans_patch) # n*numPatches, first row is lat, second row is long
    
    # print "trans patch"
    # print trans_patch
    #outputFile(trans_patch)
    #print trans_patch.shape
    
    """
        Runs K-means to learn k centroids, for maxIter iterations.
        
        Args:
        k - number of centroids.
        patches - 2D numpy array of size patchSize x numPatches
        maxIter - number of iterations to run K-means for
        
        Returns:
        centroids - 2D numpy array of size patchSize x k
        """
    # print patches
    # This line starts you out with randomly initialized centroids in a matrix
    # with patchSize rows and k columns. Each column is a centroid.
    
    centroids = trans_patch[:,0:k] #np.random.randn(trans_patch.shape[0],k)
        
    #print centroids
    
    numPatches = trans_patch.shape[1]
    # print numPatches
    
    # patchClusterLabels = collections.Counter()
    patchClusterLabelsV2 = np.zeros(numPatches)     #array to store the cluster label
    
    #for i in range(maxIter):
    #numCounterInCluster = np.zeros(k)       # initialize the label counter in every iteration
        #print numCounterInCluster

        # find the cluster that each patch belongs to
    for col in range(numPatches):
        _tempDiff = centroids - trans_patch[:,col:col+1]
        _norm = np.sum(_tempDiff*_tempDiff , axis=0)
        _cluster = np.argmin(_norm) # return index          #comment: could merge them together (but error is different)
            
        patchClusterLabelsV2[col] = _cluster
        #print patchClusterLabelsV2
        
        # find Euclidean distance between data point and cluster 
    euclideanDist = np.zeros(numPatches)
        
    for _col in range(numPatches):
        _clusterLabel = patchClusterLabelsV2[_col]
        _currentCentroid = centroids[:, _clusterLabel:_clusterLabel+1]
        _currentPatch = trans_patch[:, _col:_col+1]

        _diff = _currentPatch - _currentCentroid
        euclideanDist[_col] = sum(_diff*_diff)
    
    #print euclideanDist

    #print "++++++++++++++++", sum(euclideanDist)

    #normEuclid = euclideanDist/np.sum(euclideanDist)
    
    #print "----------------", sum(normEuclid)
    
    #print np.average(normEuclid)
    #print "<>"
    #print np.average(euclideanDist) 

    return np.average(euclideanDist)    


def generateLabel(patch, centroids):
    #print centroids.shape
    """
    num of k == centorids.shape[1]
    """

    numCluster = centroids.shape[1]
    
    transPatch = patch.reshape((len(patch),1))  # translate row vector into column vector 
    
    label = None
    minnorm = 999999
    for _col in range(numCluster):
        #print centroids[:, _col:_col+1].shape
        _currentCentroid = centroids[:, _col:_col+1]
        #print patch[:,]

        a = np.subtract(transPatch, _currentCentroid)
        #print a.shape 
        val = np.linalg.norm(a)
        if label is None:
            label = _col
            minnorm = val
        elif val < minnorm:
            label = _col 
            minnorm = val

    return label           