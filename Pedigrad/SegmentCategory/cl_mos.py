from __future__ import annotations
from Pedigrad.SegmentCategory.cl_ifn import IntFunction

class MorphismOfSegments(object): 

  __slots__ = ("f0","f1")

  def __init__(self,
               #List of inputs and their types
               f0: IntFunction,
               f1: IntFunction
               #The output type
               ) -> None:
    #IntFunction defined on the domain of the segment           
    self.f0 = f0
    #IntFunction defined on the patches of the segment
    self.f1 = f1
  
  def is_valid(self) -> bool:
    return self.f0.is_valid() and self.f1.is_valid() and self.f1.is_surjective()

  def is_surjective(self) -> bool:
    return self.f0.is_surjective()

  def is_injective(self) -> bool:
    return self.f0.is_injective() and self.f1.is_injective()

  def is_identity(self) -> bool:
    return self.f0.is_identity() and self.f1.is_identity()

  def clean(self) -> None:
    self.f0.clean()
    self.f1.clean()

  def merge(self,
            #List of inputs and their types
            inputs: list[int]
            #The output type
            ) -> MorphismOfSegments:
    f0_ = IntFunction(self.f0.target,self.f0.target,{})
    f1_ = self.f1.merge(inputs)
    return MorphismOfSegments(f0_,f1_)
  
  def detach(self,
             #List of inputs and their types
             inputs: list[int]
             #The output type
             ) -> MorphismOfSegments:
    f0_ = IntFunction(self.f0.target,self.f0.target,{})
    f1_ = self.f1.detach(inputs)
    return MorphismOfSegments(f0_,f1_)

  def insert(self,
             #List of inputs and their types
             shifts: dict[int,int]
             #The output type
             ) -> MorphismOfSegments:
    f0_ = self.f0.insert(shifts)
    f1_ = IntFunction(self.f1.target,self.f1.target,{})
    return MorphismOfSegments(f0_,f1_)

  def remove(self,
             #List of inputs and their types
             shifts: dict[int,int]
             #The output type
             ) -> MorphismOfSegments:
    f0_ = self.f0.remove(shifts)
    f1_ = IntFunction(self.f1.target,self.f1.target,{})
    return MorphismOfSegments(f0_,f1_)

  def __mul__(self,
              #List of inputs and their types
              mos: MorphismOfSegments
              #The output type
              ) -> MorphismOfSegments:
    return MorphismOfSegments(self.f0 * mos.f0,self.f1 * mos.f1)
