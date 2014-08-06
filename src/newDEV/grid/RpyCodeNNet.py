import rpy2.robjects as robjects
from rpy2.robjects import FloatVector
from rpy2.robjects.packages import importr
import array

stats = importr('stats')
base = importr('base')
nnet = importr('nnet')
#quantmod = importr('quantmod')
caret = importr('caret')

def nnlearn(v2):
	#v2 is occupancy vector 
	print "neural nets call..."
	occvector =robjects.FloatVector(v2)
	robjects.globalenv["occv"] = occvector

	#robjects.r('''
	#		dim(occv)
	#		dat <-data.frame(occv, x1=Lag(occ,1), x2 = Lag(occ,2), x3 = Lag(occ,24))
	#		names(dat) <-c('occ', 'x1', 'x2', 'x3')
	#		model <- train(occv~x1+x2+x3, dat, method='nnet', linout=TRUE, trace=FALSE)

	#		ps <- predict(model, dat)
	#		''')
	#print robjects.r('length(ps)')