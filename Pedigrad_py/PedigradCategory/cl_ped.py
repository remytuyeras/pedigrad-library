#------------------------------------------------------------------------------
#Pedigrad: .local, .loci, .taxa, .partition
#------------------------------------------------------------------------------
'''
This class possesses three objects, namely
- .local (list)
- .loci (list)
- .taxa (list)
and two methyods, namely
-  .__init__ (constructor)
-  .partition

The consructor .__init__ takes the name of a file and an integer (as in the case of the function _read_alignment_file) and stores 
- the first output of _read_alignment_file in the object .taxa;
- the transpose of the second output of _read_alignment_file (when seen as a matrix), up to removal of those rows that contain the same character, in .local;
- the indices of the lists contained in .local as indexed the in the second output of _read_alignment_file in the object .loci (see below).

If the empty string is given to the contructor .__init__, then an empty pedigrad is returned.


The method .partition takes a list of indices (or positions) within the range of the list stored in the object .local and returns the product of the partitions that are indexed by these positions in the object .local (i.e. its list).

If the indices in the input of .partition() are greater than or equal to the length of the list stored in .local, then the method outputs a error message and exits the program.

'''
from raf import _read_alignment_file
from ict import _is_column_trivial

import sys

sys.path.insert(0, '../PartitionCategory/')

from cl_pop import ProductOfPartitions
from efp import _epi_factorize_partition

class Pedigrad: 
  #The objects of the class are:
  #.local (list);
  #.loci (list);
  #.taxa (list).
  def __init__(self,name_of_file,reading_mode):
    #If the empty string is given instead of the name of a file,
    #then the pedigrad is set to be empty.
    if name_of_file == "":
      self.local = list()
      self.loci = list()
      self.taxa = list()
    #Otherwise, the procedure _read_alignment_file reads the file
    #and takes care of the possible exceptions.
    else:
      output = _read_alignment_file(name_of_file,reading_mode)
      self.taxa = output[0]
      alignment = output[1]
      if len(self.taxa) != 0:
        #The variable flag indicates whether the alignment 
        #is not well-defined as a matrix, that is to say 
        #each line of the alignment does not contain the same number
        #of columns (or characters).
        flag = False
        for i in range(len(self.taxa)-1):
          if len(alignment[0]) != len(alignment[i+1]):
            #the vriable flag is set to True if the rows of the matrix 
            #do not have the same lengths
            flag =True
            break
        if flag ==True:
          print("Error: in Pedigrad.__init__: alignment is not aligned")
          exit()
        #If the variable alignment defines a matrix, then the following lines
        #store its transpose matrix in self.local.
        else:
          self.local = list()
          self.loci = list()
          #Spaces are allocated in the memory to store the columns of
          #the variable alignment. These columns will become the rows of  
          #the matrix stored in self.local
          for i in range(len(alignment[0])):
            a_column = list()
            for j in range(len(self.taxa)):
              #The transpose operation is done here
              a_column.append(alignment[j][i])
            #All columns whose underlying partitions are terminal are 
            #ignored because they do not provide any information on the
            #aligment.
            if _is_column_trivial(a_column,[]) == 0:
              self.local.append(a_column)
              self.loci.append(i)
      else:
        print("Error: in Pedigrad.__init__: alignment is empty")
        exit()

  def partition(self,segment):
    #No position given means no image provided via the pedigrad
    if segment == []:
      print("Error: in Pedigrad.partition: segment is empty")
      exit()
    #The position defining the segment need to accessible position in
    #the list stored in self.local
    elif (0 <= max(segment) < len(self.local)):
        #This line ensure that a new space is allocated in the case
        #segment only contains one position
        the_image = _epi_factorize_partition(self.local[segment[0]]) 
        #The image of the pedigrad are compute via the product cones of 
        #the ambiant (plain) chromology
        for i in range(len(segment)-1):
          the_image = ProductOfPartitions(
the_image,self.local[segment[i+1]]).span.peak
        return the_image
    else:
      print("Error: in Pedigrad.partition: index is not valid")
      exit()
    
