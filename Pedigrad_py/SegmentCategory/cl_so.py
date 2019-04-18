#------------------------------------------------------------------------------
#SegmentObject (Sublass) | 4 objects | 6 methods
#------------------------------------------------------------------------------
'''
[Objects] 
  .domain   [Type] int
  .topology [Type] list(int * int)
  .colors   [Type] list('a)
  .parse    [Type] int

[Methods] 
  .__init__
        [Inputs: 3]
          - domain    [Type] int
          - topology  [Type] list(int * int)
          - colors    [Type] list('a)
        [Outputs: 0]
  ._start
        [Inputs: 0]
        [Outputs: 0]
  .patch
        [Inputs: 2]
          - position  [Type] int
          - search    [Type] string
        [Outputs: 1]
          - return    [Type] int
  .display
        [Inputs: 0]
        [Outputs: 0]
  .merge
        [Inputs: 2]
          - folding_format  [Type] list(int * int * int)
          - infimum         [Type] fun: 'a * 'a -> 'a
        [Outputs: 1]
          - return          [Type] SegmentObject
  .remove
        [Inputs: 2]
          - a_list  [Type] list
          - option  [Type] string
        [Outputs: 1]
          - return  [Type] SegmentObject
                          
[General description] 
  This structure models the features of segments (as defined in CGTI). A segment can be seen as a tape equipped with a read head, whose position is stored in the object [parse] and is displayed through the method [display] as a red node. The method [patch] allows one to return the index of the patch (an area in brackets) that contains a node whose position is given as an input. Note that the method [patch] starts searching the index associated with the node from where the read head is and only goes in a direction (left or right) specified through its second input; the method [merge] takes a tiling of the domain of the segment and merges groups of patches that share the same tiles. The tiling patterns are specified in a list of triples, where each triple gives a start index, a tile length, and an end index for each tiling pattern considered; the method [remove] removes either a node or a patch (from the segment) at the index given in the first argument depending on whether the second argument is equal to 'nodes-given' or is not specified.
    
>>> Method: .__init__
  [Actions]
    .level    <- use()
    .domain   <- use(domain)
    .topology <- use(topology)
    .colors   <- use(colors)
    .parse    <- use()
  [Description] 
    This method is the constructor of the class.

>>> Method: ._start
  [Actions] 
    .parse  <- use(self.parse,self.topology)
  [Description] 
    Sets the read head to index 0 if the read head is outside of the 
  segment domain.

>>> Method: .patch
  [Actions] 
    return  <- use(self.parse,self.topology,position,search)
  [Description] 
    Returns the index of a patch, or a node, or -1 if none is found.
   
>>> Method: .display
  [Actions] 
    sys.stdout  <- use(self._start,self.parse)
  [Description] 
    Displays the segment.

>>> Method: .display
  [Actions] 
    sys.stdout  <- use(self._start,self.parse)
  [Description] 
    Displays the segment on the standard output.

>>> Method: .merge
  [Actions] 
    return  <- use(self.domain,self.topology,self.colors,self.__init__)
  [Description] 
    Merges patches together according to a tiling structure on the segment.

>>> Method: .remove
  [Actions] 
    return  <- use(self.domain,self.topology,self.colors,self.__init__)
  [Description] 
    Removes patches (option = 'patches-given') or nodes (option = 'nodes-given')
  from the segment.  
'''
#------------------------------------------------------------------------------
#Dependencies: sys
#------------------------------------------------------------------------------
import sys

sys.path.insert(0, '../Useful/')
from cat import CategoryItem
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class SegmentObject(CategoryItem):
#------------------------------------------------------------------------------ 
  def __init__(self,domain,topology,colors):
    super(SegmentObject, self).__init__(0)
    if len(colors) == len(topology):
      self.domain = domain
      self.topology = topology
      self.colors = colors
      self.parse = 0
    else:
      print("Error: in SegmentObject.__init__: lengths do not match.")
      exit()
#------------------------------------------------------------------------------  
  def _start(self):
    if 0 > self.parse or self.parse >= len(self.topology):
      self.parse = 0
#------------------------------------------------------------------------------  
  def patch(self,position,search = ">1"):
    self._start()
    if 0 > position or position >= self.domain:
      return -1
    while 0<= self.parse < len(self.topology):
      if position < self.topology[self.parse][0]:
        if search[0] == '<':
          self.parse -= int(search[1:])
        else:
          return -1
      elif position > self.topology[self.parse][1]:
        if search[0] == '>':
          self.parse += int(search[1:])
        else:
          return -1
      else:
        return self.parse
        break
    return -1
