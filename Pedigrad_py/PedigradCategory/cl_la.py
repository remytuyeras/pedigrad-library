#------------------------------------------------------------------------------
#LocalAnalysis(CategoryOfSegments): .equiv, .base 
#------------------------------------------------------------------------------
'''
This class is a subclass of CategoryOfSegments that possesses three objects, namely
- .equiv (list of strings)
- .base (list of SegmentObject items)
and one method, namely
-  .__init__ (constructor)

The constructor .__init__ takes four (or five) arguments and uses them to initialize the objects of the class. The form of the second and third argument may vary depending on the form of the first one. On the other hand, the last two arguments always keep the same form, namely a string and an integer, which are given to the constructor of CategoryOfSegments to initialize the (super) objects .domain, .mask, .preorder (see SegmentCategory/cl_cos.py)


The first argument of .__init__ is meant be part of a set of global variables containing strings, as given below.

EXPR_MODE = 'exp'
SEGM_MODE = 'seg'
NUCL_MODE = 'nu'
TRAN_MODE = 'tr'
TRN0_MODE = 'tr0nu'
TRN1_MODE = 'tr1nu'
TRN2_MODE = 'tr2nu' 
AMN0_MODE = 'aa0'
AMN1_MODE = 'aa1'
AMN2_MODE = 'aa2'
AMIN_MODE = 'aa'

Depending on the string contained in the first argument, the constructor .__init__ may take four or five arguments. In addition, the second and third arguments may also take different forms.


The procedures .__init__(NUCL_MODE,-) and .__init__(TRAN_MODE,-) take three arguments whose last two arguments should be as described above, namely a string and an integer meant to be fed to the method .__init__ of CategoryOfSegments. For its part, the first argument should be a string that is the name of an element in the pre-order structure stored in the object .preorder.

From the point of view of the function ID_to_EQ (see ite.py), these procedures generate what could be seen as local analyses. The type of local analysis returned by .__init__(NUCL_MODE,-) is meant to read the columns of a sequence alignment without identification between the characters while the type of local analysis returned by .__init__(NUCL_MODE,-) is meant to identify 'A' with 'G' and 'C' with 'T'.


The procedures .__init__(TRN0_MODE,-), .__init__(TRN1_MODE,-) and .__init__(TRN2_MODE,-) take three arguments whose last two arguments are as described above, namely a string and an integer meant to be fed to the method .__init__ of CategoryOfSegments. For its part, the first argument should be a list of two strings that are the names of elements in the pre-order structure stored in the object .preorder.

From the point of view of the function ID_to_EQ (see ite.py), a procedure .__init__(TRNX_MODE,-) generates a local analysis that is meant to identify 'A' with 'G' and 'C' with 'T' on every column whose position is X modulo 3 and that is meant to read the other columns as-is.


The procedures .__init__(AMN0_MODE,-), .__init__(AMN1_MODE,-) and .__init__(AMN2_MODE,-) take three arguments whose last two arguments are as described above, namely a string and an integer meant to be fed to the method .__init__ of CategoryOfSegments. For its part, the first argument should be a string that is the name of an element in the pre-order structure stored in the object .preorder.

From the point of view of the function ID_to_EQ (see ite.py), a procedure .__init__(AMNX_MODE,-) generates a local analysis that reads the codons of the sequence alignment (i.e. via segments containing patches of lengths 3) with the assumption that the codon topology starts at position X and identify them according to the codon translation table.


The procedure .__init__(AMIN_MODE,-),  takes three arguments whose last two arguments are as described above, namely a string and an integer meant to be fed to the method .__init__ of CategoryOfSegments. For its part, the first argument should be a list of three strings that are the names of elements in the pre-order structure stored in the object .preorder.

From the point of view of the function ID_to_EQ (see ite.py), the procedure .__init__(AMIN_MODE,-) generates a local analysis that reads all the codons of the sequence (i.e. via segments containing patches of lengths 3) and identify them according to the codon translation table.


Finally the user can design their own local analysis by using the procedures .__init__(EXPR_MODE,-) and .__init__(SEGM_MODE,-), which take four more arguments as follows: 
- the first argument should be a list of SegmentObjects that is to be stored in the object .base;
- the second argument should a list of strings that is to be stored in the object .equiv. The strings should be one of the strings stored in the global variables NUCL_ID, TRAN_ID, AMIN_ID, N01_ID, N02_ID, ..., and N21_ID;
- the last two arguments are as described above, namely a string and an integer meant to be fed to the method .__init__ of CategoryOfSegments.

'''

