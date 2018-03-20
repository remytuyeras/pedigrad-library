#----------------------------------------------------------------------------
import sys
sys.path.insert(0, 'Pedigrad_py/PartitionCategory/')
from PartitionCategory import *

#print_partition(partition): standard output

#EquivalenceRelation: .classes, .range, .closure, .quotient

#product_of_partitions(partition1,partition2): list

#coproduct_of_partitions(partition1,partition2): list

#MorphismOfPartitions: .arrow, .source, .target

#homset_is_inhabited(source,target): Boolean

#----------------------------------------------------------------------------
import sys
sys.path.insert(0, 'Pedigrad_py/SegmentCategory/')
from SegmentCategory import *

#SegmentObject: .colors, .topology

#CategoryOfSegments: .domain, .mask, .preorder

#----------------------------------------------------------------------------
import sys
sys.path.insert(0, 'Pedigrad_py/PedigradCategory/')
from PedigradCategory import *

#READ_DNA = 1

#read_alignment_file(name_of_file,reading_mode): 2-tuple

#column_is_trivial(column,exceptions): Boolean

#Pedigrad(LocalAnalysis): .local, .taxa, .partition, .select, .agree

#REDUCE = 1

#LocalAnalysis(CategoryOfSegments): .equiv, .base 

#EXPR_MODE = 'exp', SEGM_MODE = 'seg', NUCL_MODE = 'anu', 
#ATRN_MODE = 'atr', TRN0_MODE = 'tr0', TRN1_MODE = 'tr1', 
#TRN2_MODE = 'tr2', AMN0_MODE = 'aa0', AMN1_MODE = 'aa1', 
#AMN2_MODE = 'aa2', AAMN_MODE = 'aaa'

#ID_to_EQ(name_ID): list of lists

#NUCL_EQ, TRAN_EQ, AMIN_EQ, N01_EQ, ..., N21_EQ
#NUCL_ID, TRAN_ID, AMIN_ID, N01_ID, ..., N21_ID

#----------------------------------------------------------------------------
import sys
sys.path.insert(0, 'Pedigrad_py/AsciiTree/')
from AsciiTree import *

#tree_of_partitions(partitions): list of MorphismOfPartitions

#convert_tree_to_atpf(tree): ascii tree pre-format

#convert_atpf_to_atf(aptf,depth): ascii tree format

#print_atf(atf,depth): standard output

#print_evolutionary_tree(partitions): standard output

#----------------------------------------------------------------------------
