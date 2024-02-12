from __future__ import annotations
from typing import Callable

class Interval(object):

  __slots__ = ("a","b","c")

  def __init__(self,
               #List of inputs and their types
               x: int,
               y: int,
               colors: list[str] = []
               #The output type
               ) -> None:
    #Left border of the interval (included)
    self.a = min(x,y)
    #Right border of the interval (included)
    self.b = max(x,y)
    #Extra information
    self.c = colors

  def __str__(self) -> str:
    return f"[{self.a},{self.b}]("+",".join(self.c) +")"

  def contains(self,
               #List of inputs and their types
               x: int
               #The output type
               ) -> tuple[bool,bool]:
    return (self.a<=x,x<=self.b)

  def __lshift__(self,
                 #List of inputs and their types
                 interval: Interval
                 #The output type
                 ) -> bool:
    return self.b < interval.a

  def __rshift__(self,
                 #List of inputs and their types
                 interval: Interval
                 #The output type
                 ) -> bool:
    return self.a > interval.b

  def __lt__(self,
             #List of inputs and their types
             interval: Interval
             #The output type
             ) -> bool:
    return self.a < interval.a

  def __gt__(self,
             #List of inputs and their types
             interval: Interval
             #The output type
             ) -> bool:
    return self.b > interval.b

  def __le__(self,
             #List of inputs and their types
             interval: Interval
             #The output type
             ) -> bool:
    '''
    Indicates whether the underlying SegmentOjbect instance is adjacent to the input instance.
    '''
    return self.b+1 == interval.a

  def __ge__(self,
             #List of inputs and their types
             interval: Interval
             #The output type
             ) -> bool:
    '''
    Indicates whether the underlying SegmentOjbect instance is adjacent to the input instance.
    '''
    return self.a-1 == interval.b
  
  def __add__(self ,
             #List of inputs and their types
             interval : Interval
             #The output type
             ) -> list[Interval]:
    '''
    Returns the best representation of a concatenation between the underlying SegmentObject
    instance (self) and the input instance: if the two intervals are not adjacent to each other,
    then a list containing the two SegmentObject instances is returned.
    '''
    if (self << interval or self >> interval) and not(self <= interval or self >= interval):
      return sorted([self,interval])
    else:
      return [Interval(min(self.a,interval.a),max(self.b,interval.b),self.c+interval.c)]

  def __and__(self,
              #List of inputs and their types
              interval: Interval
              #The output type
              ) -> list[Interval]:
    '''
    Returns the Venn-diagram decomposition associated with the combination
    of the underlying SegmentObject instance (self) and the input instance.
    '''
    if self << interval or self >> interval:
      return sorted([self,interval])
    else:
      inter = Interval(max(self.a,interval.a),min(self.b,interval.b),self.c+interval.c)
      A1 = [Interval(self.a,inter.a-1,self.c)] if self < inter else []
      A2 = [Interval(interval.a,inter.a-1,interval.c)] if interval < inter else []
      B1 = [Interval(inter.b+1,self.b,self.c)] if self > inter  else []
      B2 = [Interval(inter.b+1,interval.b,interval.c)] if interval > inter  else []
      return A1 + A2 + [inter] + B1 + B2

  def normalize(self,
                #List of inputs and their types
                key: Callable[[str,str],list[str]]
                #The output type
                ) -> Interval:
    '''
    Reduces the list of colors associated with the underlying SegmentObject instance to 
    a singleton list by using the mappings provided by the function key (not necessarily
    deterministic)
    '''
    previous_c = []
    #The initial set of colors is the initial step in the reduction loop
    new_c = self.c
    #Reduction loop to reduce new_c to a singleton list
    while len(new_c) > 1:
      previous_c = new_c
      new_c = []
      for i in range(1,len(previous_c)):
        #Overall, this step allow us to reduce the number of colors by 1
        u = key(previous_c[0],previous_c[i])
        #If key provides a non-deterministic mapping, then the loop is aborted and no color is provided
        if len(u) != 1:
          return Interval(self.a,self.b,[])
        #The new list of colors contains at most len(previous_c)-1 elements
        new_c.append(u[0])
    #At this stage, new_c should be a singleton list
    return Interval(self.a,self.b,new_c)
