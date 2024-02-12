from typing import Any, Callable, Union
from Pedigrad.Containers.cl_tre import Tree

FunList = Callable[[Any,Any],Union[None,list[Any]]]
FunBool = Callable[[Any,Any],bool]
TreeFun = Callable[[Tree,Tree],Any]

def Arborealize(#List of inputs and their types
								Category: int, 
								Trivial: Callable[[],Any] = None
								#The output type
								) -> Union[None,Callable[[Union[FunBool,FunList]],TreeFun]]:
	'''
	Returns different decorators depending on the value passed to the argument "Category".
	'''
	def decorator1(f: FunBool) -> TreeFun:
		'''
		The function "decorator1" is meant to be used as a decorator to extend the 
		arguments of a function "f" to Tree instances. See documentation for more detail.
		'''
		def wrapper(tree1: Tree,tree2: Tree) -> bool:
			#The function "f" is applied on the contents of the input trees
			output = f(tree1.content,tree2.content)
			#If the output of applying "f" is True, then one proceeds to the children
			if output and tree1.children != None:
				#If the second tree does not have children at the correspoding level, one creates them
				if tree2.children == None:
					tree2.children = [Tree(Trivial()) for _ in range(len(tree1.children))]
				#Each child in the first tree is compared to the children of the second tree
				for i, child1 in enumerate(tree1.children):
					flag = False
					for j, child2 in enumerate(tree2.children):
						#Recursive call on the present function "wrapper"
						flag = wrapper(child1,child2)
						if flag:
							break
					if not flag:
						#If none of the children pairings returned the value True, then a new child is created
						tree2.children.append(Tree(Trivial()))
						#For this last pairing, either False or True can be returned
						wrapper(child1,tree2.children[-1])
			#The boolean value returned by "f" is returned here
			return output

		return wrapper

	def decorator2(f: FunList) -> TreeFun:
		'''
		The function "decorator2" is meant to be used as a decorator to extend the
		arguments of a function "f" to Tree instances. See documentation for more detail.
		'''
		def wrapper(tree1: Tree,tree2: Tree) -> Union[None,list[Any]]:
			#The function "f" is applied on the contents of the input trees
			output = f(tree1.content,tree2.content)
			#If the output of applying "f" exists, then one proceeds to the children
			if output != None and tree1.children != None:
				#The proceed stops where the second input tree stops
				if tree2.children != None:
					#Each child in the first tree is compared to the children of the second tree
					for i, child1 in enumerate(tree1.children):
						tmp = None
						for j, child2 in enumerate(tree2.children):
							tmp = wrapper(child1,child2)
							if tmp != None:
								break
						output.append(tmp)
			#The ouput returned by "f" is returned here
			return output

		return wrapper

	#Returns "decorator1" or "decorator2" depending on the value of "Category"
	if Category == 1:
		return decorator1
	if Category == 2:
		return decorator2
