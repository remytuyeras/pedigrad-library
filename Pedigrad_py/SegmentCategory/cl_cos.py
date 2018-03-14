#------------------------------------------------------------------------------
#CategoryOfSegments: .domain, .mask, .preorder, .can_switch_to, 
#                    .homset_is_inhabited, .topology, .segment
#------------------------------------------------------------------------------
'''
This class possesses three objects, namely
- .domain (integer)
- .mask (Boolean)
- .preorder (list of lists)
and five methods, namely
-  .__init__ (constructor)
-  .can_switch_to
-  .homset_is_inhabited
-  .topology
-  .segment 

The three objects .domain, .mask, and .preorder give all the needed information to specify a "category of quasi-homologous segments" Seg(Omega|n). Specifically, the object 
 - .domain contains the integer n defining the domain [n] of the segments, which can also be identified as the 'legnth' of the segments;
 - .mask says if the pre-ordered set 'Omega' contains a formal initial object (i.e. a minimum element), which is usually used as an 'ignore' state or a mask;
 - .preorder contains the down-closure of all the elements of the pre-ordered set 'Omega'. This type of data corresponds to the type of data outputted by the composition of the procedure _transitive_closure (see tc.py) with the second output of the procedure _read_pre_order (see rpo.py).

The constructor .__init__ takes two inputs, namely the name of file that contains a pre-order structure and an integer, and stores 
- the integer in the object .domain;
- a Boolean value specifying whether the pre-order structure comprises a formal initial object in .mask;
- the down-closures of the elements of the pre-order in .preorder.

The method .can_switch_to takes two strings that are meant to be the names of elements in the pre-ordered set and returns a Boolean value indicating whether the first string is greater than or equal to the second one with respect to the pre-order structure.

The method .homset_is_inhabited takes two SegmentObject items and returns a Boolean value specifying if there is a morphism from the first one to the second one. Theoretically, this function parses the two segments as if the object .mask was set to the value True.

The method .topology takes a list of 3-tuples and returns a list of 2-tuples. The input list is meant to encode a regular expression that describes the topology of a segment. The 3-tuples contained by the input list specifies
 - where a patch starts;
 - how long the patch is;
 - how many such patches are repeated successively.
The output of the procedure is the implementation of the regular expression
into a topology (a list of 2-tuples). See the comments whithin the code for more details.

The method .segment is very similar to the method .topology. It takes a list of 4-tuples and returns a SegmentObject. The input list is meant to encode a regular expression that describes the segment. The 4-tuples contained by the input list specifies
 - where a patch starts;
 - how long the patch is;
 - how many such patches are repeated successively;
 - the color name (or state) associated with the group of patches.
The output of the procedure is the implementation of the regular expression into a SegmentObject.

'''

from rpo import _read_pre_order
from tc import _transitive_closure
from cl_so import SegmentObject

