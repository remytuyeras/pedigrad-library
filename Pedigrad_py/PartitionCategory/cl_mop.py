#------------------------------------------------------------------------------
#MorphismOfPartitions: .arrow, .source, .target
#------------------------------------------------------------------------------
'''
This class possesses three objects, namely
- .arrow (list)
- .source (list)
- .target (list)
and a constructor .__init__. The consructor .__init__ takes two lists and stores, in the object .arrow, a list that describes, if it exists, the (unique) morphism of partitions from the first list (seen as a partition) to the second list (seen as a partition). The canonical epimorphisms associated with the partitions of the first and second input lists are stored in the objects .source and .target, respectively.

If we suppose that the two input lists are labeled in the same way as the procedure _epi_factorizes_partition would (re)label them, then the list that is to be contained in the object .arrow is computed as the image of the product of the two lists, as illustrated in the following example.

Consider the following lists.
p1 = [0, 1, 2, 3, 3, 4, 5]
p2 = [0, 1, 2, 3, 3, 3, 1]

Their product is as follows:
p3 = _product_of_partitions(p1,p2) = [(0,0),(1,1),(2,2),(3,3),(3,3),(4,3),(5,1)]

The image of the product is then as follows:
p4 = _image_of_partition(p3) = [(0,0),(1,1),(2,2),(3,3),(4,3),(5,1)]

We can see that for each pair (x,y) in p4, every component x is mapped to a unique image y so that p4 defines the morphism of partitions between p1 and p2.

If there exists no morphism from the first input list to the second input list, then the function outputs an error message.

For example, if we modify p2 as follows
p2 = [0, 1, 2, 3, 6, 3, 5]

then the image of the product of p1 and p2 is as follows:
p4 = [(0,0),(1,1),(2,2),(3,3),(3,6),(4,3),(5,1)]

As can be seen, the argument 3 is 'mapped' to two different images, namely 3 and 6. In this case, the constructor .__init__ exits the program with an error message. 

'''
from efp import _epi_factorizes_partition
from iop import _image_of_partition
from ptop import _product_of_partitions

class MorphismOfPartitions:
  #the objects of the class are:
  #.arrow (list)
  #.source (list)
  #.target (list)
  def __init__(self,source,target):
    if len(source) == len(target):
      #relabeling the source and target by using _epi_factorizes_partition
      #will allow us to quickly know whether there is an arrow from the source
      #and the target (see below)
      self.source = _epi_factorizes_partition(source)
      self.target = _epi_factorizes_partition(target)
      #the following line computes the binary relation that is supposed to 
      #encode the function from the codomain of the underlying
      #epimorphism encoding the source partition to the codomain of the
      #epimorphsim encoding the target partition
      self.arrow = _image_of_partition(_product_of_partitions(self.source,self.target))
    #the following loop checks if the binary relation contained 
    #in self.arrow is a function
    for i in range(len(self.arrow)):
      #checking the following condition is equivalent to checking
      #whether the label i in self.source is mapped to a unique element in 
      #self.target, namely the value contained in self.arrow[i][1].
      #Note that: the mapping might not be unique when the indexing of 
      #the labels of the source partition is not compatible with that
      #of the target partition.
      if self.arrow[i][0]==i:
        #we are only interested in the image (not the graph) of the function
        self.arrow[i] = self.arrow[i][1] 
      else:
        print("Error: in MorphismOfPartitions.__init__: source and target are not compatible.")
        exit()
