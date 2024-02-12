from typing import Any
from Pedigrad.Containers.cl_cnt import Container
from Pedigrad.Containers.cl_rep import Repository
from Pedigrad.Containers.cl_ctr import Controller

class Compound(object):
	
	__slots__ = ("keys","containers")

	def __init__(self,
							 #List of inputs and their types
							 keys: dict[str,Any],
							 *containers: Container
							 #The output type
							 ) -> None:		 
		#Keys to assess the validity of the Container instructions
		self.keys = keys
		#The list of containers
		self.containers = list(containers)

	def push_onto(self,
								#List of inputs and their types
								repository: Repository
								#The output type
								) -> bool:
		'''
		Generalizes the "push" method associated with Container instances. See documentation.
		'''
		success = repository.controller.verify(self.keys)
		if success:
			if repository.databases == []:
				#Allocate memory for a new database
				repository.databases[:] = [container.push(None) for container in self.containers]
			else:
				#Update the data contained in the database
				repository.databases[:len(self.containers)] = [self.containers[i].push(db) for i,db in enumerate(repository.databases[:len(self.containers)])]
		return success

	def initialize(self,
								 #List of inputs and their types
								 repository: Repository
								 #The output type
								 ) -> bool:
		'''
		Deletes the content of the Repository instance and uses the data contained in the underlying 
		Compound instance to reinitialize the Repository instance: the compound's keys become 
		the data for the Controller instance and the data associated with each Container 
		instance is used to generate databases according to the Container instance's generator.
		'''
		success = repository.is_null()
		if success:
			for k,v in self.keys.items():
				#Translate self.keys into a signature
				repository.controller.signatures[k] = v
				#Try to allocate the __eq__ method to every key k
				try:
					repository.controller.verifiers[k] = type(v).__eq__
				except:
					#If type(v) does not have __eq__, then cancel the process and return False
					success = False
					repository.controller.signatures = {}
					repository.controller.verifiers = {}
					break
			#Complete the databases (the Controller instance is suppoed to allow access)
			success = success and self.push_onto(repository)
		return success
