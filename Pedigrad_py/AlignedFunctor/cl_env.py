#------------------------------------------------------------------------------
#Environment (Class) | 4 objects | 3 methods
#------------------------------------------------------------------------------
'''
[Objects] 
  .Seg  [Type] CategoryOfSegments('a)
  .pset [Type] PointedSet('b)
  .spec [Type] int
  .b    [Type] list('a)

[Methods] 
  .__init__
        [Inputs: 4]
          - Seg       [Type] CategoryOfSegments('a)
          - pset      [Type] PointedSet('b)
          - exponent  [Type] int
          - threshold [Type] list('a)
        [Outputs: 0]
  .segment
        [Inputs: 2]
          - a_list  [Type] list('b)
          - color   [Type] 'a
        [Outputs: 1]
          - return [Type] SegmentObject('a)
  .seqali
        [Inputs: 1]
          - name_of_file [Type] string
        [Outputs: 1]
          - return [Type] SequenceAlignment
                     
[General description] 
  This structure models the features of an aligned environment functors, as defined in CTGI. As in aligned environment functors, this structure is associated with a PointedSet item [pset]. The class is also equipped with a fiber operation (pullback along a point in the image of the functor) and a sequence alignment functor constructor call. Specifically, the method [segment] returns a segment that is the pullback of the aligned environment functor above any input list that represents an element in one of its images. If the input list contains a character that is not in the object [pset.symbols], then the node associated with that character is masked in the returned segment. Aditionally, the method [seqali] construct a sequence aligment functor  from a file a sequence alignments, as shown in the development of CGTI.
    
>>> Method: .__init__
  [Actions] 
    .Seg    <- use(Seg)
    .pset   <- use(pset)
    .spec   <- use(exponent)
    .b       <- use(threshold,Seg,spec)
  [Description] 
    This is the constructor of the class.
    
>>> Method: .segment
  [Actions] 
    .return   <- use(a_list,color,self.Seg,self.pset)
  [Description] 
    This method returns a segment that is the pullback of the underlying environment functor above the input list. If the list contains a character that is not in the list self.pset.symbols, then the node associated with that character is masked in the returned segment. 
    
>>> Method: .seqali
  [Actions] 
    .return  <- use(name_of_file,usf.fasta,self.Seg,self.b)
  [Description] 
    This method constructs a sequence aligment functor from a file of sequence alignments, as shown in the development of Example 3.22 of CTGI.

'''
#------------------------------------------------------------------------------
#Dependencies: current, SegmentCategory, Useful
#------------------------------------------------------------------------------
from cl_sal import SequenceAlignment

import sys
sys.path.insert(0, '../SegmentCategory/')
from cl_so import SegmentObject

import sys
sys.path.insert(0, '../Useful/')
from usf import usf
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class Environment(object): 
#------------------------------------------------------------------------------
  def __init__(self,Seg,pset,exponent,threshold):
    self.Seg = Seg
    self.pset = pset
    self.spec = exponent
    self.b = threshold
    for i in range(len(self.b)):
      if not(self.Seg.preorder.presence(self.b[i])):
        self.b[i] = self.Seg.preorder.mask
    for i in range(len(self.b),self.spec):
      self.b.append(self.Seg.preorder.mask)
#------------------------------------------------------------------------------   
  def segment(self,a_list,color):
    removal = list()
    for i in range(len(a_list)):
      if not(a_list[i] in self.pset.symbols):
        removal.append(i)
    segment = self.Seg.initial(len(a_list),color)
    return segment.remove(removal,'nodes-given')
#------------------------------------------------------------------------------  
  def seqali(self,name_of_file):
    group_labels = list()
    indiv = list()
    names,sequences = usf.fasta(name_of_file)
    for i in range(len(names)):
      usf.add_to(names[i][0],group_labels)
      usf.add_to(names[i][1],indiv)
    if len(indiv) > len(self.b):
      print("Error in Environment.seqali: "+name_of_file+" contains more individuals than the number specified in the environment.")
      exit()
    elif len(indiv) < len(self.b):
      print("Error in Environment.seqali: "+name_of_file+" contains fewer individuals than the number specified in the environment.")
      exit()
    else:  
      group_colors = list()
      alignments = list()
      check_lengths = list()
      for i in range(len(group_labels)):
        group_colors.append([self.Seg.preorder.mask]*len(indiv))
        alignments.append(['masked']*len(indiv))
        check_lengths.append([])
      for i in range(len(names)):
        gl = group_labels.index(names[i][0])
        ind = indiv.index(names[i][1])
        if self.Seg.preorder.geq(names[i][2],self.b[ind]) or self.b[ind] == True:
          group_colors[gl][ind] = names[i][2]
          alignments[gl][ind] = sequences[i]
          usf.add_to(len(alignments[gl][ind]),check_lengths[gl])
      record = list()
      indexing = list()
      for i in range(len(group_labels)):
        if len(check_lengths[i]) == 1:
          schema = [check_lengths[i][0],group_colors[i]]
          indexing.append([schema,True])
          usf.add_to(schema,record)
        else:
          indexing.append([[],False])
      base = list()
      for i in range(len(record)):
        base.append(self.Seg.initial(*record[i]))
      database = list()
      for i in range(len(record)):
        database.append([])
      for i in range(len(group_labels)):
        if indexing[i][1] == True:
          index = record.index(indexing[i][0])
          database[index].append(alignments[i])     
      return SequenceAlignment(self,indiv,base,database)
#------------------------------------------------------------------------------
