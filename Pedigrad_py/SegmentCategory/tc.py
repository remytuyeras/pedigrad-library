#------------------------------------------------------------------------------
#_transitive_closure(down_closure): list of lists
#------------------------------------------------------------------------------
'''
This function takes a list of lists (called down_closure) and returns another list of lists whose pointer is the same as that given in the input (i.e. the input modified by the function).

The input is supposed to be the list of the non-transitive down-closures of the elements of a pre-ordered set, as given by the second output of the procedure _read_pre_order (see rpo.py).

The output is then the list of transitive down-closures of the elements of a pre-ordered set.

Here is an example with the procedure _read_pre_order for the following pre-order specification.

-----------------------------------------------------
omega.yml:
-----------------------------------------------------
#This is a pre-ordered set.

#the list of elements of the set (without the formal minimum).
!obj: 1 2 3 4 5 6

#the list of non-trivial (generating) relations.
rel:
 - 1 > 2;
 - 2 > 3;
 - 3 > 5;
 - 5 > 6;
-----------------------------------------------------

preorder = _read_pre_order("omega.yml")

preorder[1] = [
['1', '2'],
['2', '3'],
['3', '5'],
['4'],
['5', '6'],
['6'],
]

Omega = _transitive_closure(preorder[1])

Omega = [
['1', '2', '3', '5', '6'],
['2', '3', '5', '6'],
['3', '5', '6'],
['4'],
['5', '6'],
['6'],
]

'''

def _transitive_closure(down_closure):
  #The transitive completion covers every down-closure present in 
  #the list down_closure
  for i in range(len(down_closure)):
    #The variable flag_closure indicates whether the closure reached 
    #a fix point in the transitive completion of the input down-closures
    flag_closure = True
    #The loop keep going while the transitive completion is not completed.
    while flag_closure == True:
      #The variable flag_closure is set to False so that only the absence
      #of element addition to down_closure[i] will tell us that
      #the transitive completion is finished (see below where flag_closure
      #is set to True.
      flag_closure = False
      #The transitive completion goes as follows:
      #the down closure of every element in down_closure[i] is added
      #to down_closure[i]. This is repeated until no new element is added 
      #to down_closure[i].
      for elt in down_closure[i]:
        #The folloiwng lines look for the down closure of every element (elt)
        #in down_closure[i].
        for j in range(len(down_closure)):
          if (j != i) and elt == down_closure[j][0]:
            #the down closure of elt is added to down_closure[i].
            for new_elt in down_closure[j]:
              #Only adds the elements that are not already in down_closure[i]
              if not(new_elt in down_closure[i]):
                down_closure[i].append(new_elt)
                #If an element is added, then the transitive 
                #closure has not been completed yet
                #so that the loop needs to keep going.
                flag_closure = True
  #The same point as that given by the input is returned.
  return down_closure

    
