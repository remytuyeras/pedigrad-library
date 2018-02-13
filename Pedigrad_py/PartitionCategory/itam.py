#------------------------------------------------------------------------------
#is_there_a_morphism(source,target): Boolean
#------------------------------------------------------------------------------
'''
This function takes two lists and returns a Boolean value indicating whether there exists a morphism of partitions from the underlying partition of the first input list to the underlying partition of the second input list.

The code of this function is very similar to the code of the contructor associated with the class MorphismOfPartitions.

'''

from efp import _epi_factorize_partition
from iop import _image_of_partition
from ptop import _product_of_partitions

def is_there_a_morphism(source,target):
  if len(source) == len(target):
    #Relabeling the source and target by using _epi_factorize_partition
    #allows us to quickly know whether there is an arrow from the source
    #and the target (see below).
    epi_source = _epi_factorize_partition(source)
    epi_target = _epi_factorize_partition(target)
    #The following line computes the binary relation that is supposed to 
    #encode the function from the codomain of the underlying
    #epimorphism encoding the source partition to the codomain of the
    #epimorphsim encoding the target partition.
    relation = _image_of_partition(_product_of_partitions(epi_source,epi_target))
    flag = 1
    #The following loop checks if the binary relation meant to encode 
    #the arrow between the two partitions is a function.
    for i in range(len(relation)):
      #Checking the following condition is equivalent to checking
      #whether the label i in epi_source is mapped to a unique element in 
      #epi_target, namely the value contained in epi_arrow[i][1].
      #See cl_mop.py for more information.
      if relation[i][0]!=i:  
        flag = 0
        break
    return flag
