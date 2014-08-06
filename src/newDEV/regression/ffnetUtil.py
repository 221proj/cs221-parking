### nerual nets util - feed forward ###

# Data and description   
# 

from ffnet import ffnet, mlgraph
import numpy as np 

def nnLearn(v, vTest):

	# Generate standard layered network architecture and create network 
	connec = mlgraph((24,48,12,1)) 
	net = ffnet(connec)
	# print "begin learning nerual nets...."


	# Read training data/construct the data frame     
	dataframe = None  
	for i in xrange(24, len(v)):
		_r = []
		for j in xrange(1,24):
			_r.append(v[i-j])
	
		_r.append(v[i])
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
	Rsquared = regression[0][2]	# R-squared 
	maxerr = abs( np.array(output).reshape( len(output) ) - np.array(targetVals) ).max()
	print "R-squared:           %s  (should be >= 0.999999)" %str(Rsquared)
	print "max. absolute error: %s  (should be <= 0.05)" %str(maxerr)
	
	######################
	## start test ##
	dataframeV2 = None;

	print "test new items ...... length of vector Test", len(vTest)
	for i in xrange(24, len(vTest)):
		_r = [];
		for j in xrange(1,24):
			print vTest[i-j]
			_r.append(vTest[i-j])
		
		_r.append(vTest[i])

		print "check dat structure",_r 
		if dataframeV2 is None: 
			dataframeV2 = np.array(_r);
		else:
			dataframeV2 = np.vstack((dataframeV2, np.array(_r) ))

	inputTest = dataframeV2[:,:24]
	targetTestVals = dataframeV2[:,-1]
			
	print "2 test new items ......"		
	output2, regression2 = net.test(inputTest, targetTestVals, iprint = 0)		
	#############
	RsquaredTest = regression2[0][2]
	print "R-squared test:   %s " % str(RsquaredTest)


	############################
	# training error #
	############################
	trainErr = abs( np.array(output).reshape( len(output) ) - np.array(targetVals) ).mean()
	testErr = abs( np.array(output2).reshape( len(output2) ) - np.array(targetTestVals) ).mean()
	# testErr = None;
	# return abs( np.array(output).reshape( len(output) ) - np.array(targetVals) ).mean()
	return (trainErr, testErr)