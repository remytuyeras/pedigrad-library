from __future__ import annotations
from typing import Any, Callable
from collections.abc import Iterator


class Tree(object):

  __slots__ = ("content","children","depth","level","weight")

  def __init__(self,
               #List of inputs and their types
               content: Any,
               *children: Tree
               #The output type
               ) -> None:
    #Any type of information           
    self.content = content
    #Pointers to the lower node of the tree
    self.children = None if children == () else list(children)
    #Distance from root
    self.level: int = 0
    #Distance from most distant leaf
    self.depth: int = 0
    #Total number of descendent leaves
    self.weight: int = 0
    #Gives accurate values to self.depth, self.level and self.weight
    self.normalize()

  def normalize(self,
                #List of inputs and their types
                level=0
                #The output type
                ) -> None:
    '''
    Gives accurate values to self.depth, self.level and self.weight.
    '''
    if self.children == None:
      #If the node if a leaf
      self.level = level
      self.depth = 0
      self.weight = 1
    else:
      #If the node has descendents
      self.level = level
      self.depth = 0
      self.weight = 0
      for child in self.children:
        #Recursive step
        child.normalize(self.level+1)
        #Depth is the maximal distance from descendent leaves
        self.depth = max(self.depth,child.depth)
        #Weight counts the number of accessible leaves from the progeny
        self.weight += child.weight
      self.depth = self.depth +1

  def __str__(self) -> str:
    '''
    Displays the architecture of the underlying Tree instance in a string (can be used to display 
    in a terminal or a text file). Descendants are displayed right below their parents in a 
    recursive fashion. The reading of a progeny can be likened to the reading of a program 
    hierarchy in python: the tree hierarchy is indentation-coded such that each level of the 
    tree is encoded by three successive dots "...". The level, depth and weight of each node 
    is displayed after the indentation inside brackets, as shown in the following example.
    [0|1|2] -> parent
    ...[1|0|1] -> child1
    ...[1|0|1] -> child2
    '''
    s = "..."*self.level
    s += f"[{self.level}|{self.depth}|{self.weight}] -> {self.content}"
    if self.children != None:
      s += "\n"
      for i, child in enumerate(self.children):
        s += str(child) + "\n" * (i<len(self.children)-1)
    return s
  
  def __levelup(self) -> None:
    '''
    Any other function __levelup could potentially be used to change self.content
    '''
    self.level = self.level + 1
    if self.children != None:
      for child in self.children:
        child.__levelup()

  def paths(self,
            #List of inputs and their types
            collect: Callable[[Any],Any]
            #The output type
            ) -> Iterator[list[Any]]:
    '''
    A generator enumerating all paths from the root to the leaves.
    '''
    l = []
    if self.children == None:
      yield [collect(self.content)]
    else:
      for child in self.children:
        for p in child.paths(collect):
          yield [collect(self.content)] + p

  @classmethod
  def generate(cls,
               #List of inputs and their types
               weights: list[int],
               filler: Callable[[],Any]
               #The output type
               ) -> Tree:
    '''
    Generates a tree whose number of branches per node at a level i is the i-th 
    element of the input list named "weights". The function filler gives a value 
    to the content of every node in the Tree instance.
    '''
    if weights ==[]:
      return cls(filler())
    else:
      return cls(filler(),*[cls.generate(weights[1:],filler) for i in range(weights[0])])