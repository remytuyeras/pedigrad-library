#------------------------------------------------------------------------------
#_quotient_of_preimage(preimage): list
#------------------------------------------------------------------------------
'''
This function takes a list of lists of indices (ment to be the preimage of a partition) and returns a partition (i.e the list) whose preimage is that given in the input.

e.g.
l = [1,2,4,5,1,2,3,2,2,1,3]
p = _preimage_of_partition(l)
_quotient_of_preimage(p) = [0, 1, 2, 3, 0, 1, 4, 1, 1, 0, 4]

Note that the procedure _quotient_of_preimage(_preimage_of_partition(l)) is equal to the procedure _epi_factorizes_partition(l)

'''

def _quotient_of_preimage(preimage):
  #allocates a space in the memory to store the partition associated
  #with the input preimage
  the_quotient = list()
  #allocates spaces in the memory in order to allow the access 
  #to the positions of the elements of the partition without 
  #using the method .append (at the end of the procedure)
  for i in range(len(preimage)):
    for j in range(len(preimage[i])):
      the_quotient.append("?")
  #now the partition has the right number of allocated spaces in the memory
  #we can fill it by using the positions instead of appending elements
  for i in range(len(preimage)):
    for j in range(len(preimage[i])):
      #the partition contains the integer i at the position preimage[i][j]
      the_quotient[preimage[i][j]]=i
  return the_quotient


