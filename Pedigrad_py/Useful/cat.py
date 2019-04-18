#------------------------------------------------------------------------------
#CategoryItem (Class) | 3 objects | 1 methods
#------------------------------------------------------------------------------
'''
[Objects] 
  .name [Type] type
  .level  [Type] int
  .source [Type] CategoryItem
  .target [Type] CategoryItem

[Methods] 
  .__init__
        [Inputs: +1]
          - level [Type] int
          - *args [Type] list(CategoryItem)
        [Outputs: 0]
           
[General description] 
  This structure models the diagrammatic features of the elements of a category. The class is equipped with an object [level] that can be used to model the polymorphic nature functors, namely both arrows and objects (of the considered category) can be given to a function as [CategoryItem] items and can be handled differently depending on their value stored in the object [level].
    
>>> Method: .__init__
  [Actions] 
    .level  <- use(level)
    .source <- use(args[0])
    .source <- use(args[1])
  [Description] 
    This is the constructor of the class.


'''
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class CategoryItem(object):
  def __init__(self,level,*args):
    self.level = level
    if len(args) == 2 and args[0].level == level-1 and args[1].level == level-1:
      self.source = args[0]
      self.target = args[1]
#------------------------------------------------------------------------------
