#------------------------------------------------------------------------------
#name (Class) | 3 objects | 1 methods
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
  This structure models the features of a sequence in a set of multiple sequence alignments meant to be displayed in a fasta file. Its objects [name] and [color] are used to form the fasta reference associated with a sequence of characters contained in its object third object [seq].
    
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
