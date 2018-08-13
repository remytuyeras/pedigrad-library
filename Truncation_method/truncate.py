from Pedigrad import *
import sys

#This file contains the truncation method used in the research paper:
#"Category theory for genetics III: Natural selection, evolution and phylogeny"
#See Example 2.28 (ibid).

#Parses the row of a table giving mutation rates between codons.
def read_row(text):
  row = list()
  position = 0
  while position < len(text):
    save = position
    while position < len(text) and not(text[position] in ['\t', ' ']):
      position = position + 1
    row.append(text[save:position])
    position = position + 1
  return row

#Parses the whole table of mutation rates between codons. The name of the
#file containing the mutation rate table is passed to the function and
#the function returns the list of the codons associated with each column in
#the order they appear in the file and a list of lists encoding the table. 
def read_table(name_of_file):
  the_file = open(name_of_file,"r")
  text = str(the_file.read())
  the_file.close()
  labels = list()
  position = 0
  while position < len(text) and not(text[position] in ['\t',' ']) :
    position = position + 1
  position = position + 1
  save = position
  while position < len(text) and not(text[position] in ['\n','\r']):
    position = position + 1
  labels = read_row(text[save:position])
  position = position + 1
  table = list()
  while position < len(text):
    while position < len(text) and not(text[position] in ['\t',' ']):
      position = position + 1
    position = position + 1
    save = position
    while position < len(text) and not(text[position] in ['\n','\r']):
      position = position + 1
    row = read_row(text[save:position])
    if position < len(text):
      #This may happen in triangular tables:
      if len(row) < len(labels):
        for i in range(len(row),len(labels)):
          row.append('')
      table.append(row)
    position = position + 1
  return (labels,table)

#If a table is triangular, then 'symmetric' turns it into a square matrix.
def symmetric((labels,table)):
  for i in range(len(table)):
    for j in range(len(table[i])):
      if i ==i:
        table[i][i] = -1
      if i > j:
        table[j][i] = table[i][j]
  return (labels,table)

#The following function is the so-called 'truncation method' mentioned in: 
#"Category theory for genetics III: Natural selection, evolution and phylogeny"
#See Example 2.28 (ibid).
#
#Every row in the input table is associated with a codon Z and every
#coefficient in each row is associated with a codon X. The present truncation 
#method classify codons with respect to these rows. 
#
#Specifically, two codons X and Y will be said to be equivalent from the point
#of view of a codon Z if their mutation rates for the mutations Z --> X and 
#Z --> Y are above the threshold passed in the second output. Then, two
#codons X and Y will be said to be equivalent if they are equivalent with 
#respect to every codon (i.e. every row). At the end, this provides an
#equivalence relation on codons, which is outputted by the function
#'truncation_method' given below.
def truncation_method((labels,table),threshold):
  print("TRUNCATION METHOD")
  print("x = greater than or equal to threshold "+str(threshold))
  print("- = less than threshold "+str(threshold))
  print("table:")
  for i in range(len(table)):
    for j in range(len(table[i])):
      t = float(table[i][j])
      #Giving two states (0 or 1) to a coeffiecient of the matrix
      #depending on wether the ratio is greater-than-or-equal or 
      #less-than the given threshold.
      if t >= threshold:
        table[i][j] = 1
        sys.stdout.write("x ")
      else:
        table[i][j] = 0
        sys.stdout.write("- ")
    sys.stdout.write("\n")
    sys.stdout.flush()
  #If the table only contains one row, then that row represents the partition
  #defining the equivalence relation. This implies that two codons X and Y
  #will have the same classification if they have the same mutation state 
  #(0 or 1) from the point of view of the codon Z with which the row is
  #associated.
  #
  #    Z --(mutation)--> X   Z --(mutation)--> Y
  #
  if len(table) == 1:
    return (labels,table)
  #If the table contains more than one row, then the 'partition product' of
  #the rows is returned. This implies that two codons X and Y will have 
  #the same classification if they have the same mutation state (0 or 1)
  #from the point of view of any other codon Z with which the rows are
  #associated.
  #
  #    Z --(mutation)--> X   Z --(mutation)--> Y
  #
  else:
    product = table[0]
    for i in range(len(table)-1):
      product = product_of_partitions(product,table[i+1])
    return (labels,product)

#Display the non-trivial euqivalence classes of the equivalence relation
#outputted by the function 'truncation_method'.
def display_classes((labels,partition)):
  the_preimage = preimage_of_partition(partition)
  equiv_classes = list()
  for i in range(len(the_preimage)-1):
    if len(the_preimage[i+1]) > 1 :
      l = list()
      for j in range(len(the_preimage[i+1])):
        l.append(labels[the_preimage[i+1][j]])
      equiv_classes.append(l)
  return equiv_classes


#Thresholds between 18 to 21 have the same set of equivalence classes. This
#suggests that these thresholds may have reached a 'stable' classification.
THRESHOLD = 18

#NONCODING

#Truncated table with respect to the threshold (here = 18)
tncod = truncation_method(symmetric(\
read_table("Mammal_noncodingRatio.tab")),THRESHOLD)

#Display the non-trivial equivalence classes.
print("Equivalence classes:")
tnc = display_classes(tncod)
print(tnc)

print("")
#CODING

#Truncated table with respect to the threshold (here = 18)
tcod = truncation_method(symmetric(\
read_table("Mammal_codingRatio.tab")),THRESHOLD)

#Display the non-trivial equivalence classes.
print("Equivalence classes:")
tc = display_classes(tcod)
print(tc)
