from typing import Any
from Pedigrad.Containers.cl_apt import Applicator


class Container(object):

	__slot__ = ("applicator","data")

	def __init__(self,
								#List of inputs and their types
								applicator: Applicator,
								data: Any
								#The output type
								) -> None:
		#The algorithm of the container; i.e. an Applicator instance
		self.applicator = applicator
		#The data of the container
		self.data = data

	def push(self,
						#List of inputs and their types
						database: Any
						#The output type
						) -> Any:
		'''
		Calls the generator of the Applicator instance when the encountered database is "None"
		and calls the incrementor of the Applicator instance when the encountered database
		exists.
		'''
		if database == None:
			return self.applicator.generate(self.data)
		else:
			return self.applicator.increment(database,self.data) 
