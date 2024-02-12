from __future__ import annotations
from typing import Union
from Pedigrad.Workflow.cl_pro import PreOrder
from Pedigrad.SegmentCategory.cl_itv import Interval

class SegmentObject(object):

  __slots__ = ("intervals","preorder")

  def __init__(self,
               #List of inputs and their types
               intervals: list[Interval],
               preorder: PreOrder
               #The output type
               ) -> None:
    #List of Intervals with colors
    self.intervals = sorted(intervals, key = lambda i:[i.a,i.b])
    #Pre-order structure on the colors
    self.preorder = preorder

  def is_downstream(self,
               #List of inputs and their types
               position: int
               #The output type
               ) -> bool:
    '''
    Indicates whether the segment is located after the position given as an input.
    '''
    return not self.intervals[0].contains(position)[0] if self.intervals!=[] else False

  def is_upstream(self,
               #List of inputs and their types
               position: int
               #The output type
               ) -> bool:
    '''
    Indicates whether the segment is located before the position given as an input.
    '''
    return not self.intervals[-1].contains(position)[-1] if self.intervals!=[] else False

  def index(self,
            #List of inputs and their types
            position: int,
            start: int = 0
            #The output type
            ) -> Union[int,None]:
    '''
    Returns the index of the first interval that contains the position given as an input.
    '''
    for i in range(start,len(self.intervals)):
      if all(self.intervals[i].contains(position)):
        return i
    return None

  def indices(self,
              #List of inputs and their types
              positions: list[int]
              #The output type
              ) -> dict[int,int]:
    '''
    Returns a dictionary mapping each position given in the input list to
    the index of the first interval containing that position.
    '''
    sorted_positions = sorted(positions)
    indices, last = {}, 0
    for i in range(len(sorted_positions)):
      index = self.index(sorted_positions[i],start=last)
      if index != None:
        indices[sorted_positions[i]] = index
        last = index
    return indices

  def colors(self,
             #List of inputs and their types
             positions: list[int]
             #The output type
             ) -> dict[int,list[str]]:
    '''
    Returns a dictionary mapping each position given in the input list to
    the color associated with the first interval containing that position.
    '''
    return {p:self.intervals[i].c for p,i in self.indices(positions).items()}

  def normalize(self,
                #List of inputs and their types
                interval: Interval,
                direct: bool,
                key: Callable[[str,str],list[str]]
                #The output type
                ) -> SegmentObject:
    '''
    Returns a segment whose colors are normalized by the function key and whose interval decomposition
    represents either a Venn-diagram decomposition of the underlying SegmentObject instance with the input 
    Interval instance (if direct = True) or a union of the underlying SegmentObject instance 
    with the input Interval instance (if direct = False). See the documentation for more detail.
    '''
    #Sort the intervals according to set inclusions
    sorted_intervals = sorted(self.intervals, key = lambda i:[i.a,i.b])
    #If the SegmentOBject instance is after the input interval, then returns the union
    if sorted_intervals == [] or interval << sorted_intervals[0]:
      return [interval] + sorted_intervals
    #Otherwise, we make the input interval interact with the intervals of the segment
    else:
      new_intervals = []
      #remainder is the end part of the input interval that has not interacted with the segment yet
      remainder = interval
      #Loop over the intervals of the segment
      for i in range(len(sorted_intervals)):
        #This is when the input interval does not intersect with the considered interval
        if remainder << sorted_intervals[i] or remainder >> sorted_intervals[i]:
          new_intervals.append(sorted_intervals[i])
        #This is when the input interval intersect with the considered interval
        else:
          #Depending on the value of the input "direct", we consider a concatenation or a Venn-diagram decomposition
          d = remainder & sorted_intervals[i] if direct else remainder + sorted_intervals[i]
          d = [x.normalize(key) for x in d]
          #When the remainder has a chance to interact with the next interval, the loop continues
          if remainder > sorted_intervals[i]:
            new_intervals.extend(d[:-1])
            remainder = d[-1]
          #When the remainder has no chance to interact with the next interval, the loop is ended (break)
          else:
            new_intervals.extend(d)
            new_intervals.extend(sorted_intervals[i+1:])
            remainder = None
            break
      #If the last remainder is not empty, we add it to the list of invervals
      if remainder != None:
        new_intervals.append(remainder)
      return SegmentObject(new_intervals,self.preorder)

  def maximize(self) -> SegmentObject:
    '''
    Normalizes the SegmentOjbect instance with respect to a supremum operation. 
    See documentation.
    '''
    s = SegmentObject(self.intervals[0:1],self.preorder)
    for i in range(1,len(self.intervals)):
      s = s.normalize(self.intervals[i],direct=True,key=self.preorder.sup)
    return s

  def minimize(self) -> SegmentObject:
    '''
    Normalizes the SegmentOjbect instance with respect to a infimum operation. 
    See documentation.
    '''
    s = SegmentObject(self.intervals[0:1],self.preorder)
    for i in range(1,len(self.intervals)):
      s = s.normalize(self.intervals[i],direct=False,key=self.preorder.inf)
    return s