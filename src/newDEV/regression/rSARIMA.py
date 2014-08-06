import rpy2.robjects as robjects
from rpy2.robjects import FloatVector
from rpy2.robjects.packages import importr
import numpy as np 

stats = importr('stats')
base = importr('base')


# pass in the data - numpy row vector 
# 
def runIdentifyModel(dat):
	occvec = robjects.FloatVector(dat)
	robjects.globalenv["occv"] = occvec
	
	print ">>>> in r function..."

	##########################
	##cat(sprintf("tuning AR param, p = %d \n",p));
	##cat(sprintf("tuning MA param, q = %d \n", q))
	##
	robjects.r('''
		best.order <- c(0,0,0,0,0,0)
		best.aic <- 99999
		occv = c(occv)
		# print(length(occv))
		for (p in 0:2){
			for (q in 0:2){
				for (i in 0:2){	
					for (n in 0:1){
						for (s in 0:2){
							tryCatch({
							cat(sprintf("tuning sarima param, p = %d, i =%d, q = %d, n =%d, s = %d\n", p,i,q,n,s))
							occfit <- arima(occv, order=c(p,i,q), seasonal=list(order=c(n,s,0), period=24), include.mean=FALSE )
							# print(occfit$aic)
							# print("fitting...")
							fit.aic <- occfit$aic
							print(fit.aic)	
							if(fit.aic < best.aic){
								best.order <- c(p,i,q,n,s,0)
								best.model <- occfit
								best.aic <- fit.aic
							}			
							}, error = function(ex) {
								cat("R modelling fail to fit");
							}, finally= { cat("Final...catch in R\n");} )
						}
					}	
				}
			}
		}
		print(best.order)
		''')
	bestOrder = np.array(robjects.r("best.order"))
	return bestOrder

	
# call the function after identify the SARIMA model  	
def runForecast(dat, p=2, i=1,q=1,n=0, s=0, t=0, desc=None):
	# call the function 
	occvec = robjects.FloatVector(dat)
	robjects.globalenv["occv"] = occvec 
	# pv = robjects.IntVector([p])
	robjects.globalenv["p"] = robjects.IntVector([p])
	robjects.globalenv["i"] = robjects.IntVector([i])
	robjects.globalenv["q"] = robjects.IntVector([q])
	robjects.globalenv["n"] = robjects.IntVector([n])
	robjects.globalenv["s"] = robjects.IntVector([s])
	robjects.globalenv["t"] = robjects.IntVector([t])

	#print occvec, 
	# print pv
	print "run forecasting...", desc
	#########################
	# 1 hour ahead prediction
	robjects.r('''
		cat(sprintf("SARIMA parameters, p = %d, i =%d, q = %d, n =%d, s = %d, t=%d \n", p,i,q,n,s,t ))
		occfit <- arima(occv, order=c(p,i,q), seasonal=list(order=c(n,s,t), period=24), include.mean=FALSE )
		occpred <- predict(occfit, n.ahead=1)
		ret <- occpred$pred;
		coefi <- occfit$coef;
		''')
	predVal = robjects.r("ret")[0]
	# print predVal
	return predVal


def runARIMA(dat, p,d,q, desc=None):
	occvec = robjects.FloatVector(dat)
	robjects.globalenv["occv"] = occvec 
	robjects.globalenv["p"] = robjects.IntVector([p])
	robjects.globalenv["d"] = robjects.IntVector([d])
	robjects.globalenv["q"] = robjects.IntVector([q])
	print "run forecast ARIMA non seasonal -- ", desc

	##############
	robjects.r('''
		cat(sprintf("ARIMA parameters, p=%d , d=%d, q=%d", p,d,q))
		occfit <-arima(occv, order=c(p,d,q), include.mean=FALSE)
		occpred <- predict(occfit, n.ahead=1)
		ret <- occpred$pred;
		coefi <- occfit$coef;
		''')

	predVal=robjects.r("ret")[0]
	print predVal;
	return predVal