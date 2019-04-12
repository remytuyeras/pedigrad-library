#------------------------------------------------------------------------------
#CategoryOfSegments (Class) | 1 object | 4 methods
#------------------------------------------------------------------------------
'''
[Objects] 
  .preorder [Type] PreOrder

[Methods] 
  .__init__
        [Inputs: 1]
          - preorder [Type] PreOrder
        [Outputs: 0]
  .identity
        [Inputs: 2]
          - segment1  [Type] SegmentObject
          - segment2  [Type] SegmentObject
        [Outputs: 1]
          - return    [Type] bool
  .initial
        [Inputs: 2]
          - domain  [Type] int
          - color   [Type] list('a)
        [Outputs: 1]
          - return  [Type] SegmentObject
  .homset
        [Inputs: 2]
          - source  [Type] SegmentObject
          - target  [Type] SegmentObject
        [Outputs: 1]
          - homset  [Type] list(MorphismOfSegments)
                
[General description] 
  This structure models the features of a category of segments. The class is initialized by passing a PreOrder item to its constructor and allows one to know or compute information related to a category structure. The method [identity] returns a Boolean value that specificies whether there may exist an identity morphism between two SegmentObject items (these may be saved in different places in the memory); the method [initial] returns an local initial object in the category, where the local aspect is determined by the colors of the segment; the method [homset] computes the hom-set of a pair of SegmentObject items. 
    
>>> Method: .__init__
  [Actions] 
    .preorder  <- use(preorder)
  [Description] 
    This is the constructor of the class.

>>> Method: .identity
  [Actions] 
    return    <- use(segment1,segment2)
  [Description] 
    Specifies whether there is an identity morphisms from [segment1] to [segment2].
    
>>> Method: .initial
  [Actions] 
    return    <- use(SegmentObject,domain,topology,colors)
  [Description] 
    Returns a local initial object with a uniform color equal to [color].

>>> Method: .homset
  [Actions] 
    homset    <- use(.preorder,source,target)
  [Description] 
    Returns the hom-set associated with the pair of objects ([source],[target]).
'''
#------------------------------------------------------------------------------
#Dependencies: current, Useful
#------------------------------------------------------------------------------
from cl_pro import PreOrder
from cl_so import SegmentObject
from cl_mos import MorphismOfSegments

import sys
sys.path.insert(0, '../Useful/')
from usf import usf
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class CategoryOfSegments(object): 
#------------------------------------------------------------------------------  
  def __init__(self,preorder):
    self.preorder = preorder
#------------------------------------------------------------------------------
  def identity(self,segment1,segment2):
    return (segment1.domain == segment2.domain) \
    and    (segment1.topology == segment2.topology) \
    and    (segment1.colors == segment2.colors)
#------------------------------------------------------------------------------    
  def initial(self,domain,color):
    topology = list()
    colors = list()
    for i in range(domain):
      topology = topology + [(i,i)]
      colors = colors + [color]
    return SegmentObject(domain,topology,colors)
#------------------------------------------------------------------------------
  def homset(self,source,target):
    homset = list()
    if target.domain-source.domain >= 0:
      for i in usf.inclusions(0,target.domain,target.domain-source.domain):
        arrow = MorphismOfSegments(source,target,i,self.preorder.geq)
        if arrow.defined:
          homset.append(arrow)
    return homset
#------------------------------------------------------------------------------
