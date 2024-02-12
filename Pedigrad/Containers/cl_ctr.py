from typing import Any, Callable

class Controller(object):

	__slot__ = ("signatures","verifiers")

	def __init__(self,
							 #List of inputs and their types
							 signatures: dict[str,Any],
							 verifiers: dict[str,Callable[[Any,Any],bool]],
							 #The output type
							 ) -> None:
		#A distionary used to store authorizations
		self.signatures = signatures
		#A dictionary of functions authorizing or forbidding accesses
		self.verifiers = verifiers

	def verify(self,
						 #List of inputs and their types
						 keys: dict[str,bool]
						 #The output type
						 ) -> dict[str,bool]:
		'''
		Assigns to every key an authorization value (Boolean).
		'''
		authorized = True
		for key, val in keys.items():
			try:
				verifier = self.verifiers[key]
			except:
				verifier = lambda x,y: False
			try:
				signature = self.signatures[key]
			except:
				signature = None
			authorized = authorized and type(val) == type(signature) and verifier(val,signature)
			if not authorized: 
				break
		return authorized

