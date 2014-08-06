"""
generate a capacity map 

"""

P = '/home/seanqian/Desktop/dev/python/sfparkProj/data/2013_07_02.csv'
P2 = '/home/seanqian/Desktop/dev/python/sfparkProj/data/2013_07_08.csv'

def genLotCap(fpath):
	"""
	read in the file path 
	"""
	_lotCap = []
	_preT = None
	fp = open(fpath, 'r')

	for line in fp:
		_r = []  # each row has [id, cap ] 
		_ = line.split(",") 
		_ts = int(_[0][1:-1])
		if _preT is None :
			_preT = _ts
			_r.append(getID(_[3], _[4]))
			_r.append(int(_[6][1:-1]))
			
		elif _preT == _ts :	
			_preT = _ts
			_r.append(getID(_[3], _[4]))
			_r.append(int(_[6][1:-1]))
		else :
			break
		_lotCap.append(_r)	
	
	_lotCap = sorted(_lotCap, key=lambda l:l[0])
	return _lotCap			

def getID(s1, s2):
	_id1 = int(s1[1:-1]);
	_id2 = int(s2[1:-1]);
	return max(_id1, _id2)


##########################
cap1 = genLotCap(P)
cap2 = genLotCap(P2)



##########################
def combine(m1, m2):
	newM = []
	for i, r in enumerate(m1):
		_row = (r[0], max(r[1], m2[i][1]))
		newM.append(_row)
	return newM	

#print len(cap1), len(cap2)
capTable = combine(cap1, cap2)


####################
# write file 
####################

def genCapFile(table, outpath):
	fp = open(outpath, 'a')
	for _ in table:
		_s = str(_[0])+','+str(_[1])+'\r\n'
		fp.write(_s)
	fp.close()

Pout = 'LOT_CAP.txt'
genCapFile(capTable, Pout)			