#The type 'object' is needed is required by LocalAnalysis for heridity
class CategoryOfSegments(object): 
  #The objects of the class are:
  #.domain (integer)
  #.mask (Boolean);
  #.preorder (list of lists);
  
  def __init__(self,name_of_file,length_of_segments):
    #The object .domain contains the theoretical lengths of segments, which
    #may not be explicit in their list representation.
    self.domain = length_of_segments
    preorder = _read_pre_order(name_of_file)
    #The object .mask indicates whether the pre-ordered set has a formal 
    #initial object, usually standing for the 'ignore'  state.
    self.mask = preorder[0]
    #The object .preorder contains the transitive down-closure of 
    #the elements of the pre-order structure specified in name_of_file.
    self.preorder = _transitive_closure(preorder[1])
  
  #The following function takes two elements that are supposed to 
  #belong to the pre-ordered set that is saved in .preorder and 
  #returns True if the first input is greater than or equal to the second input
  #with respect to the pre-order structure and False otherwise.
  def can_switch_to(self,color1,color2):
    #The variable flag indicates whether color1 is an element of the
    #pre-ordered set.
    flag = False
    for i in range(len(self.preorder)):
      #The element color1 is found in the pre-order. The loop is broken.
      if self.preorder[i][0] == color1:
        flag = True
        break
    #If color1 has not been found, the procedure output an error message and
    #exit the program.
    if flag == False:
      print("Error: in CategoryOfSegments.can_switch_to:\
 second argument is not in .preorder")
      exit()
    else:
      #Otherwise, the following line looks for color2 in the (transitive) 
      #down-closure of color1. If it is found, then True is returned.
      #Otherwise, the procedure returns False.
      return (color2 in self.preorder[i])

  #The following function takes two SegmentObject items and returns
  #a Boolean value specifying if there is a morphism between them.
  #This function assumes that the object .mask contains the value True.
  def homset_is_inhabited(self,source,target):
    #The variable flag contains the output of the procedure. Unless
    #a problem is found in the construction of the morphism from 'source'
    #to 'target' the variable flag will be returned unmodified (i.e. = True)
    flag = True
    j = 0
    #When the object .mask contains the value True, a morphism of 
    #quasi-homologous segments consists in:
    #(1) "merging brackets" together and 
    #(2) being able to pass from the colors of the merged patches to 
    #that of the patch they are mapped in the target.
    #For every patch in 'target', we try to find the group of patches 
    #in 'source' that are merged to that patch.
    for i in range(len(target.topology)):
      #If we have not manage to find a patch in 'target'
      #that starts or finishes with the same position as the patch in 'source'
      #then the merging is not possible
      if j >= len(source.topology):
        flag = False
        break
      #The following loop tries to find the first patch  of 'source'
      #that can be merged into the patch in 'target'
      while source.topology[j][0] != target.topology[i][0]:
        if j+1 < len(source.topology):
          j = j+1
        else:
          flag = False
          break
      #If we were not able to find a patch in 'target'
      #that starts with the same position as the patch in 'source'
      #then the merging is not possible
      if flag == False:
        break
      #Checks whether the color of the patch being read in 'source'
      #can be decreased to the color of the patch being read in 'target'.
      if self.can_switch_to(source.colors[j],target.colors[i]) == False:
        flag = False
        break
      #The following loop tries to find the last patch of 'source'
      #that can be merged into the patch in 'target'
      while source.topology[j][1] != target.topology[i][1]:
        if j+1 < len(source.topology):
          j = j+1
          if self.can_switch_to(source.colors[j],target.colors[i]) == False:
            flag = False
            break
        else:
          flag = False
          break
      #If we were not able to find a patch in 'target'
      #that finishes with the same position as the patch in 'source'
      #then the merging is not possible
      if flag == False:
        break
      else:
        #Increments j in order to move forward.
        j = j+1
    return flag

  #The following procedure takes a list of 3-tuples and returns a 
  #list of 2-tuples. The input list is meant to encode a regular
  #expression that describes the topology of a segment. The 3-tuples
  #contained by the input list specifies
  # - where a patch starts;
  # - how long the patch is;
  # - how many such patches are repeated successively.
  #Specifically, the input satisfies the following syntax:
  #
  #[(start_position, length_of_patch, number_of_such_patches), (etc.) ]
  #
  #Also, note that the start positions of the 3-tuples contained in the
  #regular expression need to be given in an increasing order. 
  #For instance, a topology of the form
  #
  # (0,0,0)(0,0,0)(0,0,0,0)(0,0,0)(0,0,0)(0,0,0)(0,0,0)
  #
  #would be encoded by the following lists of 3-tuples:
  #
  # [ (0,3,2), (6,4,1), (10,3,4) ]
  #
  #However, the following list is not a valid example.
  #
  # [ (10,3,4), (6,4,1), (0,3,2) ]
  #
  #The output of the procedure is the implementation of the regular expression
  #into a topology (a list of 2-tuples). The 2-tuples contained in the output
  #are the start and end positions of each patch. For instance, the output
  #that would be produced for our first example (given above) would be as
  #follows.
  #
  #[(0, 2), (3, 5), (6, 9), (10, 12), (13, 15), (16, 18), (19, 21)]
  #
  #Also, depending on whether the object .mask is True or False, the regular
  #expression either needs to cover the whole topology or only needs to give 
  #a few relevant patches whose color might not be that of the initial object
  #of the pre-order structure.
  #1) If .mask = True, then only a few patches can be specified so that the 
  #remaining patches of the topology may be assocaited with an implicit topology.
  #For instance, the expression [(5,3,1)] when .domain = 15 can specify a
  #topology as follows: (0,0,0,0,0)(0,0,0),(0,0,0,0,0,0,0)
  #2) If .mask = False, then all the patches  of the topology must be
  #specified so that the only way to specify the topology given in item 1
  #is to give the following list.
  #
  #[(0,5,1), (5,3,1), (8,7,1)]
  #
  def topology(self,expression):
    #The following lines check whether the regular expression can only give
    #a few patches or all the patches of the topology.
    if self.mask == False:
      #To cover all the patches, the first patch needs to start by 
      #the position 0.
      if expression[0][0]!=0:
        print("Error: in CategoryOfSegments.topology:\
 mask is not allowed (0)")
        exit()
      #To cover all the patches, the start position of a given patch 
      #needs to be greater than the end position of its predecessor
      #by exactly 1. Note that the end position of the i-th group of patches 
      #contained in 'expression' is given by the formula:
      #end_position = expression[i][0]+expression[i][1]*expression[i][2] - 1
      for i in range(len(expression)-1):
        if (expression[i][0]+expression[i][1]*expression[i][2] != expression[i+1][0]):
          print("Error: in CategoryOfSegments.topology:\
 expression is not well-formed (mask is False)")
          exit()
      #To cover all the patches, the end position of the last patch needs 
      #to be greater than or equal to the length of the topology.
      length = len(expression)-1
      if expression[length][0]+expression[length][1]*expression[length][2] < self.domain:
        print("Error: in CategoryOfSegments.topology:\
 mask is not allowed (1)")
        exit()
    #A space is allocated to store the output of the procedure.
    the_topology = list()
    #The following lines check that the expression is well-formed, namely:
    # - the start positions of the 3-tuples contained in the regular
    #expression need to be given in an increasing order;
    # - the start position of a given patch needs to be greater than 
    #the end position of its predecessor.
    start = expression[0][0]
    finish = expression[0][0]+expression[0][1]*expression[0][2]
    for i in range(len(expression)-1):
      start = expression[i+1][0]
      if start >= finish:
        finish = expression[i+1][0]+expression[i+1][1]*expression[i+1][2]
      else:
        print("Error: in CategoryOfSegments.topology:\
 expression is not well-formed")
        exit()
    #If the expression is well-formed, the patches are created by following
    #the syntax of the regular expression. The regular expression will
    #not generate patches if enough patches have been generated to exceed
    #a topology whose lengths is equal to self.domain.
    for i in range(len(expression)):
      for j in range(expression[i][2]):
        if expression[i][0]+(j+1)*expression[i][1]-1 < self.domain:
          the_topology.append((expression[i][0]+j*expression[i][1],expression[i][0]+(j+1)*expression[i][1]-1))
        else:
          #The following (comment) line truncates the last 
          #patch if its end position is greater than self.domain:
          if expression[i][0]+j*expression[i][1] < self.domain:
            the_topology.append((expression[i][0]+j*expression[i][1],self.domain-1))
          #After that, all the patches have been generated and w can stop the loop.
          break
    return the_topology

  #The following procedure is very similar to the procedure .topology.
  #It takes a list of 4-tuples and returns a SegmentObject. The input
  #list is meant to encode a regular expression that describes the segment.
  #The 4-tuples contained by the input list specifies
  # - where a patch starts;
  # - how long the patch is;
  # - how many such patches are repeated successively;
  # - the color name (or state) associated with the group of patches.
  #Specifically, the input satisfies the following syntax:
  #
  #[(start_position, length_of_patch, number_of_such_patches, color),
  # (etc.) ]
  #
  #Also, note that the start positions of the 4-tuples contained in the
  #regular expression need to be given in an increasing order. 
  #For instance, a segment of the form
  #
  #('0','0','0')('0','0','0')('1','1','1','1')('2','2','2')('2','2','2')
  #('2','2','2')('2','2','2')
  #
  #would be encoded by the following lists of 3-tuples:
  #
  # [ (0,3,2,'0'), (6,4,1,'1'), (10,3,4,'2') ]
  #
  #However, the following list is not a valid example.
  #
  # [ (10,3,4,'2'), (6,4,1,'1'), (0,3,2,'0') ]
  #
  #The output of the procedure is the implementation of the regular expression
  #into a SegmentObject. For instance, the segment that would be produced for
  #our first example (given above) would be given by the following pair of
  #lists.
  #
  #topology = [(0, 2), (3, 5), (6, 9), (10, 12), (13, 15), (16, 18), (19, 21)]
  #colors = ['0', '0', '1', '2', '2', '2', '2']
  #
  #Also, depending on whether the object .mask is True or False, the regular
  #expression either needs to cover the whole segment or only needs to give 
  #a few relevant patches whose color is not that of the initial object
  #potentially specified in the pre-order structure.
  #1) If .mask = True, then only a few patches can be specified so that the 
  #remaining patches of the segment may be assocaited with an implicit topology.
  #For instance, the expression [(5,3,1,'1')] when .domain = 15 can specify a
  #topology as follows: (0,0,0,0,0)('1','1','1'),(0,0,0,0,0,0,0) where 0
  #stands for the color associated with the initial object of the 
  #pre-ordered set.
  #2) If .mask = False, then all the patches of the topology must be
  #specified so that the only way to specify the segment given in item 1 
  #is to give a list as follows.
  #
  #[(0,5,1,'0'), (5,3,1,'1'), (8,7,1,'0')]
  #
  def segment(self,expression):
    #The following lines check whether the regular expression can only give
    #a few patches or all the patches of the topology.
    if self.mask == False:
      #To cover all the patches, the first patch needs to start by 
      #the position 0.
      if expression[0][0]!=0:
        print("Error: in CategoryOfSegments.segment:\
 mask is not allowed (0)")
        exit()
      #To cover all the patches, the start position of a given patch 
      #needs to be greater than the end position of its predecessor
      #by exactly 1. Note that the end position of the i-th group of patches 
      #contained in 'expression' is given by the formula:
      #end_position = expression[i][0]+expression[i][1]*expression[i][2] - 1
      for i in range(len(expression)-1):
        if (expression[i][0]+expression[i][1]*expression[i][2] != expression[i+1][0]):
          print("Error: in CategoryOfSegments.segment:\
 expression is not well-formed (mask is False)")
          exit()
      #To cover all the patches, the end position of the last patch needs 
      #to be greater than or equal to the length of the topology.     
      length = len(expression)-1
      if expression[length][0]+expression[length][1]*expression[length][2] < self.domain:
        print("Error: in CategoryOfSegments.segment:\
 mask is not allowed (1)")
        exit()
    #Two spaces are allocated to store the two objects of the output segment.
    the_topology = list()
    the_colors = list()
    #The following lines check that the expression is well-formed, namely:
    # - the start positions of the 4-tuples contained in the regular
    #expression need to be given in an increasing order;
    # - the start position of a given patch needs to be greater than 
    #the end position of its predecessor.
    # - the color associated with a patch needs to be in the pre-ordered set,
    #which means present at the beginning of one the down-closure sets
    #contained in the object .preorder.
    list_of_objects = list()
    for i in range(len(self.preorder)):
      #Records the lists of objects of the pre-ordered set
      list_of_objects.append(self.preorder[i][0])
    #Checks that the colors are present in 'list_of_objects' and checks the
    #compatibility of the end and start positions of the patches.
    start = expression[0][0]
    finish = expression[0][0]+expression[0][1]*expression[0][2]
    for i in range(len(expression)):
      if not(expression[i][3] in list_of_objects):
        print("Error: in CategoryOfSegments.segment:\
 color \'"+str(expression[i][3])+"\' not found in .preorder")
        exit()
      elif i < len(expression)-1:
        start = expression[i+1][0]
        if start >= finish:
          finish = expression[i+1][0]+expression[i+1][1]*expression[i+1][2]
        else:
          print("Error: in CategoryOfSegments.segment:\
 expression is not well-formed")
          exit()
    #If the expression is well-formed, the patches are created by following
    #the syntax of the regular expression. The regular expression will
    #not generate patches if enough patches have been generated to exceed
    #a topology whose lengths is equal to self.domain.
    for i in range(len(expression)):
      for j in range(expression[i][2]):
        if expression[i][0]+(j+1)*expression[i][1]-1 < self.domain:
          #Creates the list of colors of the segment
          the_colors.append(expression[i][3])
          #Creates the topology of the segment
          the_topology.append((expression[i][0]+j*expression[i][1],expression[i][0]+(j+1)*expression[i][1]-1))
        else:
          #The following (comment) line truncates the last 
          #patch if its end position is greater than self.domain:
          if expression[i][0]+j*expression[i][1] < self.domain:
            the_colors.append(expression[i][3])
            the_topology.append((expression[i][0]+j*expression[i][1],self.domain-1))
          #After that, all the patches have been generated and w can stop the loop.
          break
    #A new space is allocated in the memory to store the output
    the_segment = SegmentObject(the_topology,the_colors)
    return the_segment

  
  

    
