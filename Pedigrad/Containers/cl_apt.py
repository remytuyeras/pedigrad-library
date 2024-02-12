from typing import Any, Callable

class Applicator(object):

	__slot__ = ("name","generate","increment")

	def __init__(self,
							#List of inputs and their types
							name: str,
							generate: Callable[[Any],Any],
							increment: Callable[[Any,Any],Any]
							#The output type
							) -> None:
		#Text describing the function of the Applicator description
		self.name = name
		#A function to be used as an initializer
		self.generate = generate
		#A function to stack x onto the memory y
		self.increment = increment