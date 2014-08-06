import util, configSFpark 
import numpy as np
import alg
import matplotlib.pyplot as plt 
import pickle 
import rpyRalg


#print configSFpark.DIR_1HR_PATH
#print util.readDir(configSFpark.DIR_1HR_PATH)


_l = util.readDir(configSFpark.DIR_1HR_PATH)
#_l = util.readDir(configSFpark.DIR_15MIN_PATH)


def walkFileList(Flist):

	dat = DailyDictionary() #instance created to store the data

	for _ in Flist:		# _ is ID level 
		files = util.readDir(_+"/")
		#print files
		#break 
		for f in files:		# f is date level 
			ret = checkDailyFile(f)
			#print ret 
			if ret is not None:
				cap, dailyShape = ret 
				dat.add(dailyShape)
				#print dailyShape
				print "**add file**", f 
			#break	
	#dat.printDict()	

	#NUM_CLUSTER = 7	
	#centroids = alg.runKMeans(NUM_CLUSTER, dat.getter(), 99)	
	#print centroids
	
	#numOfKs = [k for k in range(3, 50)]

	numOfKs = [30]

	########################################
	# walk through all the k 
	def seeKthreshold(kList, dataFrame):
		xVals=[]
		yVals=[]
		lastErr = float('inf')
		_c = 0

		################################
		#print dataFrame 
		rpyRalg.runAkmean(dataFrame)

		#debug here 
		raise "manual break point"


		for i, val in enumerate(kList):
			
			print "calculating by k means..."


			centroids = alg.runKMeans(val, dataFrame, 99)
		
			#numCluster = centroids.shape[1]
			err1 = alg.errorKMeans(val, dataFrame, centroids)
			#print "*******************Error is :", err1
			yVals.append(err1)
			xVals.append(val)
			
			#multiPlotLayout(centroids, 600, fig)
			
			if (lastErr - err1)/lastErr < 0.001 :
				_c +=1	
			"""	
				#fig = plt.figure() 
				#multiPlotLayout(centroids, 600, fig) 
				#fig.tight_layout()
				#plt.show()
				break
			"""	
			#lastErr = err1

			if _c > 10:
				break

			with open('k'+str(val)+'centroids.pickle', 'wb') as handle:
				pickle.dump(centroids, handle)	
		
		#########################
		# figure for err - # of k
		"""	
		fig2 = plt.figure()
		plt.plot(xVals,yVals, "o-")
		#plt.show()
		plt.xlabel('number of k')
		plt.ylabel('error')
		plt.savefig('err_k_3-100.png')
		"""


		###########################
		# generate kMeanErr file 
		"""
		with open('kMeanErr.pickle', 'wb') as handle:
			pickle.dump((xVals,yVals), handle)
			
		"""
			
	##############################	
	# try to see which k is good for clustering	
	seeKthreshold(numOfKs, dat.getShapes())




	"""
	for col in range(NUM_CLUSTER):  
		centroid = centroids[:, col:col+1]
		x = [i for i in xrange(len(centroid))]
		fig = plt.figure()
		plt.plot(x, centroid, 'o-')
		plt.show()

	"""	
	#break 	
	



def checkDailyFile(path):
	"""
	sanity check for a lot on a day has desired records  
	"""
	stat = 0
	occV = []
	operV = []
	fp = open(path, 'r')
	for line in fp:
		#print line
		items = line.split(",")
		#print items
		#print items[3].strip(" \" ")
		oper = items[3].strip(" \" ")
		occ = items[2].strip(" \" ")
		price = items[4].strip(" \"|\r|\n ")
		
		#break
		if int(oper) <= 0:
			stat+=1 
		elif float(price) < 0 :
			stat +=1
		else:
			operV.append(float(oper))	
			occV.append(float(occ))
	if stat > 2:
		return None	
	elif len(operV) < configSFpark.TIME_RESOLUTION_1HR: 
		return None 
	else:	
		v1 = np.array(occV)
		v2 = np.array(operV)		
		occRateV = v1/v2
		#print v1, v2
		cap = np.max(v2) 
			
	return (cap, occRateV )


