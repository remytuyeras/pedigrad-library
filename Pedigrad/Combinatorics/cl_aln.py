from typing import Iterator
from Pedigrad.Containers.cl_tre import Tree

PathType = list[tuple[int,int,str]]

class Alignment(object):

  __slots__ = ("seq1","seq2","point","table","filled")

  def __init__(self,
               #List of inputs and their types
               seq1: str,
               seq2: str,
               point: str = "-"
               #The output type
               ) -> None:
    #The two sequences to be compared
    self.seq1: str = seq1
    self.seq2: str = seq2
    #Special character to encode a missing character
    self.point: str = point
    #Comparison table with no information
    self.table: list[list[Any]] = [["." for _ in range(len(self.seq1)+2)] \
                                        for _ in range(len(self.seq2)+2)]
    #Initialize the comparison table with zeros and sequence characters
    self.initialize()
    #Indicate whether the comparison table is filled with scores
    self.filled: bool = False

  def initialize(self) -> None:
    '''
    Initiliazes the variable self.table with zeros values and the characters of the two string
    to compare. These initializations happen on the lefmost columns and the topmost rows of the
    matrix contained in self.table.
    '''
    #Fills up the top-left corner of the numerical matrix.
    self.table[1][1] = 0
    #Fills up the two columns on the left
    for i, c in enumerate(self.seq1):
      self.table[i+2][0] = c
      self.table[i+2][1] = 0
    #Fills up the two rows on the top
    for i, c in enumerate(self.seq2):
      self.table[0][i+2] = c
      self.table[1][i+2] = 0

  def __str__(self) -> str:
    '''
    Retuns a string shoiwng the content of the matrix self.table.
    '''
    #Takes care of the indentation for long coefficients.
    num_to_str = lambda x: " "*(3-len(str(x)))+str(x)
    #Returns a table showing the content of self.table
    return "\n".join(map(lambda x:" ".join(map(num_to_str,x)),self.table))

  def fillout(self) -> None:
    '''
    Applies a dynamic programming algorithm similar to the Needleman-Wunsch algorithm to 
    compute a table of scores for comparing the two strings self.seq1 and self.seq2. 
    See the documentation for more information.
    '''
    #The method does not run if it has already been called
    if not self.filled:
      #From here on, the method is condered to be "called"
      self.filled = True
      for i, c1 in enumerate(self.seq1):
        for j, c2 in enumerate(self.seq2):
          #Applies the dynamic computing formula for the scores
          self.table[i+2][j+2] = max(self.table[i+1][j+1]+1 if c1 == c2 else 0,
                                     self.table[i+2][j+1],
                                     self.table[i+1][j+2])
  
  def quality(self) -> None:
    self.fillout()
    return self.table[-1][-1]

  #the character "-" should be a wild card
  def choices(self,
              #The output type
              i: int,
              j: int
              #The output type
              ) -> PathType:
    choices = []
    if 0 <= i <len(self.seq1) and 0 <= j < len(self.seq2):
      m = max(self.table[i+2][j+2],self.table[i+2][j+1],self.table[i+1][j+2])
      #diagonal
      if self.seq1[i] == self.seq2[j] and self.table[i+2][j+2] == m:
        choices.append([i-1,j-1,'d'])
      #vertical and horizontal   
      if self.table[i+2][j+1] == m:
        choices.append([i,j-1,'h'])
      if self.table[i+1][j+2] == m:
        choices.append([i-1,j,'v'])
    if i == -1 and 0 <= j < len(self.seq2):
      choices.append([i,j-1,'h'])
    if 0 <= i <len(self.seq1) and j == -1:
      choices.append([i-1,j,'v'])
    return choices
        
  def tree(self,
           #The output type
           i: int,
           j: int,
           move: str
           #The output type
           ) -> Tree:
    choices = self.choices(i, j)
    if not choices:
      return Tree("leaf")
    children = [self.tree(x, y, m) for x, y, m in choices]
    s1 = '-' if i == -1 else self.seq1[i]
    s2 = '-' if j == -1 else self.seq2[j]
    return Tree([s1, s2, move],*children)

  def traceback(self) -> Iterator[PathType]:
    tree = self.tree(len(self.seq1)-1,len(self.seq2)-1,'end')   
    for path in tree.paths(lambda x: x):
      yield path[:-1]
    
  def read_path(self,path,move) -> tuple[list[str],list[str]]:
    if path == []:
      return [], []
    else:
      seq1 = list()
      seq2 = list()
      head = path[len(path)-1]
      if move in ['d','start']:
        seq1.append(head[0])
        seq2.append(head[1])
      if move == 'h':
        seq1.append('-')
        seq2.append(head[1])
      if move == 'v':
        seq1.append(head[0])
        seq2.append('-')
      new_path = path[0:len(path)-1]
      s1,s2 = self.read_path(new_path,head[2])
      return seq1 + s1, seq2 + s2

  def comparisons(self) -> list[tuple[str,str]]:
    join_pairs = lambda x: ["".join(x[0]),"".join(x[1])]
    return [join_pairs(self.read_path(path,'start')) for path in self.traceback()]
