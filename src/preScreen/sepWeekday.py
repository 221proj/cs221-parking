# out put the parking 

import numpy as np 
import matplotlib.pyplot as plt 
import os, re, datetime 
from collections import Counter
import shutil

P_OUTput = '/home/seanqian/Desktop/dev/python/sfparkProj/output3/'

def readinPIDs(path):
	# read from the data path to extract the parking lot IDs
	pIDs = [] 
	for fname in os.listdir(path):
		pIDs.append(fname);

	return sorted(pIDs)

"""
- note: 
	- weekday index = 0 is monday
	- weekday index = 1 is tuesday	
	- weekday index = 2 is wendesday
	- weekday index = 3 is thursday
	- weekday index = 4 is friday
	- weekday index = 5 is Saturday
	- weekday index = 6 is Sunday
"""


def getDateIndexInWeek(dateStr):
	lotID, year, month, day = dateStr.split("_")  
	y = int(year)
	m = int(month)
	d = int(day)
	weekdayIndex = datetime.date(y, m, d).weekday()         
	return weekdayIndex

def processWeekDay(fname, i):
	# format of the file name 
	FILE_FORMAT = "(.*).csv";
	# matched file
	mf = re.match(FILE_FORMAT, fname)
	# file date
	fdate = mf.group(1)
	dayIdx = getDateIndexInWeek(fdate)
	if dayIdx == i : 
		return True 
	else: 
		return False 	





def process(pth, di, desc): 
	# process the week day index 
	# - pth is the path of the data folder 
	# - i is the date index 
	# - description is the additional notes 

	pdList = readinPIDs(pth)
	for i, val in enumerate(pdList):
		fpth = pth+val+"/"
		for fname in os.listdir(fpth):
			# process file name with weekday index i 
			if processWeekDay(fname, di):
				print "...good...", fname, desc
				dst = "../../refineData/WeekDay/"+desc+"/"+val+"/";
				if not os.path.exists(dst):
					os.makedirs(dst)
				shutil.copy2(fpth+fname, dst) #"../../refineData/WeekDay/"+desc+"/"+val+"/")
				


process(P_OUTput, 4, "friday")
