### nerual nets util - feed forward ###

# Data and description   
# 

from ffnet import ffnet, mlgraph
import numpy as np 

def nnLearn(v):

	# Generate standard layered network architecture and create network 
	connec = mlgraph((24,48,12,1)) 
	net = ffnet(connec)

	# Read training data/construct the data frame     
	dataframe = None  
	for i in xrange(24, len(v)):
		_r = []
		for j in xrange(1,24):
			_r.append(v[i-j][0])
	
		_r.append(v[i][0])
		#print _r 
		if dataframe is None: 
			dataframe = np.array(_r);
		else:
			dataframe = np.vstack((dataframe, np.array(_r) ))

	#print dataframe.shape			 
	#
	inputTrain = dataframe[:,:24]
	#print inputTrain
	targetVals = dataframe[:,-1]

	print "TRAINING NETWORK..."

	net.train_tnc(inputTrain, targetVals, maxfun = 1000, messages=1)

	print "TESTING NETWORK..." 
	
	output, regression = net.test(inputTrain, targetVals, iprint = 0)
	Rsquared = regression[0][2]
	maxerr = abs( np.array(output).reshape( len(output) ) - np.array(targetVals) ).max()
	print "R-squared:           %s  (should be >= 0.999999)" %str(Rsquared)
	print "max. absolute error: %s  (should be <= 0.05)" %str(maxerr)
	
	return abs( np.array(output).reshape( len(output) ) - np.array(targetVals) ).mean()