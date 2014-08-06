"""
FilterUtil.py holds a class which takes in the list of neighbourhood parking lots 
and doing aggregation of the occupancy 

"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from collections import deque
from collections import Counter, OrderedDict
import re, os, datetime, copy, time 
import statsmodels.api as sm 
from statsmodels.graphics.api import qqplot

import RpyCode as rpycode 


def convertFileToDataTable(fpath):
    #df = pd.read_csv(fpath, sep=',')
    df = pd.read_csv(fpath, header=None)
    #print df[1:10]      dataFrame from 
    #print type(df)

    return df 



def checkValidFile(fpath):
    if not os.path.exists(fpath):
        assert "file not exists" 
    
    m = re.match('.+/(*.csv)$', fpath)           
    if m:
        print m.group(1)


def calculateSingleFile(fpath, st, et):
    if not os.path.exists(fpath):
        assert "file not exists"
    
    fr = open(fpath, 'r')

    for line in fr:
        if isValidTimeRecord(line) and isInTimeSlot(line, st, et):
            ## TO-DO 
            # calculate the occupancy 
            print "valid"



########################################
# convert timestamp to tuple (day in week, hour in day, min in hour)
def convertTimestampToDayHourMin(ts):
    """
    the convert Timestamp to (Day, Hour, Min) tuple

    @param ts - string of timestamp
     
    """ 
    if (ts is not None) and ( int(ts) > 100000):
        dateT = datetime.datetime.fromtimestamp(int(ts)) 
        y = dateT.year
        m = dateT.month
        d = dateT.day
    
        dayInWeek = datetime.date(y, m, d).weekday()   
        hourInDay = dateT.hour
        minInHour = dateT.minute    
        return (dayInWeek, hourInDay, minInHour) 




###############################################
def isInTimeSlot(line, st, et):
    if type(line) is not str:
        raise "incorrect input "
    _tempList = line.split(',') 
        #print _tempList[0]             
    ts_record = _tempList[0].strip("\"")    # current record's time stamp
    day, hr, minute = convertTimestampToDayHourMin(ts_record)
    
    # convert each record time stamp to min format 
    rec_format_mm_day = int(hr)*60 + int(minute)          # first few elements should be around midnight so hr == 0
    # input of st, et should be xx:xx 
    st_hh, st_mm = st.split(':')    
    et_hh, et_mm = et.split(':')

    st_format_mm_day = int(st_hh) * 60 + int(st_mm) 
    et_format_mm_day = int(et_hh) * 60 + int(et_mm)

    #print rec_format_mm_day, st_format_mm_day, et_format_mm_day

    if rec_format_mm_day >= st_format_mm_day and rec_format_mm_day <= et_format_mm_day:
        return True
    else:
        return False     


###############################
def isInTimeSlotV2(ts, st, et):
    day, hr, minute = convertTimestampToDayHourMin(ts)
    
    rec_format_mm_day = int(hr)*60 + int(minute)          # first few elements should be around midnight so hr == 0
    # input of st, et should be xx:xx 
    st_hh, st_mm = st.split(':')    
    et_hh, et_mm = et.split(':')

    st_format_mm_day = int(st_hh) * 60 + int(st_mm) 
    et_format_mm_day = int(et_hh) * 60 + int(et_mm)


    #print "--show time--",rec_format_mm_day, st_format_mm_day, et_format_mm_day

    if rec_format_mm_day >= st_format_mm_day and rec_format_mm_day <= et_format_mm_day:
        return True
    else:
        return False     

    
def isValidTimeRecord(line):
    if type(line) is not str:
        assert "non valid input string"




def extractParkLotID(mixedPath):
    """
    typical string passed in are "../train/362001/"
    """
    if type(mixedPath) is not str:
        assert "not valid type"
    _l = mixedPath.split("/") #  _l = [ '..' , 'train', 'id', '' ] 

    #print _l[2], _l[-2]
    return _l[-2]

def extractMonthDay(filename):
    """
    func to extract the day & month from 
    @param filename = "parkLotID_yy_mm_dd.csv"
    """
    if type(filename) is not str:
        assert "not pass-in a string as filename"

    _s = filename.strip(".csv")    
    _l = _s.split("_")    
    #print _l[1] 

    return (_l[2], _l[3])   # return a tuple (mm, dd)

def isInTargetDateRange(fileMMDD, startMMDD, endMMDD):
    """
    pass in three tuples fileMMDD, startMMDD, endMMDD

    """
    #print "checking inside target date range"
    def compareMMDD(d1, d2):
        tMM, tDD = d1        # passed in date Month, date Day
        cMM, cDD = d2        # compared Month, compared Day  
        #print "d1, and d2, " ,d1, d2

        _t = int(tMM)*100+int(tDD)      # convert month, day => 100*m+d; i.e. 07/09 = 700+9 
        _c = int(cMM)*100+int(cDD) 

        if _t >= _c :
            return 1

        elif _t <= _c :      
            return 2 

        else:    
            return -1 

    if compareMMDD(fileMMDD, startMMDD) == 1 and compareMMDD(fileMMDD, endMMDD) == 2:      
        #print "valid"  
        return True
    else:
        #print ">_< ~!! invalid"
        return False


######################################
# class - Filter 
######################################
class Filter:
    """
    Filter class doing one by one aggregation
    
    """
    def __init__(self, dataDirPath):
        #init a total vaild number of candidates parking lot 
        self.numVar = 0
        #init a set of valid set of aggregated parking lots 
        self.varNames = []
        
        self.DIR = dataDirPath
        # queue of valid 
        self.queueLots = deque()

    def setDistance(self, dist):
        self.radius = dist  

    def setDescription(self, describe):
        self.locNameDesc = describe 

    
    def takeInCandidateLots(self, candidateList=None):	
        if candidateList is None:
            assert len(candidateList)== 0 #, "length of candidate Aggregation Lots is %d" % len(candidateList)
        
        # create a queue to store the candidate parking lots list 
        if self.queueLots is None:
            self.queueLots = deque()

        for i, val in enumerate(candidateList):
            lotFolder = str(self.DIR + val+"/") 
            self.varNames.append(lotFolder)
            self.queueLots.append(val)

        return self.varNames


    def setDateSpan(self, startDay, endDay):
        if type(startDay) is str:
            m = re.match('(.+)/(.+)/(.+)', startDay)
            if m:
                self.startMM = m.group(1)
                self.startDay = m.group(2)
                self.startYear = m.group(3)

        if type(endDay) is str :
            m = re.match('(.+)/(.+)/(.+)', endDay)
            if m:
                self.endMM = m.group(1)
                self.endDay = m.group(2)
                self.endYear = m.group(3)



    def setHourSpan(self, startHr, endHr):
        self.startHr = startHr
        self.endHr = endHr
        if type(startHr) is str:
            m = re.match('(.+):(.+)', startHr) 
            if m:     
                self.startHH = m.group(0)
                self.startMINUTE = m.group(1)

        if type(endHr) is str:
            m = re.match('(.+):(.+)', endHr) 
            if m:     
                self.endHH = m.group(0)
                self.endMINUTE = m.group(1)
        
        
    def runAggregatedOCC(self, candiList, dayFirst=0, lotFirst=0, distanceOnly=0):
        """
        inside the candiList it stores "../train/lotID/"
        """
        print self.startMM, self.startDay, " - ", self.endMM, self.endDay

        # 
        if dayFirst > lotFirst and dayFirst > 0: 
            self.runDateFirstAggregateMeth(candiList)
        elif dayFirst <= lotFirst and lotFirst > 0:  
            self.runLotFirstAggregateMeth(candiList)
        elif distanceOnly > 0 :
            self.runDateFirstAggregateMeth(candiList, 0)    
    
    def runDateFirstAggregateMeth(self, candiList, step=1):     
        """
        step = 1 means aggregate lot 1 by 1 
        """

        lotSizeDict = dict()


        for i, val in enumerate(candiList):
            # each lot 
            _plID = extractParkLotID(val) # parking lot ID 
            # print val, ">>>>", extractParkLotID(val)  
            lotSizeDict[_plID] = None 
            lotIDTimeseries = Counter() 
            
            #############################
            #plt.figure()
            lotDayLevelSeries = Counter()

            for fname in os.listdir(val): 
                # each day 
                # print extractMonthDay(fname)
                # print fname
                # create a stack to store the occupancy rate
                dailyStack = None 
                mm, dd = extractMonthDay(fname) 
                #print "month and date ", mm, dd 
                #print "-stHr, endHr-",self.startHr, self.endHr


                if isInTargetDateRange((mm,dd), (self.startMM, self.startDay) , (self.endMM, self.endDay) ):
                    
                    pDataFrame = convertFileToDataTable(str(val+fname))
                     
                    _operNumInit = pDataFrame[3][0] 
                    _operNumInit = _operNumInit.replace('\"','')
                    _operNumInit = float(_operNumInit)
                
                    if _operNumInit > 100:
                        print "garage"
                        print fname
                        print dailyStack

                        continue

                    #if len(pDataFrame) < 284: # 284 is for 5 minutes gap data

                    if len(pDataFrame) < 16:
                        print "incomplete dataset"
                        print "current record:", len(pDataFrame)

                        continue

                    #print sum([ float(pDataFrame[3][i]) for i in range(len(pDataFrame))])   
                    #print pDataFrame     

                    _soperlist = [] 
                    _socclist = []
                    #_spricelist =[]

                    for j in xrange(len(pDataFrame)):
                                                                    
                        _ts = pDataFrame[0][j]

                        _price = pDataFrame[4][j]  
                        _price = _price.replace('\"', '') 
                        
                        _occNum = pDataFrame[2][j]
                        _occNum = _occNum.replace('\"', '') 
                        _occNum = float(_occNum)

                        _operNum = pDataFrame[3][j] 
                        _operNum = _operNum.replace('\"','')
                        _operNum = float(_operNum)
                        
                        _soperlist.append(_operNum) 
                        _socclist.append(_occNum)
                        #_spricelist.append(_price)


                        if isInTimeSlotV2(_ts, self.startHr, self.endHr) and float(_price) >= 0 :
                            #newV = []
                            if _operNum > 0:
                                #print "-------------",float(_occNum)/float(_operNum)
                                newV = np.array([pDataFrame[0][j], float(_occNum)/float(_operNum), _operNum])
                            elif _operNum <= 0:
                                print "does not record ----"
                                #raise "not in operation"
                                continue

                            else: 
                                print "**********what happend?***********"
                                continue


                            
                            if dailyStack is None:
                                dailyStack = newV
                            else:    
                                dailyStack = np.vstack((dailyStack, newV))
                                #print dailyStack

                        elif float(_price) < 0:
                            continue 

                        #print dailyStack    
                    ###################################
                    # val1 is TimeStamp, val2 is occRate, val3 is operNumber
                    # lotIDTimeseries store whole time series
                    #print dailyStack 
                    """
                    print "oper", _soperlist
                    print "occ", _socclist
                    """
                    #print "*price*", _spricelist

                    if _soperlist.count(0) > 10:
                        continue 


                    if dailyStack is not None:

                        for val1, val2, val3 in dailyStack: 
                            lotIDTimeseries[val1] = (val2, val3)
                        
                    #sort 

                        lotDayLevelSeries[str(mm+"-"+dd)] = dailyStack

            #print lotDayLevelSeries.items()              
            #print lotIDTimeseries
            '''
            plt.figure() float(_price) >= 0
            #assert "debugging...."   

            for key, value in lotDayLevelSeries.items():
                _X = [_i for _i in xrange(1, len(lotDayLevelSeries[key])+1 ) ]
                _Y = lotDayLevelSeries[key][:, 1:2] 
                plt.plot(_X, _Y, 'o')
            plt.show()    
            '''
            if len(lotIDTimeseries) < 1:
                assert "calculating occ, oper error!"
                continue

            sortedLotDict = sorted(lotIDTimeseries.items(), key = lambda x: x[0] )
            #print "sorting...",sortedLotDict
            lotSizeDict[_plID] = sortedLotDict

            
        aggregateDict(lotSizeDict, step, self.radius, self.locNameDesc )


    def runLotFirstAggregateMeth(self, candiList):
        print "lot first "
    

##################################            

def aggregateDict(lotDict, step=1, distrange=0, desp='NA'):
    aggDict = Counter()
    _dict_temp = Counter()
    c = []      # list of the aggregated lots 
    accumulatedVolume = 0

    lots = None 

    tnow = datetime.datetime.now()
    fileseed = str(tnow.month)+"_"+str(tnow.day)+"_"+str(tnow.hour)+str(tnow.minute)

    for key1, valDict1 in lotDict.items():
        

        #print ">>>>>>>>>>>>>>>>>>>", valDict1
        if valDict1 is None:
            continue

        c.append(key1)
        aggDict = _dict_temp    

        for key2, val2 in valDict1:
            #key2 = int(key2)
            #print "aggDict at beg of each loop", aggDict
            if not aggDict[key2]:
                aggDict[key2] = (val2[0]*val2[1], val2[1]) 
                   
            elif aggDict[key2]: 
                aggDict[key2] = (aggDict[key2][0] + val2[0]*val2[1] , aggDict[key2][1] + val2[1])
                #print "conti after",key2, aggDict[key2]
            accumulatedVolume = aggDict[key2][1]

            _dict_temp = aggDict.copy() 

        # accumulate parking lot one by one 
        
        #showAggreationDict(aggDict, c)   
        #print _dict_temp
        lots, errRate = showAggreationDict(_dict_temp, c)
        
        ##*******************************************
        ## uncomment here - if need to output err into a individual file
        if step > 0: 
            print "accumulated v ", accumulatedVolume
            outputLotListWithErr( lots, errRate, accumulatedVolume , 'byLot', fileseed)    

    if step == 0 and lots is not None:
        print "accumulated v ", accumulatedVolume, distrange
        outputLotListWithErr( lots, errRate, accumulatedVolume , desp, fileseed, distrange)    


        #break

def showAggreationDict(aggParkLotDict, aggPList):
    
    aggDict = aggParkLotDict.copy()

    if len(aggDict) < 1:
        assert "error, empty dictionary"
        
    for key, val in aggDict.items():
        #print val[0], " and ", val[1]
        occR = float(val[0]/val[1]) 
        aggDict[key] = (occR, val[1])

    sortedaggDict = OrderedDict(sorted(aggDict.items()))    

    X = [int(key) for key in sortedaggDict]
    Y = [v[0] for key, v in sortedaggDict.items() ]  
    xNew = pd.to_datetime(X, unit='s')

    x_ts_new = xNew.tz_localize("UTC").tz_convert("America/Los_Angeles")
    
    #print x_ts_new
    #print Y  
    #print len(Y) 
    #Y = diffSeasonalTrend(Y, 24)  
    

    """
    # here is the function called previously 
    err = timeSeriesAnalysis(x_ts_new, Y, aggPList)
    """


    err = timeSeriesAnalysisV2(x_ts_new, Y, aggPList)


    return (aggPList, err)
    
    ##fig = plt.figure()
    
    #plt.plot(xNew, Y , 'o')
    #plt.plot(x_ts_new, Y, 'o')
    ##ax = fig.add_subplot(111)
    #ax.set_ylabel( (str(k)+"\n" for k in aggPList) , rotation='horizontal')

    ##ax.plot(x_ts_new, Y)
    #plt.ylabel(str(aggPList))
 
    ##plt.ylim(0,1)
    ##plt.show()

def diffSeasonalTrend(v, period):

    for i, val in enumerate(v):
        if i < (len(v) - period):
            diffV = v[i+period] - val
            v[i] = diffV
             
        elif i >= (len(v) - period):
            continue

    return v[:-period]        




def timeSeriesAnalysisV2(v1, v2, Plist):
    if len(v2) > 48 :
        return rpycode.show(v1, v2)
    else:     
        return -1






def timeSeriesAnalysis( v1, v2, Plist):

    ###################################
    # try to call program in R 
    #rpycode.show(v1, v2)





    #print v1, v2 

    ######################################
    # plot the raw data 
    """
    occSeries = pd.TimeSeries(v2, index=v1)
    plotGenericTSdata(occSeries)
    """

    """
    ###############################
    # diff to make a stationary series 
    v2 = diffSeasonalTrend(v2, 24)
    v1 = v1[:-24]

    v2 = diffSeasonalTrend(v2, 1)
    v1 = v1[:-1]
    """


    #for _ in range(2):
    #    v2 = diffSeasonalTrend(v2, 24)
    #    v1 = v1[:-24]




    print "********calculation********"
    print "-----new lot is added---- "
    occSeries = pd.TimeSeries(v2, index=v1)
    #print occSeries
    #ar_model = sm.tsa.AR(occSeries, freq='5min')

    
    ##########
    #plot -- could be commented if it is not needed to display
    
    

    #pandas_ar_res = ar_model.fit(maxlag=9, method='mle', disp=-1)
    meanErr = 0
    try:         
        arma_mod02 = sm.tsa.ARMA(occSeries,(1,0)).fit()

        #arma_mod02 = sm.tsa.AR(occSeries,1).fit()
        print "*********************************\n"
        print arma_mod02.params
        print arma_mod02.aic, arma_mod02.bic, arma_mod02.hqic
        
        print "**",len(occSeries), "**"

        #pred = arma_mod02.predict(start=600, end=643, dynamic=False)         # prediction range is hard coded here 
        
        forecastDict = dict() 

        START_POINT = 800
        STEP_AHEAD  = 2    # (inclusive)
        SPAN = 21
        for i in range(1,SPAN): 
            pred = arma_mod02.predict(START_POINT+i, START_POINT+i+STEP_AHEAD, dynamic=True)
            

            #print pred.values, pred.index.second

            for j, val in enumerate(pred.index) : 
                d1 = datetime.datetime(val.year, val.month, val.day, val.hour, val.minute, val.second)
                key = int(time.mktime(d1.timetuple()))
                #if not forecastDict[val] :
                forecastDict[key] = pred.values[j]
                
            #print len(forecastDict)            

        #while i < 600 and  
            #pred = arma_mod02.predict(i, i+3, dynamic = False)
        #arma_mod02.plot_forecast(3)
        sorted(forecastDict)

        ##############################
        #generate forcast vector 
        _fVectorIndex = []
        _fVectorVals = [] 
        for k, val  in forecastDict.iteritems():
            _fVectorIndex.append(k)
            _fVectorVals.append(val) 
             
        xNew = pd.to_datetime(_fVectorIndex, unit='s')

        xfV= xNew.tz_localize("UTC").tz_convert("America/Los_Angeles")    

        forecastVector = pd.TimeSeries(_fVectorVals, index=xfV)
        

    #print occSeries.index
    #print occSeries.ix[occSeries.index[0]:]  
        #print occSeries[100:110]
        meanErr = mean_forecast_err(occSeries[START_POINT+1:START_POINT+SPAN + STEP_AHEAD], forecastVector)
        print "*****Aggregate List***************"
        print "*>>",Plist 
        print "*******Mean Forecast Error********\n", 
        print "**", meanErr
        #print "*", mean_forecast_err(occSeries, forecastVector)
        print "*********************************"

        #####################################
        print arma_mod02.summary()

        ##################################
        # comment if figure is not needed to display
        """
        if len(Plist) > 2:
            plotPredvsTrue(occSeries, forecastVector, Plist, START_POINT)

            plotModelFigures(arma_mod02, occSeries)
        """

    except ValueError: 
        #assert "Model doesn't work"
        print "model doesn't fit ..."
        print "check aggregated lots", Plist
    #except: 
    #   print "Error: func<timeSeriesAnalysis>"

    return meanErr
    
#####################################
def mean_forecast_err(y, yhat):
    #print len(y), len(yhat)
    #print y, "--------\n", yhat, "\n"
    #print "=========\n",y.sub(yhat)

    return abs(y.sub(yhat)/y).mean() 
    #return  np.mean(np.square(y.sub(yhat).values))  
    


def plotGenericTSdata(dataV):
    print "***length of the data serie***", len(dataV)
    occSeries = dataV 
    fig = plt.figure(figsize=(14,8))
    
    ax = fig.add_subplot(111)
    
    ax = occSeries.plot(style='-')
    """
    
    x = [i for i in xrange(len(dataV))] 
    
    #x = occSeries.index.squeeze()
    ax.plot(x, dataV)
    """

    #ax.set_ylim(0,1)
    #ax.set_xlim(0, len(dataV))
   

    plt.show()

########################################
def plotModelFigures(fittedModel, occupancyV):
    arma_mod02 = fittedModel
    occSeries = occupancyV

    #########################################
    # define a func to plot residual distribution
    def residualDistributionPlot(vector, num_bins):
        #print np.sum(vector)
        print vector 
        #print vector/np.sum(vector)
        _fig = plt.figure() 
        _ax = _fig.add_subplot(111)
        n, bins, patches = plt.hist(vector, num_bins, normed=1)
        print "----| inside the residual plot |---"
        #print n 

        #print bins 
        #for patch in patches: 
        #    print patch 
        #_fig2 = plt.figure() 
        #_ax = _fig2.add_subplot(111)
        #plt.plot(bins, n/sum(n))


    ################## plot residual ################
    fig = plt.figure(figsize=(14,8))
    ax = fig.add_subplot(111)




    print "------------residual-------------"
    #print arma_mod02.resid

    #ax = arma_mod02.resid.plot(ax=ax)
    x = [i for i in range(len(arma_mod02.resid))]
    ax = plt.plot(x, arma_mod02.resid.values)

    residualDistributionPlot(arma_mod02.resid.values, 100)



    #plt.show()
    

    # 
    fig = plt.figure(figsize=(14,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(occSeries.values.squeeze(), lags=50, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(occSeries, lags=50, ax=ax2)
    #plt.show()
    
    # 

    resid = arma_mod02.resid
    fig = plt.figure(figsize=(14,8))
    ax = fig.add_subplot(111)
    fig = qqplot(resid, line='q', ax=ax, fit=True)
    plt.show()



####################################    
    # plot prediction vs observed values 
    # 
def plotPredvsTrue(occV, predV, parkingLotArr, startpoint):

    occSeries = occV
    pred = predV.sort_index()

    Plist = parkingLotArr

    """

    ax = occSeries.ix[occSeries.index[0]:].plot(style='o-', figsize=(12,8), label='True Occupancy Ratio')
    #print 
    #ax = pred.plot(ax=ax, style='r--', label='Dynamic Prediction')

    ax = pred.plot(ax=ax, style='ro-', label='Dynamic Prediction')
    ax.set_title('Prediction')
    ax.legend()
    ax.set_xlabel(str(Plist))
    """
    
    #print "inside the prediction vs true value function" 

    #print occV
    print "--------plot out prediction-------"
    #print sorted(pred)
    #print pred

    plt.plot(occSeries.index[0:startpoint], occSeries.values[0:startpoint], 'b-', sorted(predV.index), pred, 'ro-')
    plt.legend(['observation', 'prediction'])


    plt.show()



####################################
def outputLotListWithErr(plist, err, val, desp1, desc, dist="NA"):
    print "------------------", plist, err, val 
    tnow = datetime.datetime.now()

   
    
    if dist is "NA":
        filename = 'samples/CITYHALLs_1hour_beg_end_out_'+desc+'.txt'
        fp = open(filename, 'a')
        fp.write(str((plist,err,val))+"\r\n")
        fp.close() 
    elif dist is not "NA":
        filename = 'samples/milerange/Loc'+desp1+'_mileRange_1ahead_'+desc[:-1]+'.txt'
        fp = open(filename, 'a')
        fp.write(str((plist,err,dist))+"\r\n")
        fp.close()     
    

    print "-------end writing line----"