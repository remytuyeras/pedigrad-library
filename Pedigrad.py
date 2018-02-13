#----------------------------------------------------------------------------
import sys
sys.path.insert(0, 'Pedigrad_py/PartitionCategory/')
from PartitionCategory import *
#print_partition(partition): standard output
#coproduct_of_partitions(partition1,partition2): list
#MorphismOfPartitions: .arrow, .source, .target
#is_there_a_morphism(source,target): Boolean
#SpanOfPartitions: .peak, .left, .right
#ProductOfPartitions: .span
#----------------------------------------------------------------------------
import sys
sys.path.insert(0, 'Pedigrad_py/PedigradCategory/')
from PedigradCategory import *
#READ_DNA = 1
#process_local_analysis(local_analysis,exceptions,positions): list of 2-tuples
#Pedigrad: .local, .loci, .taxa, .partition
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

