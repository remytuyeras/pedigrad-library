#------------------------------------------------------------------------------
#Sequence (Class) | 3 objects | 1 methods
#------------------------------------------------------------------------------
'''
[Objects] 
  .name   [Type] string
  .seq    [Type] list(string)
  .color  [Type] string

[Methods] 
  .__init__
        [Inputs: 3]
          - name  [Type] string
          - seq   [Type] list(string)
          - color [Type] string
        [Outputs: 0]
           
[General description] 
  This structure models the features of a sequence that would belong to a multiple sequence alignment specified in a FASTA file. Its objects [name] and  [color] contain information that would be specified in the label given before the sequence (see FASTA format). The sequence itself is stored in the object [seq].
    
>>> Method: .__init__
  [Actions] 
    .name  <- use(name)
    .seq  <- use(sequence)
    .color  <- use(color)
  [Description] 
    This is the constructor of the method.

'''
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class Sequence(object): 
#------------------------------------------------------------------------------
  def __init__(self,name,sequence,color):
    self.name = name
    self.seq = sequence
    self.color = color
#------------------------------------------------------------------------------
