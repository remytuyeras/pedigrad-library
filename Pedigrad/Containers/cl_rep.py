from __future__ import annotations
from typing import Any, Union
from Pedigrad.Containers.cl_ctr import Controller

class Repository(object):

	__slot__ = ("controller","databases")

	def __init__(self,
				 #List of inputs and their types
				 controller: Controller,
				 databases: list[Any]
				 #The output type
				 ) -> None:
		#A controller instance to control access to the databases
		self.controller = controller
		#A list of databases
		self.databases = databases

	def __str__(self) -> None:
		'''
		Returns a string showing information about the keys of the underlying Repository 
		instance and the type of each item stored in its list of databases (see documentation).
		E.g. if signatures = {"owner":"Bob","push":9} and databases = [[4,5],8,"hello"] 
		then the method returns the string "Bob|push:list;int;str"
		'''
		#A function used to get a key or a value from the signatures
		getkey = lambda x: x[1] if type(x[1]) == str else x[0]
		#Get the list of keys or values from the signatures
		keys = "|".join(map(getkey,self.controller.signatures.items()))
		keys_ = "-" if keys == "" else keys
		#A function used to parse the name of a type; E.g. <class 'int'> becomes "int"
		gettype = lambda x: '\033[94m'+str(x).split("\'")[1]+'\033[0m'
		#Get the list of types from the databases
		types = ";".join(map(gettype,map(type,self.databases))) if self.databases != [] else "-"
		#Return a string shoing keys and database types
		return keys_+":"+types

	@classmethod
	def null(cls) -> Repository:
		'''
		Returns an empty Repository instance (i.e. the Controller instance is made of empty 
		dictionaries and the collection of databases is empty).
		'''
		return cls(Controller({},{}),[])

	def is_null(self) -> bool:
		'''
		Returns a Boolean value indicating whether the Repository instance is empty 
		(i.e. the Controller instance is made of empty dictionaries and the collection 
		of databases is empty).
		'''
		return self.controller.signatures == {} and \
					 self.controller.verifiers == {} and \
					 self.databases == []

	def deliver(self,
							#List of inputs and their types
							keys: dict[str,bool],
							*restrictions: bool
							#The output type
							) -> Union[None,list[Any]]:
		'''
		Allows to pull information from the Repository.
		'''
		if self.controller.verify(keys):
			return [db for i, db in enumerate(self.databases) if i>=len(restrictions) or restrictions[i]!= False]
