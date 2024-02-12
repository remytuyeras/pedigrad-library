from __future__ import annotations
from typing import  Any, Callable, IO, Union
from Pedigrad.Pipeline.cl_prs import Parser, PSchemaArg, PSchemaOut
from Pedigrad.Workflow.cl_pro import PreOrder

class Application(Parser):

	__slots__ = ("separators","bracketors","line_values","line_pointers", \
							 "preorder","pipeline","memory")

	def __init__(self,
							 #List of inputs and their types
							 separators: list[str],
							 bracketors: list[str],
							 preorder: PreOrder,
							 #The output type
							 ) -> None:
		#The subclass Parser is equipped with 4 variables
		super(Application,self).__init__(separators,bracketors)
		##Preorder used to organize the pipeline working space
		self.preorder: PreOrder = preorder
		self.preorder.complete()
		#Pipeline of functions to be applied to the parsed data
		self.pipeline: dict[str,list[Callable[[int],None]]] = {}
		#Outputs of each function in the pipeline
		self.memory: dict[str,dict] = {}
		self.initialize()

	def _buffer(self,
							#List of inputs and their types
							row
							#The output type
							) -> None:
		'''
		Memorizes the information parsed through the method read_line.
		'''
		self.memory["!"].setdefault(row,self.line_values)

	def run_at(self,
						 #List of inputs and their types
						 row: int,
						 key: str
						 #The output type
						 ) -> None:
		'''
		Runs all processes associated with a given step in the pipeline.
		'''
		for callable_item in self.pipeline[key]:
			callable_item(row)

	def add_step(self,
							 #List of inputs and their types
							 key: str,
							 callable_item: Callable[[int,Application],None]
							 #The output type
							 ) -> None:
		'''
		Adds a process to the pipeline.
		'''
		if key != "!":
			self.pipeline[key].append(lambda row: callable_item(row,self))

	def run_below(self,
								#List of inputs and their types
								row: int,
								key: str
								#The output type
								) -> None:
		'''
		Runs all processes associated with keys that are less than or equal to the input key
		for the preorder structure stored in self.preorder.
		'''
		if self.preorder.mask:
			self.run_at(row,"!")
		all_elements = list(self.preorder.relations[key])
		while all_elements != []:
			minima = self.preorder.extrema(all_elements,False)
			for elt in minima:
				self.run_at(row,elt)
			all_elements = [x for x in all_elements if not x in minima]

	def initialize(self) -> None:
		'''
		Empties both the memory and the pipeline, and add the process self._buffer to the pipeline
		at the initial step "!" when it exists.
		'''
		for key in self.preorder.relations.keys():
			self.pipeline[key] = []
			self.memory[key] = {}
		if self.preorder.mask:
			self.pipeline["!"] = [self._buffer]
			self.memory["!"] = {}

	def erase(self,
						#List of inputs and their types
						threshold: Union[None,str] = None
						#The output type
						) -> None:
		'''
		Empties the memory.
		'''
		for key in self.preorder.relations.keys():
			if threshold == None or self.preorder.geq(threshold,key):
				self.memory[key] = {}
		if self.preorder.mask:
			self.memory["!"] = {}
