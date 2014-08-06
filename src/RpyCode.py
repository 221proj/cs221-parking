import rpy2.robjects as robjects
from rpy2.robjects import FloatVector
from rpy2.robjects.packages import importr
import array

stats = importr('stats')
base = importr('base')



def show(v1, v2):
	#print v1, v2 
	occvector =robjects.FloatVector(v2)



	robjects.globalenv["occv"] = occvector
	#print occvector 

	#print robjects.r("is.numeric(occv)")
	#print occvector.rclass 


	# robjects 	
	fitObj = robjects.r(" occfit<-arima(occv, order=c(1,1,0), seasonal=list(order=c(0,1,0), period=24 ), include.mean=FALSE )")
	occPred = robjects.r(" occpred<-predict(occfit, n.ahead=2)")
	#print fitObj.names

	#fitObj = robjects.r("""
	#	seq.fit <-arima(occvector, order = c(1,1,0), 
	#		seasonal=list(order=c(1,1,0), period=24)),
	#		include.mean = FALSE)
	#	""")  
	#print "++++++++++++++++"
	#print occPred.rx("se")
	#print occPred.rx2("se")
	#print "----"
	#print occPred.rx2("se")[2]
	
	#print summary(fitObj)
	#print "hello"
	#raise "not implement"
	return occPred.rx2("se")[0]