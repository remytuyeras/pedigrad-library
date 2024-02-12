from __future__ import annotations
from typing import Union
from Pedigrad.SegmentCategory.cl_so import SegmentObject
from Pedigrad.SegmentCategory.cl_itv import Interval
from Pedigrad.SegmentCategory.cl_dos import DiagramOfSegments
from Pedigrad.Workflow.cl_pro import PreOrder
from Pedigrad.Combinatorics.cl_z3 import Z3
from Pedigrad.Combinatorics.cl_z3m import Z3matrix

class SeqData(DiagramOfSegments):

  __slots__ = ("labels","sequences","objects","arrows","analyses","graph","selected","current")

  def __init__(self,
               #List of inputs and their types
               label: Union[None,str] = None,
               sequence: Union[None,str] = None
               #The output type
               ) -> None:
    self.labels: list[str] = [label] if label != None else []
    self.sequences: list[list[str]] = [[sequence]] if sequence != None else []
    intervals = [Interval(x+1,x+1,[str(x+1)]) for x in range(len(sequence))] if sequence != None else []
    preorder = PreOrder({str(x+1):[] for x in range(len(sequence))},mask = True) if sequence != None else PreOrder({},mask = False)
    segment = SegmentObject(intervals,preorder)
    super(SeqData,self).__init__(segment)
  
  def __xor__(self,sqdt: SeqData) -> bool:
    seg1 = self.objects[self.current].intervals
    seg2 = sqdt.objects[sqdt.current].intervals
    n = max(len(seg1),len(seg2))
    return n == len(seg1) == len(seg2) and \
                all([seg1[i].a == seg2[i].a and seg1[i].b == seg2[i].b and \
                seg1[i].c == seg2[i].c for i in range(n)])

  def __or__(self,sqdt: SeqData) -> SeqData:
    output = SeqData()
    n = max(len(self.labels),len(sqdt.labels))
    if self ^ sqdt and n == len(self.labels) == len(sqdt.labels):
      output.sequences.extend([self.sequences[i]+sqdt.sequences[i]  for i in range(n) if self.labels[i] == sqdt.labels[i]])
      output.labels.extend(self.labels)
      super(SeqData,output).__init__(self.objects[self.current])
    return output

  def __and__(self,sqdt: SeqData) -> SeqData:
    output = SeqData()
    n = max(len(self.labels),len(sqdt.labels))
    if self ^ sqdt:
      output.sequences.extend(self.sequences+sqdt.sequences)
      output.labels.extend(self.labels+sqdt.labels)
      super(SeqData,output).__init__(self.objects[self.current])
    return output

  def matrix(self) -> Z3matrix:
    #Use containers?
    #I need to use a cone, like in the paper!!
    current_segment = self.objects[self.current]
    colors = []
    record = []
    for I in current_segment.intervals:
      if I.c == ["!"]:
        continue
      record.append({})
      colors.append(":".join(I.c))
      for align in self.sequences:
        for s in align:
          record[-1].setdefault(s[I.a-1:I.b],len(record[-1].keys()))
    prematrix = []
    for align in self.sequences:
      row = []
      for i,I in enumerate(current_segment.intervals):
        m = [0] * len(record[i].keys())
        for s in align:
          m[record[i][s[I.a-1:I.b]]] = 1
        row.extend([Z3(c,0) for c in m])
      prematrix.append(row)
    col_labels = [colors[i] for i in range(len(colors)) for _ in range(len(record[i].keys()))]
    return Z3matrix(prematrix,self.labels,col_labels).transpose(), record

  def __mul__(self) -> SeqData:
    #Computes Pairwise alignment
    #What if the input sequence has the point "-"?
    #Align with current segment
    #Alignments always provide the same semgnet length, with all symmetries (given by morphisms)
    #In this case, easy to compute Ran
    #Diagram needs to contain the diagram for the Ran
    #2 sequences easy
    #3 less easy
    #use only current
    #[[sequenceA_sym],[sequenceB_sym],[sequenceC_sym]]
    return
  
  def __getitem__(self,i: int): #
    #CTGI: i-slice
    return
  
  def integrate(self,i: int): #
    #Compute the limit wrt to the cone of the diagram.
    return