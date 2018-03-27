#------------------------------------------------------------------------------
#Pedigrad(LocalAnalysis): .local, .taxa, .partition, .reduce, .agree
#------------------------------------------------------------------------------
'''
This class is a subclass of LocalAnalysis that possesses two objects, namely
- .local (list of lists)
- .taxa (list)
and two methods, namely
-  .__init__ (constructor)
-  .partition
-  .reduce
-  .agree

The consructor .__init__ takes the name of a file and an integer (as in the case of the function read_alignment_file) as well as a list of arguments that could be given to the constructor of LocalAnalysis (see __init__ in cl_la.py), except for the last argument that does not need to be given if the name of the file exists or the given name is actually empty. 

E.g.

P = Pedigrad("align.fa",READ_DNA,TRN2_MODE,['2','1'],"omega.yml")

L = LocalAnalysis(TRN2_MODE,['2','1'],"omega.yml",500)

The constructor __init__ then passes its first two arguments to the procedure read_alignment_file and proceeds to the initialization of the objects .local, .taxa and .base as follows:
- it stores the first output of read_alignment_file in the object .taxa;
- it appends the remaining lists of arguments given to the __init__ with a variable containing the length of the second output of read_alignment_file and gives the resulting tuples of arguments to the constructor of LocalAnalysis. Once the object .base of the super class has been (pre-)initialized by this process, the segments that it contains are used to parse the sequence alignment. The parsed data is then stored in the object .local as follows:

- For every patch (x,y) occurring in the topology of i-th segment contained .base, the characters appearing from position x to position y, in the sequence alignment, are collected for each line of the sequence alignment (i.e. each list of characters contained in the second output of read_alignment_file) and put together to form a list of strings;

- This list of strings is then relabeled with respect the indices of the lists of equivalence classes that should have been among the arguments meant to be given to the constructor of LocalAnalysis;

- If the relabeled list of strings is not trivial according to the procedure column_is_trivial(-,[]), then it is stored at position i in the object .local;

- If the lists of strings happens to be trivial, then it is not stored and the associated segment is removed from the object .base (thus shifting the indexing).

Note that when the segments of the base only contain patches of length 1 and the equivalence classes are empty (e.g. NUCL_EQ), then the list of lists stored in .local corresponds to the transpose of the sequence alignment (when seen as a matrix), up to removal of those columns (in the alignment) that only contain the one character;

If the name of the file that is passed to the contructor in its first argument is empty, then the objects .local and .taxa are initialized with empty lists while the other objects .equv, .base, .domain, .mask and .preorder are initialized via the constructor of the class LocalAnalysis.


The method .partition takes 

- either no argument;
- or the regular expression of SegmentObject item and a string;
- or a SegmentObject item and a string.

If no argument is given, then the procedure returns a terminal partition. Otherwise, the procedure returns the image of the right Kan extension (see \cite{Phylog} for more details) of the underlying local analysis on the input segment. 

This image is a partition that is computed as the product of the partitions in .local whose indices correspond to the indices of those segments in .base to which there is a morphism of segment from the input SegmentObject item.


The method .reduce takes from 2 to 3 arguments and returns a Pedigrad item that can be seen as a restriction of the ambient pedigrad (self). Specifically, the method .reduce takes:
- an EquivalenceRelation item (see PartitionCategory/cl_er.py);
- an integer;
- and if the previous integer is 1, a list of elements.

If the integer input is not 1, then the procedure returns a pedigrad whose images (i.e. the outputs of the method .partition) are equal to the categorical products of the images of the ambient pedigrad (for the same segment) with the underlying partition of the EquivalenceRelation item passed to the function.

P.reduce(eq,0).partition(s) = P.partition(s) x u.quotient()

Broadly, this means that the partitions of the returned pedigrad gather those integers that:
- are in non-trivial classes of the input RelationEquivalence item;
- and are gathered in the corresponding partitions of the ambient pedigrad;
and isolate those integers that:
- are in trivial classes of the input RelationEquivalence item;
- or are not present in the input RelationEquivalence item;

If the integer input is 1, then the procedure returns the same images as those returned when the second input is 0, except for those images that originate from columns of the alignment containing elements in the third output at the indices specified in the EquivalenceRelation item, in which case these images are all equal to the terminal partition.


The method .agree takes a list of SegmentObjects items and a list of non-negative integers (i.e. a partition) and returns all those segments contained in the first input whose images are equal to the second input. Categorically, this corresponds to pulling back what can be seen as the restriction of the pedigrad on the first input along the obvious functor 1 --> Part(S) determined by the second input.



'''
from raf import read_alignment_file
from cit import column_is_trivial
from cl_la import LocalAnalysis
from cl_la import SEGM_MODE
from cl_la import EXPR_MODE
from ite import ID_to_EQ

import sys

sys.path.insert(0, '../PartitionCategory/')

from pop import product_of_partitions
from efp import _epi_factorize_partition
from cl_er import EquivalenceRelation

REMOVE = 1

