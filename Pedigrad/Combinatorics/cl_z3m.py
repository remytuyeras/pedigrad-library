from __future__ import annotations
from typing import Union
from Pedigrad.Combinatorics.cl_z3 import Z3

class Z3matrix(object):

  __slots__ = ("matrix","row_labels","col_labels")

  def __init__(self,
               #List of inputs and their types
               matrix: list[list[Z3]],
               row_labels: Union[None,list[str]] = None,
               col_labels: Union[None,list[str]] = None
               #The output type
               ) -> None:
    self.matrix = matrix
    self.row_labels = row_labels
    self.col_labels = col_labels


  def __str__(self) -> str:
    s = "Z3matrix("
    for i in range(len(self.matrix)):
      if i >0:
        s = s + "\t "
      name = " "+str(self.row_labels[i]) if self.row_labels != None and i < len(self.row_labels) else ""
      inside = self.matrix[i] if len(self.matrix[i]) <= 7 else self.matrix[i][:3] + ["..."]+ self.matrix[i][-3:]
      s = s + "[" + ",\t".join(map(str,inside)) + "]" + name
      if i <len(self.matrix)-1:
        s = s + ",\n"
    s = s + "\n)"
    return s

  def dim(self) -> tuple[int,int]:
    n = len(self.matrix)
    m = len(self.matrix[0]) if n > 0 else 0
    return (n,m)

  def col(self,
          #List of inputs and their types
          j: int
          #The output type
          ) -> Z3matrix:
    n, _ = self.dim()
    return Z3matrix([[self.matrix[i][j]] for i in range(n)],self.row_labels,self.col_labels[j:j+1])

  def row(self,
          #List of inputs and their types
          i: int
          #The output type
          ) -> Z3matrix:
    _, m = self.dim()
    return Z3matrix([[self.matrix[i][j] for j in range(m)]],self.row_labels[i:i+1],self.col_labels)

  def transpose(self) -> Z3matrix:
    matrix = list()
    n,m = self.dim()
    for j in range(m):
      row = list()
      for i in range(n):
        row.append(self.matrix[i][j])
      matrix.append(row)
    return Z3matrix(matrix,self.col_labels,self.row_labels)

  def __mul__(self,
              #List of inputs and their types
              matrix: Z3matrix
              #The output type
              ) -> Z3matrix:
    matrix_prod = list()
    n,m = self.dim()
    m,p = matrix.dim()
    for i in range(n):
      matrix_row = list()
      for j in range(p):
        r = self.row(i).matrix
        c = matrix.col(j).matrix
        a = Z3(0,0)
        for k in range(m):
          a = a + r[0][k] * c[k][0]
        matrix_row.append(a)
      matrix_prod.append(matrix_row)
    return Z3matrix(matrix_prod,self.row_labels,matrix.col_labels)

  def REF(self,generators: Union[None,list[int]] = None) -> Z3matrix:
    matrix = []
    for i, row in enumerate(self.matrix):
      pivots = [len(row)-1] if generators == None else generators
      if not (True in [row[k] != Z3(0,0) for k in pivots]):
        continue
      pivot = False
      updown = False
      all_zero = True
      new_row = []
      for j, x in enumerate(row):
        if all_zero and x != Z3(0,0):
          all_zero = False
        if not updown and x == Z3(1,1):
          updown = True
        if not pivot and x == Z3(0,1):
          pivot = True
        if pivot:
          new_row.append(self.matrix[i][j] * Z3(0,1))
        else:
          new_row.append(self.matrix[i][j])
      if not updown or all_zero:
        matrix.append((i,new_row))
    matrix_ = sorted(matrix,key=lambda x:x[1])
    row_labels = [self.row_labels[i] for i,x in matrix_]
    return Z3matrix([x for i,x in matrix_],row_labels,self.col_labels)

  def conflicts(self,generators: Union[None,list[int]] = None):
    conflicts_output = {s: False for s in self.row_labels}
    for i, row in enumerate(self.matrix):
      if not conflicts_output[self.row_labels[i]]:
        conflict = True
        for j, coef in enumerate(row):
          pivots = [len(row)-1] if generators == None else generators
          if coef != Z3(0,0) and not j in pivots:
            conflict = False
            break
        if conflict:
          conflicts_output[self.row_labels[i]] = True
    return {k:v for k,v in sorted(conflicts_output.items())}
        
  def null_space(self,labels) -> None:
    equations = {}
    ref_matrix = self.REF()
    for i in range(len(ref_matrix.matrix)):
      pivot = None
      for j, x in enumerate(ref_matrix.matrix[i]):
        if pivot == None and x == Z3(1,0):
          pivot = labels[j]
          if pivot in equations.keys():
            equations[pivot][i] = {"+":[],"-":[]}
          else:
            equations[pivot] = {i:{"+":[],"-":[]}}
        elif pivot != None:
          if x == Z3(1,0):
            equations[pivot][i]["+"].append(labels[j])
          elif x == Z3(0,1):
            equations[pivot][i]["-"].append(labels[j])
    return equations
