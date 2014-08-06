# this script show 

import pickle
from datetime import datetime
import numpy as np 

#############
import matplotlib.pyplot as plt 
#############
import pandas as pd 
####################
# stats model 
import statsmodels.formula.api as smf 
####################
import statsmodels.api as sm 



FILE_PATH = '../regression/interim/ATTocc2.p'
# this function show load the pickle file stored with dictionary
# 
def readpickleFile(path):
	print path
	with open(path, 'rb') as handle:
		b = pickle.load(handle)

	return b 	

TSseries = readpickleFile(FILE_PATH)


def reconstruct(dat):
	print ":: inside the reconstruction ::"
	vals = None	# occupancy values 
	catHvals = None # categorical hour index 
	catWeekday = None # categorical day index 

	for k, v in dat.items():
		weekday = identifyDayOfWeek(k)		
		cateHour = np.linspace(0,23,24)  # categorical data 
		# print np.ones(24)*weekday
		# print v 
		# print cateHour
		if np.ndarray.min(v) <= 0.05: 
			continue

		if vals is None:
			vals = v
			catHvals = cateHour
			catWeekday = np.ones(24)*weekday			
		else:
			vals = np.append(vals, v)		
			catHvals = np.append(catHvals, cateHour)
			catWday = np.ones(24)*weekday;
			catWeekday = np.append(catWeekday, catWday)

	# X = np.c_[v[0], cateHour, np.ones(24)*weekday];
	y_true = vals[1:]
	X = np.c_[y_true, vals[:-1], catHvals[1:], catWeekday[1:]]
	# y_true = vals[1:]
	# print len(X[:,0]), len(X[:,1]), len(X[:,2])
	print X.shape
	dframe = pd.DataFrame({ 'y_true': X[:,0], 'preHour': X[:,1], 'HourIdx': X[:,2], 'weekOfday': X[:,3]})
	# print dframe.preHour

	result = smf.ols(formula='y_true ~ preHour + C(HourIdx) + C(weekOfday)', data=dframe).fit() 

	# print result.params.T
	beta = result.params.T 
	print "shape of beta", beta.shape
	try:
		nsample = X.shape[0]
	except:
		nsample = len(X)	 
	hIdx = np.array(X[:,2])	
	# print hIdx
	dummy = (hIdx[:,None] == np.unique(hIdx)).astype(float)
	wdayIdx = np.array(X[:,3])  
	dummy2 = (wdayIdx[:, None] == np.unique(wdayIdx)).astype(float)
	# print dummy, dummy2

	# X_test = [np.,  ]
	XX = np.c_[np.ones(nsample), dummy[:,1:], dummy2[:,1:], vals[:-1]]
	print XX.shape
	vec = XX.dot(beta)
	print vec

	s = 24*30+6
	t = 30*30+20 
	errRvals = abs(np.subtract(y_true[s:t], vec[s:t])/y_true[s:t])  
	print np.mean(errRvals)
	# print (result.summary())
	# print XX.shape
	plt.figure()
	# plt.plot(X[:,0:1])
	plt.plot(y_true[s:t])
	plt.plot(vec[s:t])
	plt.legend(["true", "predict"])
	plt.ylim(0,1)
	plt.ylabel("occupancy")
	plt.xlabel("# spots")
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)
	plt.show()

	# break

def identifyDayOfWeek(dictkey):
	datekey, sumVal, idx = dictkey 
	y = int(datekey[:4])
	m = int(datekey[4:6])
	d = int(datekey[6:])

	# print y, m, d 
	# notice that 
	weekday = datetime(y, m, d).weekday()

	return weekday+1

reconstruct(TSseries)	