class Pedigrad(LocalAnalysis): 
  #The objects of the class are:
  #.local (list);
  #.taxa (list).
  def __init__(self,name_of_file,reading_mode,*args):
    #If the empty string is given instead of the name of a file,
    #then the pedigrad is set to be empty.
    if name_of_file == "":
      #If the name of the file is empty, the tuple *args should as
      #given to the constructor of the super class, that is to say that
      #it should finish with an integer indicating the length of the alignment.
      super(Pedigrad, self).__init__(*args)
      self.local = list()
      self.taxa = list()
    #Otherwise, the procedure read_alignment_file reads the file
    #and takes care of the possible exceptions.
    else:
      output = read_alignment_file(name_of_file,reading_mode)
      self.taxa = output[0]
      alignment = output[1]
      if len(self.taxa) == 0:
        print("Error: in Pedigrad.__init__: alignment is empty")
        exit()
      else:
        #The variable flag indicates whether the alignment 
        #is not well-defined as a matrix, that is to say 
        #each line of the alignment does not contain the same number
        #of columns (or characters).
        flag = False
        for i in range(len(self.taxa)-1):
          if len(alignment[0]) != len(alignment[i+1]):
            #The variable flag is set to True if the rows of the matrix 
            #do not have the same lengths
            flag =True
            break
        if flag ==True:
          print("Error: in Pedigrad.__init__: alignment is not aligned")
          exit()
        else:
          #The arguments stored in *args are used with iniatialize
          #the objects of the super class LocalAnalysis. To do so, *args needs
          #to be extended by the integer len(alignment[0]), which is 
          #done via tuple concatenation:  *args+(len(alignment[0]),)
          #Note the last comma for a singleton tuple.
          super(Pedigrad, self).__init__(*args+(len(alignment[0]),))
          self.local = list()
          new_base = list()
          #For every segment in .base, one wants to reads every line of the
          #sequence alignment.
          for i in range(len(self.base)):
            #The variable an_interval is going to be used to store the various
            #portions of the sequence alignment specificed by the topologies
            #of the segments stored in the object .base of the 
            #super class LocalAnalisys.
            an_interval = list()
            #The following loop reads every line of the alignment 
            #for a fix segment.
            for j in range(len(self.taxa)):
              #The variable indiv_patch is used to store the portion of the
              #sequence alignment specified by a given patch in a segment.
              indiv_patch = ""
              #The following loop runs over all the patches contained the
              #topology of the i-th segment of the base.
              for x,y in self.base[i].topology:
                #All the characters appearing from position x to position
                #y in the j-th of the alignment are collected in indiv_patch
                for k in range(x,y+1):
                  indiv_patch = indiv_patch + alignment[j][k]
              #The following lines take care of relabeling the string 
              #indiv_patch by the index of the equivalence class with 
              #which it is associated from the point of view of the 
              #LocaAnalysis structure. For the i-th segment in the base,
              #the associated set of equivalence classes is encoded
              #by the string stored in self.equiv[k]
              quotient = ID_to_EQ(self.equiv[i])
              #To detect if we failed to give a representative to the string
              #indiv_patch, we ask whether the representative is equal to -1. 
              representative = -1
              for k in range(len(quotient)):
                if indiv_patch in quotient[k]:
                  representative = k
                  break
              if representative == -1: 
                #If no representative was found, then we use indiv_patch
                #itself.
                an_interval.append(indiv_patch)
              else:
                #Otherwise, the representative replaces the string indiv_patch
                an_interval.append(representative)
            #There is, a priori, no need to consider trivial columns so that
            #these are automatically removed (future development might make
            #it optional). Of course, the corresponding segment is also removed
            #from the base of the local analysis.
            if not(column_is_trivial(an_interval,[])):
              self.local.append(an_interval)
              new_base.append(self.base[i])
          #the base is updated
          self.base = new_base
              

  def partition(self,*args):
    #If no argument is given, then the procedure returns the terminal
    #partition.
    if len(args) == 0:
      terminal_partition = list()
      #The (unique) value of the terminal partition is chosen to be 0.
      for i in range(len(self.taxa)):
        terminal_partition.append(0)
      return terminal_partition
    #Otherwise, the procedure 'partition' should exactly take 2 arguments.
    #The first argument is either a regular expression specifying a
    #SegmentObject
    #item or a SegmentObject item. The two cases are detected via the second
    #argument, which should be equal to the global variable EXPR_MODE in the 
    #first case (see cl_la.py) and equal to the golbal variable SEGM_MODE
    #in the second case (see cl_la.py).
    elif len(args) != 2:
      print("Error: in Pedigrad.partition: takes a segment and a mode ("+str(len(args))+" arguments given)")
      exit()
    else:
      #If the second argument of args is EXPR_MODE, then the regular expression
      #given in the first argument is converted into an acutal SegmentObject
      #item.
      if args[1] == EXPR_MODE:
        the_segment = self.segment(args[0])
      #Otherwise, the SegmentObject item given in the first argument suffices.
      elif args[1] == SEGM_MODE:
        the_segment = args[0]
      #Any other value than EXPR_MODE and SEGM_MODE is considered an error,
      #which triggers the output of an error message and forces the procedure
      #to exit the program. 
      else:
        print("Error: in Pedigrad.partition: \'"+str(args[1])+"\' is not recognized.")
        exit()
      #A space in allocated in the memory to store the image of the segment;
      #i.e. the output.
      the_image = self.partition()
      #The image of the segment is then computed as the product of 
      #the obvious (partial) chromology above the base of the local analysis.
      for i in range(len(self.base)):
        if self.homset_is_inhabited(the_segment,self.base[i]):
          the_image = product_of_partitions(the_image,self.local[i])
      #The resulting product of partitions is returned
      return the_image

  #The argument 'equivalence' is an EquivalenceRelation item while *args is
  #either of the form (1,a_list) or 0.
  def reduce(self,equivalence,*args):
    #A new Pedigrad item is allocated in the memory. Since the name of the
    #file passed in its first argument is empty, the objects .local and .taxa 
    #of the variable 'new_pedigrad' are empty. Also, because the name of the
    #preorder structure is empty, the object .mask is set to False and the
    #the preorder is encoded by an empty list (this is rectified below).
    new_pedigrad = Pedigrad('',0,SEGM_MODE,self.base,self.equiv,'',self.domain)
    #The following two lines reset the preorder structure to that of the
    #ambient pedigrad. 
    new_pedigrad.mask = self.mask
    new_pedigrad.preorder = self.preorder
    #The object .taxa is set to that of the ambient pedigrad
    new_pedigrad.taxa = self.taxa
    #The variable 'partition' contains the underlying partition of the
    #equivalence relation defined by 'equivalence'.
    partition = equivalence.quotient()
    #This part deals with the case where 1 is the second input.
    if args[0] == 1:
      #In this case, any segment of the base that is mapped to a partition 
      #that originates from a list of strings that contains at least 
      #one string in 'args[1]' is removed from the base. 
      #To construct the new base, a space is allocated in the memory.
      new_base = list()
      #The variable 'the_range' is used to store the elements appearing
      #in the specification of the equivalence class 'equivalence'.
      the_range = list()
      for i in range(len(equivalence.classes)):
        the_range.extend(equivalence.classes[i])
      #The following lines fill:
      #- the list 'new_pedigrad.local' with the i-th segment of self.base;
      #- the list 'new_base'  with the partition resulting from the product
      #  of the i-th list of strings contained in self.local with the
      #  underlying partition of 'equivalence',
      #provided that the i-th list of strings in self.local do not contain
      #strings in 'args[1]' at the indices contained in the list 'the_range'.
      for i in range(len(self.local)):
        #The variable flag indicates indicates whether 'self.local[i]' contains
        #a string that is in 'args[1]' at the indices contained in 'the_range'.
        flag = False
        for j in range(len(the_range)):
          #If 'self.local[i]' contains an element of 'args[1]' at one of the
          #indices contained in 'the_range', then flag is set to False.
          if self.local[i][the_range[j]] in args[1]:
            flag = True   
            break
        if flag == False:
          #No string was matching with those contained in args[1]. Therefore
          #product_of_partitions(self.local[i],partition) is added to the 
          #object .local of the output pedigrad.
          new_pedigrad.local.append(product_of_partitions(self.local[i],partition))
          #The associated segment is also added to the future .base of the
          #output pedigrad.
          new_base.append(new_pedigrad.base[i])
        else:
          continue
      #Once the list 'new_base' is completed, it is stored in the object 
      #.base of the output pedigrad.
      new_pedigrad.base = new_base
    #This part deals with the case where the second input is not 1.
    #In this case, the object .base stays the same, but the object .local
    #of the new pedigrad contains the product of equivalence.quotient()
    #with the partitions contained the object .local of the ambient pedigrad.
    else:
      for i in range(len(self.local)):
        new_pedigrad.local.append(product_of_partitions(self.local[i],partition))
    #The new pedigrad is returned with an updated .base and an updated .local
    return new_pedigrad

  #The variable 'ground' is meant to be a list of SegmentObject items 
  #while the variable pulling_condition is meant to be a list of 
  #non-negative integers.
  def agree(self,ground,pulling_condition):
    #A space is allocated to memorize the output. The list 'agreeing_segments'
    #will record all the segments whose images via the pedigrad (self) are
    #equal to the list 'pulling_condition'.
    agreeing_segments = list()
    #Partitions are generally considered the same up to relabeling.
    #Since the images of the pedigrad are always labeled according to
    #the procedure _epi_factorize_partition, the list 'pulling_condition'
    #should also be relabeled via the procedure _epi_factorize_partition.
    pulling_condition = _epi_factorize_partition(pulling_condition)
    #The following loop collects the segments from the list 'ground'
    #whose outputs via the procedure self.partition are equal to
    #the relabeled list 'pulling_condition'.
    for i in range(len(ground)):
      if self.partition(ground[i],SEGM_MODE) == pulling_condition:
        agreeing_segments.append(ground[i])
    #The segments agreeing with the pulling condition are returned.
    return agreeing_segments
