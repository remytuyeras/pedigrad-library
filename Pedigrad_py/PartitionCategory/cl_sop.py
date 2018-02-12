#------------------------------------------------------------------------------
#SpanOfPartitions: .peak, .left, .right
#------------------------------------------------------------------------------
'''
This class possesses three objects, namely
- .peak (list)
- .left (MorphismOfPartitions)
- .right (MorphismOfPartitions)
and a constructor .__init__. The consructor .__init__ takes two MorphismOfPartitions that should have the same .source object and stores 
- the common source in the object .peak;
- the first input MorphismOfPartitions in the object .left;
- the second input MorphismOfPartitions in the object .right;

If the pair of MorphismOfPartitions do not fit the desired format, the constructor outputs and error message and exits the program.

'''

class SpanOfPartitions:
  #the objects of the class are:
  #.peak (list)
  #.left (MorphismOfPartitions)
  #.right (MorphismOfPartitions)
  def __init__(self,left_morphism,right_morphism):
    #checks whether the two input morphisms have the same source object
    if left_morphism.source == right_morphism.source:
      #if it is so, the pair of morphisms is a valid span structure
      self.peak = left_morphism.source
      self.left = left_morphism
      self.right = right_morphism
    else:
      print("Error: in SpanOfPartitions.__init__: source objects do no match.")
      exit()
