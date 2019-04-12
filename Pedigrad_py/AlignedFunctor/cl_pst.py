#------------------------------------------------------------------------------
#PointedSet (Class) | 2 objects | 2 methods
#------------------------------------------------------------------------------
'''
[Objects]
  .symbols  [Type] list('a)
  .index    [Type] int

[Methods] 
  .__init__
        [Inputs: 2]
          - symbols [Type] list('a)
          - index [Type] int
        [Outputs: 0]
  .point
        [Inputs: 0]
        [Outputs: 1]
          - return [Type] 'a
           
[General description] 
  This structure models the features of a pointed set. It is made of an object [symbols] containing a list of the elements of the underlying set, and an object [index] giving the index at which the point of the pointed set is located whithin [symbols].
    
>>> Method: .__init__
  [Actions] 
    .symbols  <- use(symbol)
    .index <- use(index)
  [Description] 
    This is the constructor of the class.

>>> Method: .point
  [Actions] 
    .return  <- use(self.symbol,self.index)
  [Description] 
    Returns the symbol of the point of the pointed structure.
    
'''
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class PointedSet(object): 
#------------------------------------------------------------------------------
  def __init__(self,symbols,index):
    self.symbols = symbols
    if not(index in range(len(self.symbols))):
      self.index = 0
      self.symbols = ['*'] + self.symbols
    else:
      self.index = index
#------------------------------------------------------------------------------
  def point(self):
    return self.symbols[self.index]
#------------------------------------------------------------------------------
