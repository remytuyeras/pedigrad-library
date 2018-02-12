#------------------------------------------------------------------------------
#_epi_normalizes_column(column,exceptions): list
#------------------------------------------------------------------------------
'''
This function refines the procedure _epi_factorizes_partition by relabeling the elements of a list with canonical labels except for those elements that can be found in a second input list. In other words, it takes two input lists and returns one. 

The first input lists is supposed to encode the column of an alignment file (which is usually stored in the object .local of a pedigrad) while the second input list is the list of elements that should never be relabeled by the procedure (i.e. left as is). Therefore the procedure returns the relabeling of the first input list, where the special elements contained present in the second input are left as is.

e.g. 
_epi_normalizes_column(['A','4','C','C','a','A'],['4']) = [0, '4', 2, 2, 3, 0]

'''
import sys

sys.path.insert(0, '../PartitionCategory/')

from iop import _image_of_partition

def _epi_normalizes_column(column,exceptions):
  #the relabeling depends on the cardinal of the image of the column.
  #Computing the cardinal of the image is roughly the same as computing
  #the image itself.
  the_image = _image_of_partition(column)
  #a space is allocated to contain the relabeled list
  epimorphism=list()
  #if the i-th element of the list is the j-th element of the image
  #then this element is relabelled by the integer j
  for i in range(len(column)):
    #the characters that are present in the list exception are not relabeled
    if column[i] in exceptions:
        epimorphism.append(column[i])
        continue
    else:
      #otherwise, any other character is relabeled by its position in the image
      #of the column 
      for j in range(len(the_image)):
        if (column[i] == the_image[j]):
          epimorphism.append(j)
          break   
  #returns the relabeled list
  return epimorphism
