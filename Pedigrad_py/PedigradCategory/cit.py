#------------------------------------------------------------------------------
#column_is_trivial(column,exceptions): Boolean
#------------------------------------------------------------------------------
'''
This function takes two lists of elements and 
- returns True if, apart from the elements in the second input list, the first input list contains copies of a unique element 
- returns False if, apart from the elements in the second input list, the first input list contains at least two different elements.

In the former case, the list is said to be trivial.
'''
def column_is_trivial(column,exceptions):
  #If the input list is not empty, the first element of the first input list 
  #that is not an element of the second input list must be different from
  #another element in the list. The variable initiate will tell us if we
  #have already found the first element of the input list that is not an 
  #element of the second input list.
  initiate = False
  #The variable flag is the answer to the question whether the first input list is
  #trivial. The first input list is assumed to be trivial before checking (to
  #handle the empty case).
  flag = True
  #The following loop the looks for the first element of the first input list 
  #that is not an element of the second input list. Then, when the variable
  #initiate is set to True, it checks whether this first element is different from
  #any other element in the list.
  for i in range(len(column)):
    if initiate == False: 
      if not(column[i] in exceptions):
        first = column[i]
        initiate = True
        continue
    else:
      #Checks whether this first element is different from
      #any other element in the list.
      if not(column[i] in exceptions) and first != column[i]:
        flag = False
        break
  return flag
