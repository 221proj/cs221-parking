### this script utilize the svm ###
# 
# For this particular case 
# 
from sklearn.svm import SVR 
import numpy as np 

# n_samples, n_features = 10, 5
# np.random.seed(0)

# x = np.sort(5 * np.random.rand(40, 1), axis=0)
# y = np.sin(x).ravel()

###############################################################################
# Add noise to targets
# y[::5] += 3 * (0.5 - np.random.rand(8))


# y = np.random.randn(n_samples)
# x = np.random.randn(n_samples, n_features)
# classifier 

# clf = SVR(C=1.0, epsilon=0.2)
# svr_rbf = clf.fit(x,y)

# y_rbf = svr_rbf.predict(x)
# print y_rbf
# print "\n***\n"
# print y 
 
# import matplotlib.pyplot as plt 
# plt.figure()
# plt.scatter(x, y)
# plt.plot(x, y_rbf, 'r-')
# plt.show()

def svrLearn(v):
	#print v

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

	clf = SVR()
	clf.fit(inputTrain, targetVals)
	#print clf.predict(inputTrain)-
	errV = np.divide(abs(clf.predict(inputTrain)-targetVals), targetVals)# .max()
	print errV.mean()
	#print errV.max()
	return errV.mean()