#------------------------------------------------------------------------------
#Tree:
#------------------------------------------------------------------------------
'''




'''


import sys
from cl_tre import Tree


import sys
sys.path.insert(0, '../Useful/')
from usf import usf


class Table(object):
  #----------------------------------------------------------
  def __init__(self,seq1,seq2):
    self.seq1 = seq1
    self.seq2 = seq2
    self.content = list()
    for i in range(len(self.seq1.seq)+2):
      row = list()
      for j in range(len(self.seq2.seq)+2):
        row.append('.')
      self.content.append(row)
    self.content[0][0] = '.'
    self.content[1][1] = 0
    for i in range(len(self.seq1.seq)):
      self.content[i+2][0] = self.seq1.seq[i]
      self.content[i+2][1] = 0
    for i in range(len(self.seq2.seq)):
      self.content[0][i+2] = self.seq2.seq[i]
      self.content[1][i+2] = 0
   #----------------------------------------------------------
  def incidence(self):
    for i in range(len(self.seq1.seq)):
      for j in range(len(self.seq2.seq)):
        if self.seq1.seq[i] != self.seq2.seq[j]:
          self.content[i+2][j+2] = 0
        else:
          self.content[i+2][j+2] = 1
  #----------------------------------------------------------
  def fillout(self):
    for i in range(len(self.seq1.seq)):
      for j in range(len(self.seq2.seq)):
        if self.seq1.seq[i] == self.seq2.seq[j]:
          self.content[i+2][j+2] = max(self.content[i+2][j+2] + self.content[i+1][j+1],self.content[i+2][j+1],self.content[i+1][j+2])
        else:
          self.content[i+2][j+2] = max(self.content[i+2][j+2],self.content[i+2][j+1],self.content[i+1][j+2])
  #----------------------------------------------------------
  def choices(self,i,j):
    choices = list()
    if 0 <= i <len(self.seq1.seq) and 0 <= j < len(self.seq2.seq):
      m = max(self.content[i+2][j+2],self.content[i+2][j+1],self.content[i+1][j+2])
      #diagonal
      if self.seq1.seq[i] == self.seq2.seq[j] and self.content[i+2][j+2] == m:
        choices.append([i-1,j-1,'d'])
      #vertical and horizontal   
      if self.content[i+2][j+1] == m:
        choices.append([i,j-1,'h'])
      if self.content[i+1][j+2] == m:
        choices.append([i-1,j,'v'])
    if i == -1 and 0 <= j < len(self.seq2.seq):
      choices.append([i,j-1,'h'])
    if 0 <= i <len(self.seq1.seq) and j == -1:
      choices.append([i-1,j,'v'])
    return choices
  #----------------------------------------------------------        
  def tree(self,i,j,move):
    choices = self.choices(i,j)
    if choices == []:
      return Tree("leaf",[])
    else:
      children = list()
      for x,y,m in choices:
        children.append(self.tree(x,y,m))
        s1 = self.seq1.seq[i]
        s2 = self.seq2.seq[j]
        if i == -1:
          s1 = '-'
        if j == -1:
          s2 = '-'
      return  Tree([s1,s2,move],children)
  #----------------------------------------------------------
  def traceback(self,debug):
    tree = self.tree(len(self.seq1.seq)-1,len(self.seq2.seq)-1,'end')   
    if debug == True:
      print("\ntree")
      tree.stdout()
    return tree.paths()
  #----------------------------------------------------------    
  def read_path(self,path,move):
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
  #----------------------------------------------------------  
  def dynamic_programming(self,name_of_file,option="a",debug=False,display=True):
    paths = self.traceback(debug)
    outputs = list()
    if debug == True:
        print("\npaths")
    for i in range(len(paths)):
      outputs.append(self.read_path(paths[i],'start'))
      if debug == True:
        print(paths[i])
    with open(name_of_file,option) as the_file:
      for i in range(len(outputs)):
        n1 = ">"+str(i)+":"+str(self.seq1.name)+":"+str(self.seq1.color)+"\n"
        s1 = usf.list_to_string(outputs[i][0])+"\n"
        n2 = ">"+str(i)+":"+str(self.seq2.name)+":"+str(self.seq2.color)+"\n"
        s2 = usf.list_to_string(outputs[i][1])+"\n"
        the_file.write(n1)
        the_file.write(s1)
        the_file.write(n2)
        the_file.write(s2)  
        if display == True:  
          sys.stdout.write(n1)
          sys.stdout.write(s1)
          sys.stdout.write(n2)
          sys.stdout.write(s2)
    return outputs
  #---------------------------------------------------------- 
  def stdout(self):
    for a in range(len(self.content)):
      for b in range(len(self.content[a])):
        sys.stdout.write(str(self.content[a][b])+" | ")  
      sys.stdout.write('\n')
      sys.stdout.flush()
