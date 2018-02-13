#------------------------------------------------------------------------------
#process_local_analysis(local_analysis,exceptions,positions): list of 2-tuples
#------------------------------------------------------------------------------
'''
This function takes three inputs: 
- a list of lists meant to be the list stored in the object .local of a Pedigrad; 
- a list meant to be a list of special characters to be ignored during the procedure;
- a list of positions within the range of the first input list,
and returns a lists of 2-tuples of lists. 

Each 2-tuple of lists, say (l,m), contained in the output of process_local_analysis gives the list m of positions, that belong to the third input lists, at which the partition l can be found in the first input list, up to canonical relabeling.

e.g.

l = [[0,1,0], [1,0,1], [3,3,4]]
process_local_analysis(l,[],[0,1,2])) = [([0, 1, 0], [0, 1]), ([0, 0, 1], [2])]

If the first input list is empty, then the procedure returns the empty list.

'''
from enc import _epi_normalize_column
from ict import _is_column_trivial 


def process_local_analysis(local_analysis,exceptions,positions):
  if len(positions) == 0:
    return []
  else:
    #The following lines detect all the partitions of the same type
    #as that of the first partition encountered in local_analysis[positions[0]].
    column = _epi_normalize_column(local_analysis[positions[0]],exceptions)
    #A space is allocated in the memory to store the positions of the
    #detected partitions in local_analysis.
    record = list()
    #Obviously, the index given by positions[0] must be considered.
    record.append(positions[0])
    #The position recorded are deleted in the input list 'positions'
    #The indices are only relabelled in order to keep track of the indexing
    #of the elements in the list 'positions'.
    positions[0] = -1
    for i  in range(len(positions)-1):
      #Detection of a partition of the desired type.
      if column == _epi_normalize_column(local_analysis[positions[i+1]],exceptions):
        #Records the positions of the partitions that were identified
        #as having the same type as that of local_analysis[positions[0]].
        record.append(positions[i+1])
        positions[i+1] = -1
    #We proceed by recursion where the new positions are the positions of the 
    #partitions that have not been detected yet.
    new_positions = list()
    for i in range(len(positions)):
      #The positions already detected are not included in new_positions
      if positions[i] != -1:
        new_positions.append(positions[i])
    #In case there are trivial columns, these are not included in the output.
    #If the present procedure is applied on the object .local of a pedigrad, this
    #scenario should never occur.
    if _is_column_trivial(column,exceptions) == 0:
      return [(column,record)]+ process_local_analysis(local_analysis,exceptions,new_positions)
    else:
      return process_local_analysis(local_analysis,exceptions,new_positions)
