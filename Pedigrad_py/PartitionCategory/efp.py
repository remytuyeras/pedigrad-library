#------------------------------------------------------------------------------
#_epi_factorize_partition(partition): list
#------------------------------------------------------------------------------
'''
This function relabels the elements of a list with non-negative integers. It starts with the integer 0 and allocates a new label by increasing the previously allocated label by 1. The first element of the list always receives the label 0 and the highest integer used in the relabeling equals the length of the 'image' of the list decreased by 1 (see iop.py).

e.g. _epi_factorize_partition(['A',4,'C','C','a','A']) = [0, 1, 2, 2, 3, 0]

'''
from iop import _image_of_partition

def _epi_factorize_partition(partition):
  #The relabeling depends on the cardinal of the image of the partition.
  #Computing the cardinal of the image is roughly the same as computing
  #the image itself.
  the_image = _image_of_partition(partition)
  #A space is allocated to contain the relabeled list.
  epimorphism=list()
  #If the i-th element of the list is the j-th element of the image
  #then this element is relabelled by the integer j.
  for i in range(len(partition)):
    for j in range(len(the_image)):
      if partition[i] == the_image[j]:
        epimorphism.append(j)
        break
  #Returns the relabeled list.
  return epimorphism
