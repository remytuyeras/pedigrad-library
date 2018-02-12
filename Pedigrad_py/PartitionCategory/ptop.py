#------------------------------------------------------------------------------
#_product_of_partitions(partition1,partition2): list of 2-tuples
#------------------------------------------------------------------------------
'''
This function takes two lists and returns the list of pairs of element with the same index in the two lists.

e.g.
_product_of_partitions([1,2,3],['a','b','c']) = [(1, 'a'), (2, 'b'), (3, 'c')]

The function outputs an error if the two input lists do not have the same length.
'''

def _product_of_partitions(partition1,partition2):
  #checks if the product of the two lists is possible
  if len(partition1) ==  len(partition2):
    #allocates a space in the memory to store the output
    the_product = list()
    for i in range(len(partition1)):
      #constructs the list of pairs of element with the same index 
      #in the two lists.
      the_product.append((partition1[i],partition2[i])) 
    return the_product 
  else:
    print("Error: in product_of_partitions: lengths do not match.")
    exit()
