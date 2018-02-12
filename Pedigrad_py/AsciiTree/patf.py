#------------------------------------------------------------------------------
#print_atf(atf,depth): standard output
#------------------------------------------------------------------------------
'''
This function  takes an atf and its depth and prints the ascii tree associated with the atf on the standard output.

e.g. 

l = [[0,1,0,0,0,0], [0,2,0,0,0,1], [0,4,2,3,3,5]]

tree = tree_of_partitions(l)
atpf = convert_tree_to_atpf(tree)
atf  = convert_atpf_to_atf(atpf[0],atpf[1])

The output of print_atf(atf,atpf[1]) is given below.

|                   |   
|________________   |   
|               |   |   
|________       |   |   
|   |   |       |   |   
A   C   D...E   F   B
'''

import sys

def print_atf(atf,depth):
  #if depth = 0 then the program terminates and the tree is printed 
  #on the standard output
  if depth != 0 :
    for j in range(len(atf)):
      sys.stdout.write("|   ")
      for i in range(atf[j][0][0]-1):
        sys.stdout.write("    ")
    sys.stdout.write("\n")
    sys.stdout.flush()
    for j in range(len(atf)):
      #print branches for intermediate levels
      if depth != 1:
        sys.stdout.write("|")
      #print the label of the leaves
      else:
        for k in range(len(atf[j][1])):
          if k > 0:
            sys.stdout.write("...")
          sys.stdout.write(chr(65+atf[j][1][k]))
      for i in range(atf[j][0][1]):
        sys.stdout.write("____")
      #print spaces between the branches of intermediate levels
      if depth != 1:
        for i in range(atf[j][0][0]-atf[j][0][1]-1):
          sys.stdout.write("    ")
      sys.stdout.write("   ")
    sys.stdout.write("\n")
    sys.stdout.flush()
    next_atf = list()
    for i in range(len(atf)):
      #Truncates the atf from below so that 
      #the next level of the atf is turned into a forest.
      next_atf = next_atf + atf[i][1]
    #recursion: continue to the next line on the standard output
    print_atf(next_atf, depth-1)



