from __future__ import annotations
from itertools import product

class PreOrder(object):
  
  __slots__ = ("relations","closed","mask")

  def __init__(self,
              #List of inputs and their types
              relations: dict[str,list[str]],
              closed: bool = False,
              mask: bool = False
              #The output type
              ) -> None:
    #Dictionary giving a presentation for each lower set of the pre-order
    self.relations = relations
    #Boolean indicating whether the lower sets are realized
    self.closed = closed
    #Boolean indicating whether a formal initial element is added
    self.mask = mask

  def complete(self) -> None:
    '''
    Computes the transitive and reflexive closure the lower sets stored in the
    variable self.relations.
    '''
    if not self.closed:
      self.closed = True
      extrarel, not_transitive = [], True
      #Transitive completion
      while not_transitive:
        not_transitive = False
        for key, downrel in self.relations.items():
          for obj in downrel:
            extrarel = [x for x in self.relations[obj] if not x in extrarel + self.relations[key]]
            not_transitive = extrarel!=[]
            self.relations[key].extend(extrarel)
      #Reflexive completion
      for key in self.relations.keys():
        if not key in self.relations[key]:
          self.relations[key].append(key)

  def contains(self,
               #List of inputs and their types
               element: str
               #The output type
               ) -> bool:
    '''
    Indicates whether the input is an element of the preorder structure.
    '''
    return element in self.relations.keys() or element == "!" and self.mask

  def geq(self,
          #List of inputs and their types
          element1: str,
          element2: str
          #The output type
          ) -> bool:
    '''
    Indicates whether the first input is greater than or equal to the second input 
    with respect to the underlying preorder structure.
    '''
    self.complete()
    return element1 in self.relations.keys() and element2 in self.relations[element1] or element2 == "!" and self.mask
  
  def extrema(self,
              #List of inputs and their types
              elements: list[str],
              maxima: bool
              #The output type
              ) -> list[str]:
    '''
    Computes the list of extrema of a given list of elements.
    '''
    remove = []
    ext = elements
    working = True
    while working:
      working = False
      for elt1 in ext:
        for elt2 in ext:
          pair = [elt1,elt2]
          if self.geq(*pair) and not self.geq(*pair[::-1]):
            remove.append(pair[maxima])
            working = True
      ext = [x for x in ext if not x in remove]
      return ext

  def inf(self,
          #List of inputs and their types
          element1: str,
          element2: str
          #The output type
          ) -> list[str]:
    '''
    Computes the list of infima associated with a pair of elements in the preordered set.
    '''
    if (element1 == "!" or element2 == "!") and self.mask:
        return ["!"]
    self.complete()
    #This list is to contain the intersection between the lower sets of element1 and element2
    candidates = []
    #Computes the intersection of the lower sets
    for elt in self.relations[element1]:
      if elt in self.relations[element2]:
        candidates.append(elt)
    #Infima are defined as the maxima of the intersection
    infima = self.extrema(candidates,True)
    return ["!"] if infima == [] and self.mask else infima

  def sup(self,
          #List of inputs and their types
          element1: str,
          element2: str
          #The output type
          ) -> list[str]:
    '''
    Computes the list of suprema associated with a pair of elements in the preordered set.
    '''
    self.complete()
    #This list is to contain the intersection between the upper sets of of element1 and element2
    candidates = []
    #Computes the intersection of the upper sets
    for key, lwr in self.relations.items():
      if element1 == "!" and self.mask:
        return [element2]
      elif element2 == "!" and self.mask:
        return [element1]
      elif element1 in lwr and element2 in lwr:
        candidates.append(key)
    #Suprema are defined as the minima of the intersection
    return self.extrema(candidates,False)

  def __mul__(self,
              #List of inputs and their types
              preorder: PreOrder
              #The output type
              ) -> PreOrder:
    '''
    Returns a PreOrder instance representing a Cartesian product of self with the preorder
    structure given as an input.
    '''
    #Completion is necessary to compute the elements of the product preorder
    self.complete()
    preorder.complete()
    #Turn the returned generators into lists
    keys1 = list(self.relations.keys())
    keys2 = list(preorder.relations.keys())
    #Computes the numbers of product components already involved in the inputs
    n1 = len(keys1[0].split(",")) if keys1 != [] else 0
    n2 = len(keys2[0].split(",")) if keys2 != [] else 0
    #List of elements belonging to the product structure
    keys = list(product(keys1,keys2))
    #Intializes the dictionary that will contain the lower sets of the product structure
    relations = {}
    #Computes the products between the non-initial elements of the preorders
    for key in keys:
      relations[",".join(key)] = [",".join(x) for x in product(self.relations[key[0]],preorder.relations[key[1]])]
    #Computes the products the non-initial and initial elements
    if preorder.mask:
      for key in keys1:
        relations[key + ",!"*n2] = [x + ",!" for x in self.relations[key]]
    #Computes the products the initial and non-initial elements
    if self.mask:
      for key in keys2:
        relations["!,"*n1 + key] = ["!," + x for x in preorder.relations[key]]
    #If the two preorders have formal initial elements, so do their product
    mask = self.mask and preorder.mask
    return PreOrder(relations,True,mask)
    