#def plotShapes(x, y):
	
def getpickleFile(fname):
	with open(fname, 'rb') as handle:
		b = pickle.load(handle)

	return b	

#############################
# plot centroids 
###################
def plotCentroidsV2(totK, topK, desc):

	print "plotCentroids" 
	NUM_CLUSTER = min(totK, topK)
	centroids = getpickleFile('k'+str(totK)+'centroids.pickle')


	"""
	for col in range(NUM_CLUSTER):  
		centroid = centroids[:, col:col+1]
	"""
	for j, centroid in enumerate(centroids): 
		x = [i for i in xrange(len(centroid))]
		fig = plt.figure()
		plt.plot(x, centroid, 'o-',linewidth=3)
		plt.xlabel( desc )
		plt.ylabel('occupancy rate')
		#plt.show()
		plt.xlim(0, max(x))
		plt.ylim(0,1)
		plt.savefig('fig1hr/shape'+str(j)+'.png')

####################

class DailyDictionary:
	def __init__(self):
		self.shapes = []

	def add(self, v):
		self.shapes.append(v)
	

	def printDict(self):
		print self.shapes

	def getShapes(self):
		return self.shapes


class LotDailyDictionary(DailyDictionary):
	def __init__(self):
		DailyDictionary.__init__(self)
		self.ID = None

	def addID(self, lotID):
		self.ID = lotID

	def getID(self): 	
		return self.ID 
	
	def getSize(self):
		return len(self.shapes)
	
	def setLotCapacity(self, num):
		self.CAP = num

	def getCap(self):
		return self.CAP 	



class AggregateDictionary(DailyDictionary):
	def __init__(self):
		DailyDictionary.__init__(self)
		self.LOTS = None
		self.shapes = []
		self.sumCAP = 0 

		#self.MINR = 0

	def setAggregateSet(self, varset):
		self.LOTS = varset 

	def getIDs(self):
		return [ obj.getID() for obj in self.LOTS]

	def getMinRecord(self):	
		r = None
		#print self.LOTS
		for obj in self.LOTS:
			#print obj
			if not r:
				r = obj.getSize()
			elif r > obj.getSize():
				r = obj.getSize()

		#self.MINR = r
		return r		

	def setTotalCap(self, num):
		self.sumCAP = num

	def getTotalCap(self):
		return self.sumCAP


	def run(self):	
		_r = self.getMinRecord()
		_sum = 0 
		_occVols = []
		#_counter = 0  
		for obj in self.LOTS: 
			_vector = []	# single lot 
			#print obj.getID()
			_sum += obj.getCap()
			_counter = 0 
			#print obj.getShapes()
			for s in obj.getShapes():	
				#print s  
				#print _r
				_counter +=1
				if _counter <= _r: 
					volume = s*obj.getCap()
					#print volume
				else:	 
					break
				_vector.append(volume)

			#print len(_vector)	
			_occVols.append(_vector)

			#print len(_occVols)
			#print _occVols
			#if len(_occVols) > 1:
			#	break

		v = np.array(_occVols)
		#np.sum
		vnew = np.sum(v, axis=0) 
		#print v.shape, _sum 
		
		#print vnew/_sum

		#print vnew.shape
			#break	
		self.setTotalCap(_sum)
			
		return vnew/_sum	



"""
List of individual parking lots 
"""
def checkLotDailyLoad(Flist):
	ind = []

	for _ in Flist:		# _ is ID level 
		files = util.readDir(_+"/")
		#print files
		#break 
		dat = LotDailyDictionary()
		cap = None
		for f in files:		# f is date level 
			ret = checkDailyFile(f)
			if ret is not None:
				vol, dailyShape = ret
				dat.add(dailyShape)
				#print dailyShape
				print "**add file**", f 
			
				if cap is None:
					cap = vol 

		if dat.getSize()> 0:
			_id = _[-6:]
			dat.addID(_id)
			dat.setLotCapacity(cap)
			ind.append(dat)		

		 
	return ind