#------------------------------------------------------------------------------
  def display(self):
    #In any cases
    sys.stdout.write('(')
    
    if len(self.topology)>0:
      #How to display segments with a long masked start patch 
      if self.topology[0][0] < self.domain: #Should happen
        if self.topology[0][0] > 10:
          sys.stdout.write('o-'+str(self.topology[0][0]-1)+'-o')
        else:
          for i in range(self.topology[0][0]):
            sys.stdout.write('o')
      else: #Special case where the whole segment is masked
        if self.domain > 11:
          sys.stdout.write('o-'+str(self.domain-2)+'-o')
        else: #Bottleneck case w/t the normal case
          for i in range(self.domain):
            sys.stdout.write('o')
      if 0 < self.topology[0][0] < self.domain:
        sys.stdout.write('|')
        
      #Display the inside of the segment 
      self._start()
      saved_parse = self.parse
      prec_value = -1
      self.parse = 0
      i = self.topology[0][0]
      while i <= min(self.domain-1,self.topology[len(self.topology)-1][1]):
        value = self.patch(i)
        if i == self.topology[0][0]:
          prec_value = value
        elif prec_value != value:
          prec_value = value
          sys.stdout.write('|')
        if value != -1:
          if self.parse == saved_parse:
            sys.stdout.write('\033[91m\033[1mo\033[0m')
          else:
            sys.stdout.write('\033[1mo\033[0m')
        else:
          sys.stdout.write('o')
        i += 1
        
      #How to display segments with a long masked end patch 
      if self.domain-self.topology[len(self.topology)-1][1]-1> 11:
        sys.stdout.write('|o-'+str(self.domain-self.topology[len(self.topology)-1][1]-3)+'-o')
      else:
        for i in range(self.domain-self.topology[len(self.topology)-1][1]-1):
          if i == 0:
            sys.stdout.write('|')
          sys.stdout.write('o')
          
      #In any cases       
      self.parse = saved_parse
    sys.stdout.write(')\n')
#------------------------------------------------------------------------------  
  def merge(self,folding_format,infimum):
    new_topology = list()
    new_colors = list()
    initial = 0
    final = 0
    step = 0
    while step < len(folding_format):
      start,modulo,end = folding_format[step]
      initial = max(start,initial)
      new_topology = new_topology + self.topology[final:initial]
      new_colors = new_colors + self.colors[final:initial]
      if initial >= len(self.topology):
        break
      final = min(max(initial,end+1),len(self.topology))
      saved_pos = 0
      saved_color = ''
      for i in range(initial,final):
        #Look for masked patches within the tiling
        if i+1 < len(self.topology) \
        and (self.topology[i+1][0] - self.topology[i][1] > 1):
          saved_color = True
        #If no color has been attributed yet (first color)
        if saved_color == '':
          saved_color = self.colors[i]
        #Otherwise, take the infimum with the previous color
        else:
          saved_color = infimum(self.colors[i],saved_color)
        if i % modulo == initial % modulo:
          saved_pos = self.topology[i][0]
        if i % modulo == (initial-1) % modulo or i == final-1:
          if saved_color != True:
            new_topology.append((saved_pos,self.topology[i][1]))
            new_colors.append(saved_color)
          #Repeat the same process if the tiling continues  
          saved_color = ''
      if step == len(folding_format)-1:
        new_topology = new_topology + self.topology[final:]
        new_colors = new_colors + self.colors[final:]
      initial = final
      step += 1
    return SegmentObject(self.domain,new_topology,new_colors)
#------------------------------------------------------------------------------    
  def remove(self,a_list, option = 'patches-given'):
    new_topology = list()
    new_colors = list()
    removed_patches = list()
    for i in range(len(a_list)):
      if option == 'nodes-given':
        p = self.patch(a_list[i])
      else:
        p = a_list[i]
      #Avoid the value p = -1
      if 0<= p < len(self.topology):
        removed_patches.append(p)
    for i in range(len(self.topology)):
      if not(i in removed_patches):
        new_topology.append(self.topology[i])
        new_colors.append(self.colors[i])
    return SegmentObject(self.domain,new_topology,new_colors)
#------------------------------------------------------------------------------  
