class Z3matrix(object):

  def __init__(self,matrix):
    self.matrix = matrix

  def __str__(self):
    s = "Z3matrix("
    for i in range(len(self.matrix)):
      if i >0:
        s = s + "\t  "
      s = s + "[" + ",\t".join(map(str,self.matrix[i])) + "]"
      if i <len(self.matrix)-1:
        s = s + ",\n"
    s = s + ")"
    return s

  def dim(self):
    n = len(self.matrix)
    m = len(self.matrix[0]) if n > 0 else 0
    return (n,m)

  def col(self,j):
    n, _ = self.dim()
    return [self.matrix[i][j] for i in range(n)]

  def row(self,i):
    _, m = self.dim()
    return [self.matrix[i][j] for j in range(m)]

  def transpose(self):
    matrix = list()
    n,m = self.dim()
    for j in range(m):
      row = list()
      for i in range(n):
        row.append(self.matrix[i][j])
      matrix.append(row)
    return IC_matrix(matrix)

  def __mul__(self,matrix):
    matrix_prod = list()
    n,m = self.dim()
    m,p = matrix.dim()
    for i in range(n):
      matrix_row = list()
      for j in range(p):
        r = self.row(i)
        c = matrix.col(j)
        a = Z3(0,0)
        for k in range(m):
          a = a + r[k] * c[k]
        matrix_row.append(a)
      matrix_prod.append(matrix_row)
    return IC_matrix(matrix_prod)

  def REF(self):
    return Z3matrix(sorted(self.matrix)[::-1])