def constructLotPoolPath(lotPool):
	_l=[]
	for val in sorted(lotPool): 
		if len(val)> 4:
			path = configSFpark.DIR_1HR_PATH+val
			_l.append(path)
	return _l	


def seeSingleLotShapes(obj):
	if not isinstance(obj, LotDailyDictionary):
		#print "hey", obj.getID(), obj.getSize()
		raise "not right instance"

	labelSet = []	
	if obj.getSize() > 2:	
		#historyAvg = np.average(obj.getShapes)
		
		for s in obj.getShapes():
			clabel = alg.generateLabel(s, CEN)
			labelSet.append(clabel)
			#break 
	return labelSet		
			

def processDict(_dictionary):

	_l = []
	
	_xV = []
	_yV = []

	for d in _dictionary:
		#print d.getCap
		if d.getSize() < 3:

			continue
		elif d.getSize() >= 3:	
		
			_l.append(d)	
			a_dict = AggregateDictionary()

			labelSet = []
			a_dict.setAggregateSet(_l)
			shapes = a_dict.run()
			
			print "------shapes------", shapes 

			raise "break point------"


			for s in shapes:
				clabel = alg.generateLabel(s, CEN)
				labelSet.append(clabel)

			#print labelSet, a_dict.getTotalCap()
			H = entropy(labelSet)
			V = a_dict.getTotalCap()
			#listOfLabels = seeSingleLotShapes(d)
			#print listOfLabels, d.getCap()
			_yV.append(H)
			_xV.append(V)


	#width = .35
	#ind = np.arange(len(_yV))		
	plt.figure()
	plt.plot(_xV, _yV, 'r-')
	plt.xlabel('number of spots')
	plt.ylabel('value of entropy')
	plt.show()
 
	

def entropy(x):
	elems = {}
	for v in x: 
		#x.count(val)
		val = str(v)
		if val in elems.keys():
			elems[val] +=1 
		elif val not in elems.keys():
			elems[val] =1 	
	"""	
		if elems[val]: 
			elems[val] +=1 
		else:
			elems[val] = 1	
	"""		
	for key, val in elems.items():
		elems[key] = float(val)/float(len(x))
		
	a = np.array([i for i in elems.values()])	
	#print a 
	#print np.log(a)
	b = np.log(a)
	#print b 
	e = a.dot(b)
	#print -e 
	return -e	



#############################
# calculate entropy
def processDictV2(_dictionary):
	_l = []
	
	_xV = []
	#_yV = []
	num_bins = 50 

	for d in _dictionary:
		labelSet = seeSingleLotShapes(d)
		if len(labelSet) > 0:
			H = entropy(labelSet) 
			_xV.append(H)


	fig1 = plt.figure()
	plt.hist(_xV, num_bins)	
	plt.ylabel("# of lots")
	plt.xlabel("entropy value")
	plt.show()
	#plt.savefig('entropy_plot.png')

################################################
#CEN = getpickleFile('k30centroids.pickle')






########################
# step 1 
# - walk all lots cluster akmean
########################
#print _l[:-15]
walkFileList(_l[:-15])

########################
# step 2 
# - plot out all the centers  
########################
#plotCentroidsV2(112, 16, "daily profile - 15 minutes resolution")
#plotCentroidsV2(530, 16, "daily profile - 1 hour resolution")
######################

#print  _l[:-15]
#onParkIDs = _l[:-15]

#Dict = checkLotDailyLoad(onParkIDs)
#print len(Dict)

#################################

#_dict = checkLotDailyLoad(constructLotPoolPath(configSFpark.CANDIDATE))

##############entropy########## 

#_dict = checkLotDailyLoad(_l[:-15])
#processDictV2(_dict)
#processDict(_dict)

