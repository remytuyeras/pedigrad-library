#------------------------------------------------------------------------------
#ProductOfPartitions: .span
#------------------------------------------------------------------------------
'''
This class possesses one object, namely .span (SpanOfPartitions) and a constructor .__init__. The consructor .__init__ takes two lists and stores the span structure of their categorical product (as partitions) in the object .span.

If the lengths of the two input lists are not equal, the constructor outputs and error message and exits the program.

'''
from efp import _epi_factorizes_partition
from ptop import _product_of_partitions
from cl_mop import MorphismOfPartitions
from cl_sop import SpanOfPartitions

class ProductOfPartitions:
  #the object of the class is:
  #.span (SpanOfPartitions)
  def __init__(self,left_object,right_object):
    #the following line is equivalent to checking that
    #whether the two partitions belong two the same category or not
    if len(left_object) ==  len(right_object):
      #if so, their product can be computed. The procedure
      #_epi_factorizes_partition is applied in order to make 
      #the representation of the product object canonical.
      the_product = _epi_factorizes_partition(
_product_of_partitions(
left_object,right_object))
      #the left and right legs of the span structure associated with the 
      #categorical product are stored in the variables left_morphism and  
      #right_morphism, respecticely.
      left_morphism   = MorphismOfPartitions(the_product,left_object)
      right_morphism  = MorphismOfPartitions(the_product,right_object)
      #The span is formed from the pair (left_morphism,right_morphism).
      #According the previous two lines, this pair does define a span since
      #the source objects of left_morphism and right_morphism must
      #be equal to the list stored in the_product.
      self.span = SpanOfPartitions(left_morphism,right_morphism)
    else:
      print("Error: in ProductOfPartitions.__init__: lengths do not match.")
      exit()
