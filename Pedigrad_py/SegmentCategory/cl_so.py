#------------------------------------------------------------------------------
#SegmentObject: .colors, .topology, .patch
#------------------------------------------------------------------------------
'''
This class possesses two objects, namely
- .topology (list of 2-tuples)
- .colors (list of indices);
and two methods, namely
-  .__init__ (constructor)
-  .patch

The idea of behind the two objects .colors and .topology is that they contain all the needed information to define a mathetical segment given by a pair (t,c) where t is the 'topology', usually encoded by an order preserving surjection, and c is the coloring map, usually encoded by a functor going to a pre-ordered set. 

c = [0,1,1,0,0]
t = [(0,2), (3,5), (6,8), (9,11), (12,14)]

s = SegmentObject(t,c)

For its part, the pre-ordered set associated with a segment can be specified through the classs CategoryOfSegments (see cl_cos.py).

The constructor .__init__ takes two lists, specifically a lists of indices and a list of pairs of increasing indices, and allocate them in the object .colors and .topology, respectively

The other method .patch takes an integer and returns the index of the first pair (a,b) of .topology that bounds the integer, that is to say that the input integer is greater than or equal to the first component 'a' and  also is less than or equal to the second component 'b'. If no such index exists, then the procedure returns -1.

'''

class SegmentObject: 
  #The objects of the class are:
  #.topology (list of 2-tuples);
  #.colors (list of indices);
  def __init__(self,topology,colors):
    if len(colors) == len(topology):
    #This constructor only assignments values that already exist in the memory.
      self.colors = colors
      self.topology = topology
    else:
      print("Error: in SegmentObject.__init__: lengths do not match.")
      exit()
  #The following method takes a position within the domain of segment and 
  #returns the index of the patch in which it lives in the segment structure. 
  #This index also corresponds to the image of the position through the 
  #topology of the segment. If the position is not found, the value -1 is returned.
  def patch(self,position):
    the_index = -1
    #Looks for the position in the topology
    for i in range(len(self.topology)):
      if self.topology[i][0] <= position <= self.topology[i][1]:
        #The index of the list in which 'position' appears is saved
        the_index = i
        break
    #Either the index of the patch associated with 'position' is returned 
    #or -1 is returned if there is no such index.
    return the_index
