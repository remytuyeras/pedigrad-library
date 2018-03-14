from iop import _image_of_partition
#_image_of_partition(partition): list

from efp import _epi_factorize_partition
#_epi_factorize_partition(partition): list

from piop import _preimage_of_partition
#_preimage_of_partition(partition): list of lists

from jpop import _join_preimages_of_partitions
#_join_preimages_of_partitions(preimage1,preimage2): list of lists

from pp import print_partition
#print_partition(partition): standard output

from cl_er import EquivalenceRelation
#EquivalenceRelation: .classes, .range, .closure, .quotient

from cop import coproduct_of_partitions
#coproduct_of_partitions(partition1,partition2): list

from pop import product_of_partitions
#product_of_partitions(partition1,partition2): list

from hii import homset_is_inhabited
#homset_is_inhabited(source,target): Boolean

from cl_mop import MorphismOfPartitions
#MorphismOfPartitions: .arrow, .source, .target
