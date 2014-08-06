"""
setup new dev environment
	test script 

"""

## 
import matplotlib.pyplot as plt 
import numpy as np 

P ='../../refineData/15_MIN/902/902_2013_07_08.csv'

def readinData(f):
	fp = open(f,'r')
	for line in fp:
		print line


readinData(P)		