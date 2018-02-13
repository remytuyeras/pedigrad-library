#------------------------------------------------------------------------------
#print_evolutionary_tree(partitions): standard output
#------------------------------------------------------------------------------
'''
This function takes a list of partitions between which a sequence of composable morphisms exists and returns the tree encoded by this sequence of morphisms.

'''

from top import tree_of_partitions
from ctta import convert_tree_to_atpf
from cata import convert_atpf_to_atf
from patf import print_atf


def print_evolutionary_tree(partitions):
  #Returns a sequence of morphisms of partitions.
  tree = tree_of_partitions(partitions)
  #Returns an ascii tree pre-format and its depth.
  atpf = convert_tree_to_atpf(tree)
  #Returns the ascii tree format of the atpf.
  atf = convert_atpf_to_atf(atpf[0],atpf[1])
  #Prints the atf on the standard output.
  print_atf(atf,atpf[1])



