#------------------------------------------------------------------------------
#tree_of_partitions(partitions): list of MorphismOfPartitions
#------------------------------------------------------------------------------
'''
This function takes a list of partitions that can successively be related by morphisms of partitions and returns the actual lists of morphisms of partitions between these.

The input list should always start with the target of the first arrow, then present its source, which should also be the target of the next arrow, etc.

e.g.
if we set
a = [0,0,0,0,0,0]
b = [0,0,0,0,0,1]
c = [0,0,2,2,2,1]
l = [a,b,c]
f = MorphismsOfPartitions(b,a)
g = MorphismsOfPartitions(c,b)

then the following identity should formally hold: 

tree_of_partitions(l) = [f, g]

or more graphically: l = [a <-- b:f, b <-- c:g]

'''
import sys

sys.path.insert(0, '../PartitionCategory/')

from cl_mop import MorphismOfPartitions

def tree_of_partitions(partitions):
  #The tree cannot exist if there is no morphism arising from the input list,
  #which means that the list should contain, at least, a source and a target.
  if len(partitions) < 2:
    print("Error: in tree_of_partitions: list is empty")
    exit()
  else:
    #A space is allocated in the memory to store the data of the tree.
    the_tree = list()
    for i in range(len(partitions)-1):
      #The first element of the list is always the target of the tree structure
      #while its source is the last element of the tree. This gives the direction
      #in which the morphism needs to be oriented.
      the_tree.append(MorphismOfPartitions(partitions[i+1],partitions[i]))
    return the_tree
  


