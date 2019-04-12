#------------------------------------------------------------------------------
#Tree
#------------------------------------------------------------------------------
'''




'''

import sys
 
class Tree(object):
  #----------------------------------------------------------
  def __init__(self,parent,children):
    self.depth = 0
    self.level = 0
    self.parent = parent
    self.children = children
    if self.children != []:
      for i in range(len(self.children)):
        self.children[i].levelup()
      for i in range(len(self.children)):
        self.depth = max(self.depth,self.children[i].depth)
      self.depth = self.depth +1
  #----------------------------------------------------------  
  def levelup(self):
    self.level = self.level + 1
    if self.children != []:
      for i in range(len(self.children)):
        self.children[i].levelup()
  #----------------------------------------------------------
  def stdout(self):
    sys.stdout.write("["+str(self.level)+"] -> "+str(self.parent)+"\n")
    if self.children != []:
      for i in range(len(self.children)):
        n = self.children[i].level
        sys.stdout.write("."*n)
        self.children[i].stdout()
  #----------------------------------------------------------
  def paths(self):
    l = list()
    if self.parent == 'leaf':
      return [[]]
    else:
      for i in range(len(self.children)):
        l = l + self.children[i].paths()
      for i in range(len(l)):
        l[i] = [self.parent] + l[i]
      return l
      
           
