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
from enc import _epi_normalizes_column
from ict import _is_column_trivial 


def process_local_analysis(local_analysis,exceptions,positions):
  if len(positions) == 0:
    return []
  else:
    column = _epi_normalizes_column(local_analysis[positions[0]],exceptions)
    record = list()
    record.append(positions[0])
    positions[0] = -1
    for i  in range(len(positions)-1):
      if column == _epi_normalizes_column(local_analysis[positions[i+1]],exceptions):
        record.append(positions[i+1])
        positions[i+1] = -1
    new_positions = list()
    for i in range(len(positions)):
      if positions[i] != -1:
        new_positions.append(positions[i])
    if _is_column_trivial(column,exceptions) == 0:
      return [(column,record)]+ process_local_analysis(local_analysis,exceptions,new_positions)
    else:
      return process_local_analysis(local_analysis,exceptions,new_positions)
