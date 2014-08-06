"""
# this is base class to run the grid aggregation 
"""
import util

# An abstract class representing Grid Search Aggregation 
# 
class gridBase:
	def update(self): raise NotImplementedError("Override me")

	def insert(self): raise NotImplementedError("Override me")

	def computeOcc(self): raise NotImplementedError("Override me") 

class gridAggLots(gridBase):	
	def __init__(self, coords):
		self.coords = coords 
	
	def update(self):



	def insert(self): 	

	def computeOcc(self):
		self.lots = set()
		queue = []

		 