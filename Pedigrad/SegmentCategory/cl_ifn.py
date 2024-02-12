from __future__ import annotations

class IntFunction(object):

  __slots__ = ("source","target","mapsto")

  def __init__(self,
               #List of inputs and their types
               source: int,
               target: int,
               mapsto: dict[int,int]
               #The output type
               ) -> None:
    self.source = source
    self.target = target
    self.mapsto = mapsto

  def is_valid(self) -> bool:
    return self.map([self.source-1])[0] < self.target and all([k < self.source and (v >= -1 if k>0 else v >= 0) for k,v in self.mapsto.items()])

  def is_surjective(self) -> bool:
    return self.map([self.source-1])[0] == self.target-1 and all([k < self.source and (-1 <= v <= 0 if k>0 else v == 0) for k,v in self.mapsto.items()])

  def is_injective(self) -> bool:
    return self.map([self.source-1])[0] < self.target and all([k < self.source and v >= 0 for k,v in self.mapsto.items()])

  def is_identity(self) -> bool:
    return self.source == self.target and all([k < self.source and v == 0 for k,v in self.mapsto.items()])

  def clean(self) -> None:
    self.mapsto = {k:v for k, v in sorted(self.mapsto.items(), key = lambda x: x[0]) if v!= 0}

  def merge(self,
            #List of inputs and their types
            inputs: list[int]
            #The output type
            ) -> IntFunction:
    '''
    Merges the images f(k) of the elements k given in the input to the images f(k-1) of their 
    predecessors. See the documentation for more detail.
    '''
    #The variable mapsto contains the dictionary defining the output IntFunction
    mapsto = {x:-1 for x in self.map(inputs) if not x in self.map([0])}
    changed = []
    for x in inputs:
      if x != 0:
        #Merge the image of the argument with the image of the preceding argument
        self.mapsto[x] = -1
        changed.append(x)
    #Define the domains and codomains of the underlying factorization
    old_target = self.target
    self.target -= len(changed)
    return IntFunction(old_target,self.target,mapsto)

  def detach(self,
            #List of inputs and their types
            inputs: list[int]
            #The output type
            ) -> IntFunction:
    '''
    Detaches the images f(k) of the elements k given in the input from the images f(k-1) of their predecessors provided
    that these images are initially equal; i.e. f(k) = f(k-1). See the documentation for more detail.
    '''
    changed = []
    for x in inputs:
      #Find merged images
      if self.mapsto[x] == -1:
        #Detach the image of the current argument from the image of the previous argument
        self.mapsto[x] = 0
        changed.append(x)
    #Define the domains and codomains of the underlying factorization
    old_target = self.target
    self.target += len(changed)
    #The variable mapsto contains the dictionary defining the output IntFunction
    mapsto = {x:-1 for x in self.map(changed)}
    return IntFunction(self.target,old_target,mapsto)

  def insert(self,
             #List of inputs and their types
             shifts: dict[int,int]
             #The output type
             ) -> IntFunction:
    '''
    Distances images f(k) and f(k-1) by an additional distance equal to shift[k]. 
    See the documentation for more detail.
    '''
    valid = [key for key in sorted(shifts.keys()) if shifts[key] > 0]
    images = self.map(valid)
    #The variable mapsto contains the dictionary defining the output IntFunction
    mapsto, inserted = {}, 0
    for i in range(len(images)):
      s = shifts[valid[i]]
      #The shift specified in the input inserts a correpsonding number of elements
      mapsto[images[i]] = s
      inserted += s
      try:
        self.mapsto[valid[i]] += s
      except:
        self.mapsto[valid[i]] = s
    #Define the domains and codomains of the underlying factorization
    old_target = self.target
    self.target += inserted
    return IntFunction(old_target,self.target,mapsto)

  def remove(self,
             #List of inputs and their types
             shifts: dict[int,int]
             #The output type
             ) -> IntFunction:
    '''
    Shortens the dictance between the images f(k) and f(k-1) by an value equal to shift[k]. 
    See the documentation for more detail.
    '''
    valid = []
    for key in sorted(shifts.keys()):
      try:
        if 0 < shifts[key] <= self.mapsto[key]:
          valid.append(key)
      except:
          continue
    images = self.map(valid)
    #The variable mapsto contains the dictionary defining the output IntFunction
    mapsto, removed = {}, 0
    for i in range(len(images)):
      s = shifts[valid[i]]
      #The shift specified in the input removes a correpsonding number of elements
      self.mapsto[valid[i]] -= s
      removed += s
    #Define the domains and codomains of the underlying factorization
    old_target = self.target
    self.target -= removed
    mapsto = {x:shifts[valid[i]] for i,x in enumerate(self.map(valid))}
    return IntFunction(self.target,old_target,mapsto)

  def map(self,
          #List of inputs and their types
          inputs: list[int]
          #The output type
          ) -> list[int]:
    '''
    Orders the input list and outputs the list of images of each ordered inputs via the mappings 
    of the underlying IntFunction instance. See the documentation for more detail.
    '''
    increment_before, increment_after = 0, 0
    outputs, unprocessed = [], sorted(inputs)
    #Loop computing the images wrt to the shifts provided in the dictionary self.mapsto
    for key in sorted(self.mapsto.keys()):
      #Shift before the mapping at the integer "key"
      increment_before = increment_after
      #Shift after the mapping at the integer "key" (and before the nbext mapping)
      increment_after += self.mapsto[key]
      #We start at -1 to address subsequent list truncations at index+1 = 0 (see after the for-loop)
      index = -1
      #Shift images according to the shift values stored in self.mapsto
      for i, x in enumerate(unprocessed):
        if x < key:
          outputs.append(x + increment_before)
          index = i
        if x == key:
          outputs.append(x + increment_after)
          index = i
        if x > key:
          break
      #The rest of the input to process
      unprocessed = unprocessed[index+1:]
    #When the loop ends, computes the rest of the images wrt to the last shift value
    for x in unprocessed:
      outputs.append(x + increment_after)
    return outputs
  
  def __mul__(self,
              #List of inputs and their types
              intfunction: IntFunction
              #The output type
              ) -> IntFunction:
    '''
    Permits to compose InFunction instances (in a category-theoretic sense). 
    See documentation.
    '''
    f = self.map(range(self.source))
    g = intfunction.map(range(intfunction.source))
    fg = [f[g[i]] for i in range(intfunction.source)]
    return IntFunction.convert(fg,self.target)

  @classmethod
  def convert(cls,
          #List of inputs and their types
          intlist: list[int],
          target: int
          #The output type
          ) -> IntFunction:
    '''
    Turns a list of non-negative integers into an IntFunction instance such that the
    input list is the list of images of the IntFuction instance returned.
    '''
    increment, distance = 0, 0
    #Dictionary associated with the  IntFunction instance
    mapsto = {}
    for i in range(len(intlist)):
      #The value used to define the dictionary at i
      distance = intlist[i]-(i+increment)
      increment += distance
      #Zero values for the dictionary are ignored
      if distance != 0:
        mapsto[i] = distance
    return cls(len(intlist),target,mapsto)

