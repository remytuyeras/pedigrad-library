from iop import _image_of_partition
#_image_of_partition(partition): list

from efp import _epi_factorize_partition
#_epi_factorize_partition(partition): list

from pop import _preimage_of_partition
#_preimage_of_partition(partition): list of lists

from jpop import _join_preimages_of_partitions
#_join_preimages_of_partitions(preimage1,preimage2): list of lists

from pp import print_partition
#print_partition(partition): standard output

from qop import _quotient_of_preimage
#_quotient_of_preimage(preimage): list

from cop import coproduct_of_partitions
#coproduct_of_partitions(partition1,partition2): list

from ptop import _product_of_partitions
#_product_of_partitions(partition1,partition2): list of 2-tuples

from itam import is_there_a_morphism
#is_there_a_morphism(source,target): Boolean

from cl_mop import MorphismOfPartitions
#MorphismOfPartitions: .arrow, .source, .target

from cl_sop import SpanOfPartitions
#SpanOfPartitions: .peak, .left, .right

from cl_pop import ProductOfPartitions
#ProductOfPartitions: .span
