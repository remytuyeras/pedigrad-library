#------------------------------------------------------------------------------
#convert_tree_to_atpf(tree): ascii tree pre-format
#------------------------------------------------------------------------------
'''
This function takes a list of morphisms of partitions and convert it into its associated ascii tree pre-format (abbrev. atpf; see below and the documentation for more details). Specifically, the procedure returns a list and an integer, where the list is the atpf of the input and the integer is equal to the depth of the atpf.

The idea behind the ascii tree pre-format is to compute a higher level bracketing on the indices of the partition (i.e. the taxa) by considering the successive preimages of each morphisms of partitions contained in the input list.

For illustration, consider the following list of partitions:
a = [0,1,0,0,0,0],
b = [0,2,0,0,0,1],
c = [0,4,2,3,3,5]

This list induces an obvious sequence of morphisms of partitions that can be constructed by the procedure tree_of_partitions (see top.py).

Since the lengths of these partitions is 6, the atpf will induce a higher level bracketing of the elemens 1,2,3,4,5 and 6. To start with, one considers the preimage of the last partition c whose preimage is given by the following list of lists:

[[0], [1], [2], [3, 4], [5]]

To start constructing the atpf, we follow the recursive definition of the grammar of atpfs (see the documentation) by taking the lists [0], [1, 2], [3, 4], and [5] to be the initial values of the recursion so that the first level of the atpf is given by the following list:

the_atpf = [(1, [0]), (1, [1]]), (1, [2]]), (2, [3, 4]), (1, [5])]
 
For the next level, we need to compute the preimage of the arrow encoding the morphism of partitions c --> b. Specifically, the arrow of the morphism c --> b is as follows when c and b are relabeled as c = [0,1,2,3,3,4] and b = [0,1,0,0,0,2].
0 --> 0
2 --> 0
3 --> 0
1 --> 1
4 --> 2 

Since b has three elements in its image, this morphism possesses three fibers, which are given by the following list of lists:

fiber = [[0, 2, 3], [1], [4]]

Following the atpf grammar, we now need to replace 

fiber[0][0] with the_atpf[0]
fiber[0][1] with the_atpf[2]
fiber[0][2] with the_atpf[3]
fiber[1][0] with the_atpf[1]
fiber[2][0] with the_atpf[4]

so that the fiber is turned into the folloiwng list.

fiber = [[(1, [0]), (1, [2]]), (2, [3, 4])], [(1, [1]])], [(1, [5])]]

To complete the construction of the next level of the atpf, there remains to compute the weight for each internal list. Precisely, we can see that

- the weight of [(1, [0]), (1, [2]]), (2, [3, 4])] is 1+1+2 = 4;
- the weight of [(1, [1]])] is 1;
- the weight of [(1, [5])]] is 1.

We then equip each list with its weight via tuples as shown below.

the_atpf = [(4,[(1, [0]), (1, [2]]), (2, [3, 4])]), (1,[(1, [1]]))], (1,[(1, [5])])]

We then repeat the previous procedure with, this time, the fiber of the morphism b -> a and the earlier list so that the final atpf is of the following form.

the_atpf = [(5, [(4, [(1, [0]), (1, [2]), (2, [3, 4])]), (1, [(1, [5])])]), (1, [(1, [(1, [1])])])]

'''
import sys

sys.path.insert(0, '../PartitionCategory/')

from pop import _preimage_of_partition

def convert_tree_to_atpf(tree):
  #The highest level in the atpf grammar (i.e. the leaves) is computed
  #by computing the preimage of the last source given in the input list
  the_atpf =_preimage_of_partition(tree[len(tree)-1].source)
  for i in range(len(the_atpf)):
    the_atpf[i]=(len(the_atpf[i]),the_atpf[i])
  #To compute of the next levels of the atpf grammar (i.e. the trees)
  #one needs to compute the fibers of the morphisms contained in 
  #the input list (i.e tree)
  for k in range(len(tree)):
    fiber = _preimage_of_partition(tree[len(tree)-1-k].arrow)
    for i in range(len(fiber)):
      for j in range(len(fiber[i])):
        #The next line replaces the fibers with the backeting induced by the atpf.
        #The bracketing of the fiber is preserved, so that the level of the 
        #bracketing contained in the atpf is increased.
        fiber[i][j] = the_atpf[fiber[i][j]]
    #Computes the weight of each tree
    for i in range(len(fiber)):
      weight = 0
      for t in fiber[i]:
        weight = weight + t[0]
      fiber[i] = (weight,fiber[i])
    #The construction of the grammar is completed in the following line.
    #The procedure repeats the previous construction until it reaches the 
    #first morphism of the input list.
    the_atpf = fiber
  #The depth of the atpf is equal to len(tree)+1
  return (the_atpf,len(tree)+1)