import sys
sys.path.insert(0,'../SegmentCategory/')
from cl_cos import *

#The following global variables should be used 
#with the method .__init__ of LocalAnalysis .

EXPR_MODE = 'exp'
SEGM_MODE = 'seg'
NUCL_MODE = 'nu'
TRAN_MODE = 'tr'
TRN0_MODE = 'tr0nu'
TRN1_MODE = 'tr1nu'
TRN2_MODE = 'tr2nu' 
AMN0_MODE = 'aa0'
AMN1_MODE = 'aa1'
AMN2_MODE = 'aa2'
AMIN_MODE = 'aa'


class LocalAnalysis(CategoryOfSegments): 
  #The objects of the class are:
  #.equiv (list of lists of lists);
  #.base (list of SegmentObjects);
  def __init__(self,analysis_mode,*args):
    if analysis_mode == EXPR_MODE:
      #For the first user mode, args needs to contain 4 arguments, namely
      # - a list of regular expressions for SegmentObject.segment;
      # - a list of strings;
      # - the name of a file;
      # - an integer;
      if len(args) != 4:
        print("Error: in LocalAnalysis.__init__: 4 arguments needed ("+str(len(args))+" given)") 
        exit()
      else:
      #The last two arguments are used to initialize the super class
        #CategoryOfSegments
        super(LocalAnalysis, self).__init__(*args[2:4])
        #The list of regular expression for SegmentObject.segment is turned 
        #into a list of segments and is stored in .base.
        self.base = list()
        for i in range(len(args[0])):
          self.base.append(self.segment(args[0][i]))
        #The list of strings is given to .equiv.
        self.equiv = args[1]
    
    elif analysis_mode == SEGM_MODE:
      #For the second user mode, args needs to contain 4 arguments, namely
      # - a list of segments;
      # - a list of strings;
      # - the name of a file;
      # - an integer;
      if len(args) != 4:
        print("Error: in LocalAnalysis.__init__: 4 arguments needed ("+str(len(args))+" given)") 
        exit()
      else:
      #The last two arguments are used to initialize the super class
        #CategoryOfSegments
        super(LocalAnalysis, self).__init__(*args[2:4])
        #The list of segments is given to .base.
        self.base = args[0]
        #The list of strings is given to .equiv.
        self.equiv = args[1]
    
    elif analysis_mode in [NUCL_MODE,TRAN_MODE]:
      #For these modes, args needs to contain 3 arguments, namely
      # - a string (the name of an element in the pre-ordered set);
      # - the name of a file;
      # - an integer;
      self.base = list()
      self.equiv = list()
      #The last two arguments are used to initialize the super class
      #CategoryOfSegments.
      super(LocalAnalysis, self).__init__(*args[1:3])
      #The segments that are to be stored in .base will be specified as if
      #the value of object .mask was True. The following lines check that
      #this is the case.
      if self.mask == False:
        print("Error: in LocalAnalysis.__init__: "+ str(args[2])+" should contain a formal initial object (use ! before obj:)")
        exit()
      else:
        for i in range(self.domain):
          #The name of the element in the pre-ordered set is used to 
          #color the patches of the segments.
          self.base.append(self.segment([(i,1,1,args[0])]))
          #The string contained in analysis_mode[0:2] is equal to 'nu'.
          self.equiv.append(analysis_mode[0:2])

    elif analysis_mode in [TRN0_MODE,TRN1_MODE,TRN2_MODE]:
      #For these modes, args needs to contain 3 arguments, namely
      # - a lists of 2 strings (names of elements in the pre-ordered set);
      # - the name of a file;
      # - an integer;
      #The following line checks whether the first argument is a list
      #containing exactly two elements.
      if len(args[0]) != 2:
        print("Error: in LocalAnalysis.__init__: a list of 2 colors is required ("+str(len(args[0]))+" given)") 
        exit()
      else:
        self.base = list()
        self.equiv = list()
        #The last two arguments are used to initialize the super class
        #CategoryOfSegments.
        super(LocalAnalysis, self).__init__(*args[1:3])
        #The segments that are to be stored in .base will be specified as 
        #if the value of object .mask was True. The following lines check 
        #that this is the case.
        if self.mask == False:
          print("Error: in LocalAnalysis.__init__: "+ str(args[2])+" should contain a formal initial object (use ! before obj:)")
          exit()
        else:
          remainder = int(analysis_mode[2])
          for i in range(self.domain):
            if i % 3 == remainder:
            #The first name of args[0] is used to color the patches of 
            #the segments are supposed to identify A with G and  C with T.
              self.base.append(self.segment([(i,1,1,args[0][0])]))
              #The string contained in analysis_mode[0:2] is equal to 'tr'.
              self.equiv.append(analysis_mode[0:2])
            else:
            #The second name of args[0] is used to color the patches of 
            #the segments are supposed to the columns as are.
              self.base.append(self.segment([(i,1,1,args[0][1])]))
              #The string contained in analysis_mode[3:5] is equal to 'nu'.
              self.equiv.append(analysis_mode[3:5])

    elif analysis_mode in [AMN0_MODE,AMN1_MODE,AMN2_MODE]:
      #For these modes, args needs to contain 3 arguments, namely
      # - a string (the name of an element in the pre-ordered set);
      # - the name of a file;
      # - an integer;
      self.base = list()
      self.equiv = list()
      #The last two arguments are used to initialize the super class
      #CategoryOfSegments.
      super(LocalAnalysis, self).__init__(*args[1:3])
      #The segments that are to be stored in .base will be specified as if
      #the value of object .mask was True. The following lines check that
      #this is the case.
      if self.mask == False:
        print("Error: in LocalAnalysis.__init__: "+ str(args[2])+" should contain a formal initial object (use ! before obj:)")
        exit()
      else:
        remainder = int(analysis_mode[2])
        for i in range((self.domain-remainder)/3):
          #The codon topology starts at the index 'pos' (see below) and
          #then considers patches of 3 nucleotides until the nucleotide
          #at the index (self.domain-remainder)/3 is read.
          pos = 3*i+remainder
          #The string in args[0] is used to color the patches of 
          #the segments are supposed to the columns as are.
          self.base.append(self.segment([(pos,3,1,args[0])]))
          #The string contained in analysis_mode[0:2] is equal to 'aa'.
          self.equiv.append(analysis_mode[0:2])

    elif analysis_mode in [AMIN_MODE]:
      #For this mode, args needs to contain 3 arguments, namely
      # - a lists of 3 strings (names of elements in the pre-ordered set);
      # - the name of a file;
      # - an integer;
      #The following line checks whether the first argument is a list
      #containing exactly three elements.
      if len(args[0]) != 3:
        print("Error: in LocalAnalysis.__init__: a list of 3 colors is required ("+str(len(args[0]))+" given)") 
        exit()
      else:
        self.base = list()
        self.equiv = list()
        #The last two arguments are used to initialize the super class
        #CategoryOfSegments.
        super(LocalAnalysis, self).__init__(*args[1:3])
        #The segments that are to be stored in .base will be specified as 
        #if the value of object .mask was True. The following lines check 
        #that this is the case.
        if self.mask == False:
          print("Error: in LocalAnalysis.__init__: "+ str(args[2])+" should contain a formal initial object (use ! before obj:)")
          exit()
        else:
          remainder = 0
          for i in range((self.domain-remainder)/3): 
            #The codon topology starts at the index 'pos' (see below) and
            #then considers patches of 3 nucleotides until the nucleotide
            #at the index (self.domain-remainder)/3 is read.
            pos = 3*i+remainder
            #The first string of args[0] is used to color this first 
            #collection of segments.
            self.base.append(self.segment([(pos,3,1,args[0][0])]))
            #The string contained in analysis_mode[0:2] is equal to 'aa'.
            self.equiv.append(analysis_mode[0:2])
          remainder = 1
          for i in range((self.domain-remainder)/3): 
            #The codon topology starts at the index 'pos' (see below) and
            #then considers patches of 3 nucleotides until the nucleotide
            #at the index (self.domain-remainder)/3 is read.
            pos = 3*i+remainder
            #The second string of args[0] is used to color this second 
            #collection of segments.
            self.base.append(self.segment([(pos,3,1,args[0][1])]))
            #The string contained in analysis_mode[0:2] is equal to 'aa'.
            self.equiv.append(analysis_mode[0:2])
          remainder = 2
          for i in range((self.domain-remainder)/3): 
            #The codon topology starts at the index 'pos' (see below) and
            #then considers patches of 3 nucleotides until the nucleotide
            #at the index (self.domain-remainder)/3 is read.
            pos = 3*i+remainder
            #The third string of args[0] is used to color this third 
            #collection of segments.
            self.base.append(self.segment([(pos,3,1,args[0][2])]))
            #The string contained in analysis_mode[0:2] is equal to 'aa'.
            self.equiv.append(analysis_mode[0:2])    
    
