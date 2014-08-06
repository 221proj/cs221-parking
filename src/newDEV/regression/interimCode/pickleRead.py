# this script print out the file 
import pickle 

def readpfile(fpth):
	with open(fpth, 'rb') as handle:
		b = pickle.load(handle)

	return b


ret = readpfile("../err/ATT38FFNN_agg_err.p")	

print ret[0] 

import matplotlib.pyplot as plt

plt.figure()
plt.plot(ret[0], ret[1])
plt.ylim(0,0.001)
plt.show()

