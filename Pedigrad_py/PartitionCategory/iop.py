#------------------------------------------------------------------------------
#_image_of_partition(partition): list
#------------------------------------------------------------------------------
'''
This function takes a list of elements and returns the list of its elements that occur at least once (without repetition) in the order in which they can be accessed through the list.

e.g. _image_of_partition([3,3,2,1,1,2,4,5,6,5,2,6]) = [3,2,1,4,5,6]

'''
def _image_of_partition(partition):
  #a space is allocated in the memory to contain the image of the list
  the_image=list()
  #the variable flag indicates whether the element that is read in
  #partition, at index i, is already present in the list. If it is not
  #the element is added, otherwise the loop is broken
  flag = 0
  for i in range(len(partition)):
    for j in range(len(the_image)):
      #the i-th element of partition is detected in the image
      #this is recorded in flag and the loop is instantly broken
      if the_image[j]== partition[i]:
        flag = 1
        break
    #if the value partition[i] was already present in the image
    #the variable is set back to 0; nothing  happens
    #and the next iteration is initiated.
    if flag == 1:
      flag = 0
      continue
    #if the value partition[i] was not already in the image
    #this value is added to the image and flag is set back to 0
    else:
      the_image.append(partition[i])
      flag = 0
  #after the loop, the list of elements found in partition is returned
  return the_image
