#------------------------------------------------------------------------------
#ID_to_EQ(name_ID): list of lists
#------------------------------------------------------------------------------
'''
This function takes a string and returns a list of lists describing identifications to be made during the parsing of an alignment.

The function ID_to_EQ is meant to be used with two sets of global variables. One sets consists of strings that define the valid inputs of ID_to_EQ while the other set consists of the possible outputs of ID_to_EQ, which are lists of lists that are 
- either already equipped with specific equivalence classes describing a well-known evolution model 
- or that are empty so that they can be 'edited'.

Below, we give three examples of global variables that are associated with already determined equivalence classes.

ID_to_EQ(NUCL_ID) = [[]] (This equivalence relation is the trivial one, that is to say that only reflexive comparisons are considered)

ID_to_EQ(TRAN_ID) = [['A','G'],['C','T']] (This equivalence relation describes transition mutations that can occur at the level of nucleotides)

ID_to_EQ(AMIN_ID) would return the equivalence classes induced by the codon table.

The user can also makes its own equivalence relation (up to 21) via the (empty) global variables N01_EQ, N02_EQ,..., N21_EQ, which are associated with the global strings N01_ID, N02_ID,..., N21_ID.

N01_EQ.append(["A","G"])
ID_to_EQ(N01_ID) = [["A","G"]]

N02_EQ.extend([["AC","TC"],["CC", "TC"]])
ID_to_EQ(N02_ID) = [["AC","TC"],["CC", "TC"]]

'''

#THE QUOTIENT IS GIVEN BY THE INDICES OF THE LISTS!!

#There is no identification to be made when only reading nucleotides.
NUCL_EQ = [[]]

#The equivalence class of transition mutations between nucleotides.
TRAN_EQ = [
['A','G'],
['C','T']
]
#The equivalence class of silent mutations between codons.
AMIN_EQ = [
["TTT","TTC"],
["TTA","TTG","CTT","CTC","CTA","CTG"],
["TCT","TCC","TCA","TCG","AGT","AGC"],
["CCT","CCC","CCA","CCG"],
["TAT","TAC"],
#["TAA"], (stop)
#["TAG"], (stop)
["CAT","CAC"],
["CAA","CAG"],
["TGT","TGC"],
#["TGA"], (stop)
#["TGG"],
["CGT","CGC","CGA","CGG"],
["ATT","ATC","ATA"],
#["ATG"],
["GTT","GTC","GTA","GTG"],
["ACT","ACC","ACA","ACG"],
["GCT","GCC","GCA","GCG"],
["AAT","AAC"],
["AAA","AAG"],
["GAT","GAC"],
["GAA","GAG"],
["AGA","AGG"],
["GGT","GGC","GGA","GGG"]
]

#These are global variables: use .append() to update them.
N01_EQ = []
N02_EQ = []
N03_EQ = []
N04_EQ = []
N05_EQ = []
N06_EQ = []
N07_EQ = []
N08_EQ = []
N09_EQ = []
N10_EQ = []
N11_EQ = []
N12_EQ = []
N13_EQ = []
N14_EQ = []
N15_EQ = []
N16_EQ = []
N17_EQ = []
N18_EQ = []
N19_EQ = []
N20_EQ = []
N21_EQ = []

NUCL_ID = 'nu'
TRAN_ID = 'tr'
AMIN_ID = 'aa'

#Equivalence classes that can be given by the user.
#E.g. 
#- Equivalence class of mutations occurring in non-coding regions
#- Equivalence class of mutations occurring in coding regions
N01_ID = 'n1'
N02_ID = 'n2'
N03_ID = 'n3'
N04_ID = 'n4'
N05_ID = 'n5'
N06_ID = 'n6'
N07_ID = 'n7'
N08_ID = 'n8'
N09_ID = 'n9'
N10_ID = 'n10'
N11_ID = 'n11'
N12_ID = 'n12'
N13_ID = 'n13'
N14_ID = 'n14'
N15_ID = 'n15'
N16_ID = 'n16'
N17_ID = 'n17'
N18_ID = 'n18'
N19_ID = 'n19'
N20_ID = 'n20'
N21_ID = 'n21'


def ID_to_EQ(name_ID):
  if name_ID == NUCL_ID:
    return NUCL_EQ
  elif name_ID == TRAN_ID:
    return TRAN_EQ
  elif name_ID == AMIN_ID:
    return AMIN_EQ
  elif name_ID == N01_ID:
    return N01_EQ
  elif name_ID == N02_ID:
    return N02_EQ
  elif name_ID == N03_ID:
    return N03_EQ
  elif name_ID == N04_ID:
    return N04_EQ
  elif name_ID == N05_ID:
    return N05_EQ
  elif name_ID == N06_ID:
    return N06_EQ
  elif name_ID == N07_ID:
    return N07_EQ
  elif name_ID == N08_ID:
    return N08_EQ
  elif name_ID == N09_ID:
    return N09_EQ
  elif name_ID == N10_ID:
    return N10_EQ
  elif name_ID == N11_ID:
    return N11_EQ
  elif name_ID == N12_ID:
    return N12_EQ
  elif name_ID == N13_ID:
    return N13_EQ
  elif name_ID == N14_ID:
    return N14_EQ
  elif name_ID == N15_ID:
    return N15_EQ
  elif name_ID == N16_ID:
    return N16_EQ
  elif name_ID == N17_ID:
    return N17_EQ
  elif name_ID == N18_ID:
    return N18_EQ
  elif name_ID == N19_ID:
    return N19_EQ
  elif name_ID == N20_ID:
    return N20_EQ
  elif name_ID == N21_ID:
    return N21_EQ
  else:
    print("Error: in ID_to_EQ: name_ID is not recognized")
    exit()
