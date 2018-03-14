#------------------------------------------------------------------------------
#product_of_partitions(partition1,partition2): list
#------------------------------------------------------------------------------
'''
This function takes two lists of same length and returns a list that is the relabeling of the zipping of the two lists (i.e. the list of pairs of elements with corresponding indices in each of the input lists) via the procedure _epi_factorize_partition.

e.g.
product_of_partitions([1,1,1,1,2,3],['a','b','c','c','c','c']) = 
[0, 1, 2, 2, 3, 4]

The function outputs an error if the two input lists do not have the same length.
'''
from efp import _epi_factorize_partition

def product_of_partitions(partition1,partition2):
  #The following line checks if the product of the two lists is possible.
  if len(partition1) ==  len(partition2):
    #Constructs the list of pairs of element with the 
    #same index in the two lists, and then relabels 
    #the pairs using _epi_factorize_partition.
    return _epi_factorize_partition(zip(partition1,partition2))
  else:
    print("Error: in product_of_partitions: lengths do not match.")
    exit()
