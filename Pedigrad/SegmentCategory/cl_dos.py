# from __future__ import annotations
from Pedigrad.SegmentCategory.cl_itv import Interval
from Pedigrad.SegmentCategory.cl_so import SegmentObject
from Pedigrad.SegmentCategory.cl_ifn import IntFunction
from Pedigrad.SegmentCategory.cl_mos import MorphismOfSegments
from Pedigrad.Workflow.cl_pro import PreOrder

ConeType = tuple[SegmentObject,list[SegmentObject],list[MorphismOfSegments]]

class DiagramOfSegments(object): 
  
  __slots__ = ("objects","arrows","analyses","graph","selected","current")

  def __init__(self,
               #List of inputs and their types
               segment: SegmentObject
               #The output type
               ) -> None:
    #Essential
    self.objects: list[SegmentObject] = [segment]
    self.current: int = 0
    #Useful
    self.analyses: list[list[str]] = [["initial"]]
    #Extra
    n = len(segment.intervals)
    morphism = MorphismOfSegments(IntFunction(n,n,{}),IntFunction(n,n,{}))
    #Suggestion below: Integrate the graph structure in the arrows structure
    self.arrows: list[MorphismOfSegments] = [morphism]
    self.graph: PreOrder = PreOrder({"doc_0":["doc_0"]},mask=False) #whole diagram
    #Fancy
    self.selected: PreOrder = PreOrder({},mask=False) #cone

  def merge(self,
            #List of inputs and their types
            inputs: list[tuple[int,int]]
            #The output type
            ) -> None:
    segment = self.objects[self.current]
    for i,j in inputs:
      segment = segment.normalize(Interval(i,j),direct=False,key = lambda x,y:[x+":"+y])
    self.objects.append(segment)
    self.current += 1
  
  def detach(self,
             #List of inputs and their types
             inputs: list[int]
             #The output type
             ) -> None:
    pass

  def insert(self,
             #List of inputs and their types
             shifts: dict[int,int]
             #The output type
             ) -> None:
    pass

  def remove(self,
             #List of inputs and their types
             shifts: dict[int,int]
             #The output type
             ) -> None:
    pass

  def history(self) -> list[str]:
    pass

  def gobackto(self,
               #List of inputs and their types
               read: int
               #The output type
               ) -> None:
    pass

  def select(self,
             #List of inputs and their types
             read: int
             #The output type
             ) -> None:
    pass

  def forget(self,
             #List of inputs and their types
             read: int
             #The output type
             ) -> None:
    pass

  def limit(self) -> ConeType:
    #COmpute the limit of selected
    pass

