from cl_la import *
#LocalAnalysis(CategoryOfSegments): .equiv, .base 
#EXPR_MODE = 'exp', SEGM_MODE = 'seg', NUCL_MODE = 'anu', 
#ATRN_MODE = 'atr', TRN0_MODE = 'tr0', TRN1_MODE = 'tr1', 
#TRN2_MODE = 'tr2', AMN0_MODE = 'aa0', AMN1_MODE = 'aa1', 
#AMN2_MODE = 'aa2', AAMN_MODE = 'aaa'

from ite import *
#ID_to_EQ(name_ID): list of lists
#NUCL_EQ, TRAN_EQ, AMIN_EQ, (CODR_EQ, NCDR_EQ)
#NUCL_ID, TRAN_ID, AMIN_ID, CODR_ID, NCDR_ID

from cit import column_is_trivial
#column_is_trivial(column,exceptions): Boolean

from raf import READ_DNA
#READ_DNA = 1

from raf import read_alignment_file
#read_alignment_file(name_of_file,reading_mode): 2-tuple

from cl_ped import NEW
#NEW = 1

from cl_ped import Pedigrad
#Pedigrad(LocalAnalysis): .local, .taxa, .partition, .reduce, .agree
