#------------------------------------------------------------------------------
#name (Class) | 5 objects | 4 methods
#------------------------------------------------------------------------------
'''
[Objects] 
  .env      [Type] Environment
  .Seg      [Type] CategoryOfSegments
  .indiv    [Type] list
  .base     [Type] list(SegmentObject)
  .database [Type] list('a)

[Methods] 
  .__init__
        [Inputs: 4]
          - env       [Type] Environment
          - indiv     [Type] list
          - base      [Type] list(SegmentObject)
          - database  [Type] list('a)
        [Outputs: 0]
  .eval
        [Inputs: 1]
          - segment   [Type] SegmentObject
        [Outputs: 1]
          - return    [Type] 'a
  .extending_diagram
        [Inputs: 1]
          - segment   [Type] SegmentObject
        [Outputs: 1]
          - outputs   [Type] list(int * MorphismOfSegments)
  .ran
        [Inputs: 1]
          - cat_item    [Type] CategoryItem
        [Outputs: 1]
          - outputs         [Type] 'a
        
[General description] 
  This structure models the features of a sequence alignment functor, as defined in CTGI. The images of the sequence alignment functor are stored in the object [database] and can be queried throught the method [eval]. The method also computes the images of the right Kan extension of this functor through the method [ran] (TO BE CODED). The extending diagram (see CTGI) used to compute this right Kan extension can be computed through the method [extending_diagram] (TO BE COMPLETED WITH ARROWS).
    
>>> Method: .__init__
  [Actions] 
    .env      <- use(env)
    .Seg      <- use(PreOrder,CategoryOfSegments,self.env)
    .indiv    <- use(indiv)
    .base     <- use(base)
    .database <- use(database)
  [Description] 
    This is the constructor of the class.

>>> Method: .eval
  [Actions] 
    .return      <- use(segment,self.Seg,self.base,self.database)
  [Description] 
    This method returns the image of the sequence alignment functor for the given input SegmentObject item.

>>> Method: .extending_diagram
  [Actions] 
    .return      <- use(segment.self.Seg,self.base)
  [Description] 
    This method computes the objects of the extending diagram (see CTGI) for compting the right Kan extension of the functor encoded by the method self.eval.

>>> Method: .ran
  [Actions] 
    .return      <- use(cat_item,self.extending_diagram)
  [Description] 
    This method computes the images of the right Kan extension of the functor encoded by the method self.eval. [TO BE CODED]
'''
#------------------------------------------------------------------------------
#Dependencies: current, SegmentCategory
#------------------------------------------------------------------------------
import sys
sys.path.insert(0, '../SegmentCategory/')
from cl_pro import PreOrder
from cl_cos import CategoryOfSegments
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class SequenceAlignment(object): 
#------------------------------------------------------------------------------  
  def __init__(self,env,indiv,base,database):
    self.env = env
    preorder = PreOrder('cartesian',self.env.spec,self.env.Seg.preorder)
    self.Seg = CategoryOfSegments(preorder)
    self.indiv = indiv
    self.base = base
    self.database = database
#------------------------------------------------------------------------------  
  def eval(self,segment):
    for i in range(len(self.base)):
      if self.Seg.identity(segment,self.base[i]):
        return self.database[i]
        break
    return list()
#------------------------------------------------------------------------------     
  def extending_diagram(self,segment):
    outputs = list()
    for i in range(len(self.base)):
      for m in self.Seg.homset(segment,self.base[i]):
        outputs.append((i,m))  
    return outputs
#------------------------------------------------------------------------------   
  def ran(self,cat_item):
    {}
#------------------------------------------------------------------------------
