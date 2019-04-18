#------------------------------------------------------------------------------
#Tree (Class) | 4 objects | 4 methods
#------------------------------------------------------------------------------
'''
[Objects] 
  .depth  [Type] int
  .level  [Type] int
  .parent [Type] 'a
  .children [Type] list(Tree('a))

[Methods] 
  .__init__
        [Inputs: +1]
          - parent  [Type] 'a
          - args    [Type] list(Tree('a))
        [Outputs: 0]
  .stdout
        [Inputs: 0]
        [Outputs: 0]
  .levelup
        [Inputs: 0]
        [Outputs: 0]
  .paths
        [Inputs: 0]
        [Outputs: 1]
          - l [Type] list('a)
                     
[General description] 
  This structure models the features of a tree structure. A Tree item is equipped with an object [parent] in which it is possible to store information and an object [children] through which one can specify descendants. A Tree item can be constructed recursively from the constructor. Tree items whose object [parent] is equal to the string "leaf"  are distinguished from the rest of the structure and considered as terminal states. For instance, these terminal states are useful if one wants to enumerate all the paths in the tree. For instance, the class [Tree] is equipped with a method [paths] that returns a list of all the paths going from the root to a leaf. 
    
>>> Method: .__init__
  [Actions] 
    .depth  <- use(args[0])
    .level  <- use()
    .parent <- use(parent)
    .children <- use(args[0])
  [Description] 
    This is the constructor of the class.

>>> Method: .stdout
  [Description] 
    This method displays the tree structure on the standard output.

>>> Method: .levelup
  [Actions] 
    .level  <- use()
    .children <- use()
  [Description] 
    This method increments all the objects [level] by 1 in the recursive structure of the [Tree] item.


>>> Method: .paths
  [Description] 
    This method returns a list of all the paths going from the root to a leaf.
    
'''
#------------------------------------------------------------------------------
#Dependencies: sys
#------------------------------------------------------------------------------
import sys
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class Tree(object):
#------------------------------------------------------------------------------
  def __init__(self,parent,*args):
    self.depth = 0
    self.level = 0
    self.parent = parent
    if self.parent != "leaf":
      self.children = args[0]
      for i in range(len(self.children)):
        self.children[i].levelup()
      for i in range(len(self.children)):
        self.depth = max(self.depth,self.children[i].depth)
      self.depth = self.depth +1
#------------------------------------------------------------------------------
  def stdout(self):
    if self.parent != 'leaf':
      n = self.level
      sys.stdout.write("."*n)
      sys.stdout.write("["+str(self.level)+"] -> "+str(self.parent)+"\n")
      for i in range(len(self.children)):
        self.children[i].stdout()
#------------------------------------------------------------------------------  
  def levelup(self):
    self.level = self.level + 1
    if self.parent != 'leaf':
      for i in range(len(self.children)):
        self.children[i].levelup()
#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------          
