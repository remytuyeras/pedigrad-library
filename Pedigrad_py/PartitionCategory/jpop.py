#------------------------------------------------------------------------------
#_join_preimages_of_partitions(preimage1,preimage2): list of lists
#------------------------------------------------------------------------------
'''
This function takes a pair of lists of disjoint lists of indices (the indices should not be repeated and should range from 0 to a fixed positive integer) and returns the list of the maximal unions of internal lists that intersect within the concatenation of the two input lists (see below). 

In practice, the two input lists would be obtained as outputs of the procedure _preimage_of_partition(_,_) for two lists of the same length.

e.g.
Considering the following lists of lists of indices
p1 = [[0, 3], [1, 4], [2]]
p2 = [[0, 1], [2], [3], [4]]
we can notice that
[0,3] intersects with [0,1] and [3]
[0,1] intersects with [1,4] and [1]
[1,4] intersects with [4]
and
[2] only intersects with [2]
so that we have
_join_preimages_of_partitions(p1,p2) = [[1, 4, 0, 3], [2]]

In terms of implementation, the procedure _join_preimages_of_partitions(p1,p2) considers each internal list of p1 and searches for the lists of p2 that intersect it. If an intersection is found between two internal lists, it merges the two internal lists in p1 and empties that of p2 (the list is emptied and *not* removed in order to preserve a coherent indexing of the elements of p2). The function continues until all the possible intersections have been checked.

Here is a detail of what _join_preimages_of_partitions(p1,p2) does with respect to the earlier example:

The element 0 of [0,3] is searched in the list [0,1] of p2;
The element 0 is found;
The lists [0,3] and [0,1] are merged in p1 and [0,1] is emptied from p2 as follows:
p1 = [[0, 3, 1], [1, 4], [2]]
p2 = [[], [2], [3], [4]];
The element 0 has now been found in p2 and does not need to be searched again (breaks)

The element 3 of [0, 3] is searched in the list [] of p2;
The element 3 is not found (continues)
The element 3 of [0, 3] is searched in the list [2] of p2;
The element 3 is not found (continues)
The element 3 of [0, 3] is searched in the list [3] of p2;
The element 3 is found;
The lists [0,3] and [3] are merged in p1 and [3] is emptied from p2 as follows:
p1 = [[0, 3, 1], [1, 4], [2]]
p2 = [[], [2], [], [4]];
The element 3 has now been found in p2 and does not need to be searched again (breaks)

All elements of the initial list [0, 3] have been searched.
The first lists of p1 is appended to p2 in order to ensure the transitive computation of the maximal unions through the next interations. 
The list [0, 3, 1] of p1 is emptied as follows:
p1 = [[], [1, 4], [2]]
p2 = [[], [2], [], [4], [0, 3, 1]];

Repeat the previous procedure with respect to the list [1, 4] of p1.
We obtain the following pair:
p1 = [[], [], [2]]
p2 = [[], [2], [], [], [], [1, 4, 0, 3]]

Repeat the previous procedure with respect to the remaining list [2] of p1.
We obtain the following pair:
p1 = [[], [], []]
p2 = [[], [], [], [], [], [1, 4, 0, 3], [2]]

The function stops because there is no more list to process in p1.
The output is all the non-empty lists of p2; i.e. [[1, 4, 0, 3], [2]]
'''
from iop import _image_of_partition

def _join_preimages_of_partitions(preimage1,preimage2):
  #Spaces are allocated in the memory so that the lists saved at the addresses
  #of the variables 'preimage1' and 'preimage2' are not modified.
  #For convenience, we will refer to tmp1 and tmp2 as preimage1 and preimage2.
  tmp1 = preimage1
  tmp2 = preimage2
  #Reads preimage1;
  for i1 in range(len(tmp1)):
    #Reads in the i1-th internal lists of preimage1;
    for j1 in range(len(tmp1[i1])):
      #Reads preimage2;
      for i2 in range(len(tmp2)):
        #The variable flag indicates whether the value tmp1[i1][j1]
        #has been found in one of the internal lists of preimage2;
        flag = False
        #Reads in the i2-th internal lists of preimage2.
        for j2 in range(len(tmp2[i2])):
          #The j1-th element of the i1-th internal list of preimage1
          #is found in preimage2, specifically at position j2 
          #of the i2-th internal list.
          if tmp1[i1][j1] == tmp2[i2][j2]:
            #The i2-th internal lists of preimage2 is appended
            #to the i1-th internal lists of preimage1.
            tmp1[i1].extend(tmp2[i2])
            #The i2-th internal lists of preimage2 is emptied.
            tmp2[i2]=[]
            #Repeated elements occuring in the union of the two internal 
            #lists, in preimage1, are eliminated.
            tmp1[i1] = _image_of_partition(tmp1[i1])
            #the variable flag indicates whether the j1-th element of  
            #the i1-th internal list of preimage1 was found in preimage2.
            flag = True
            break
        #tmp1[i1][j1] no longer needs to be searched in preimage2.
        if flag == True:
          break
    #On the one hand, the union of the first internal list of preimage1 
    #with all the other internal lists of preimage2 that intersect 
    #it is appended to preimage2.
    tmp2.append(tmp1[i1])
    #On the other hand, this union is emptied in preimage1.
    tmp1[i1] = []
  #A space is allocated for the output of the procedure.
  the_join = list()
  #Only includes the non-empty lists of preimage2 in the output.
  for i in range(len(tmp2)):
    if tmp2[i]!=[]:
      the_join.append(tmp2[i])
  #The output contains the non-empty lists of preimage2.
  return the_join
