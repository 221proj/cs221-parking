#read in AR err file and plot
import matplotlib.pyplot as plt 
import numpy as np 

filePath = 'AR_ERR_OUT.csv'
ERR_OUT_SVM = 'SVM_ERR_OUT.csv'

def readnplot(fpath):
	dat = []
	fp= open(fpath, 'r')
	for line in fp:
		
		_ = line.split(',')
		vol = int(_[0])
		print _[1][1:-3]	
		err = float(_[1][:-3])
		#print vol, err 
		a = [vol, err]
		dat.append(a)

	fp.close()	
	data = np.array(dat)

	#print data[:,1]*100

	#y = np.log10([1:]])
	y = data[:,1]#*100
	#"""
	##########
	# plot error hist 
	##########
	#plt.figure()
	#plt.hist(y, bins=25)
	#plt.show()
	###############

	###########
	# plot 
	###########
	print data.shape
	#print data[:,0] 
	
	plt.figure()
	# init a stack to store the error per centroid aggregation
	stackE = []
	for i in range(len(data[:,0])):
		if i+1== len(data[:,0]):
			break

		if data[i,0] <= data[(i+1),0]:
			stackE.append([data[i,0], data[i,1]])
		elif data[i,0] > data[(i+1),0]:
			stackE = np.array(stackE)
			plt.plot(stackE[:,0], stackE[:,1], '.-')
			#print stackE
			#print np.array(stackE).shape
			stackE = []
			#stackE.append(data[i,:])

	#plt.plot(data[:,0], y, '.-')
	
	plt.show()

	#plt.scatter(data[:,0], data[:,1])
	#plt.semilogy(data[:,0], y, '.')
	#ua, uid = np.unique(y, return_inverse=True)
	#count = np.bincount(uid)
	#"""


#readnplot(ERR_OUT_SVM)	
readnplot(filePath)
