#------------------------------------------------------------------------------
#coproduct_of_partitions(partition1,partition2): list
#------------------------------------------------------------------------------
'''
This function takes two lists of the same legnth and returns their coproduct (or join) as partitions. Specifically, the procedure outputs the quotient of the join of their preimages. If the two input lists do not have the same length, then an error message is outputted and the program is aborted.

'''
from piop import _preimage_of_partition
from jpop import _join_preimages_of_partitions
from cl_er import EquivalenceRelation

def coproduct_of_partitions(partition1,partition2):
  #The following line checks if the coproduct is possible.
  if len(partition1) == len(partition2):
    #Returns the coproduct of two partitions as the quotient of the
    #equivalence relation induced by the join of the preimages
    #of the two partitions.
    the_join = EquivalenceRelation(_join_preimages_of_partitions(_preimage_of_partition(partition1),_preimage_of_partition(partition2)))
    return the_join.quotient()
  else:
    print("Error: in coproduct_of_partitions: lengths do not match.")
    exit()
