#------------------------------------------------------------------------------
#PreOrder (Class) | 4 objects | 7 methods
#------------------------------------------------------------------------------
'''
[Objects] 
  .relations  [Type] list(list('a))
  .transitive [Type] bool
  .mask       [Type] bool
  .cartesian  [Type] int

[Methods] 
  .__init__
        [Inputs: 2+] 
          - name_of_file  [Type] char
          - cartesian     [Type] int
          - *args         [Type] list
        [Outputs: 0]
  .closure
        [Inputs: 0]
        [Outputs: 0]
  ._geq
        [Inputs: 2]
          - element1  [Type] 'a
          - element2  [Type] 'a
        [Outputs: 1]
          - return    [Type] bool
  .geq
        [Inputs: 2]
          - element1  [Type] 'a
          - element2  [Type] 'a
        [Outputs: 1]
          - return    [Type] bool
  ._inf
        [Inputs: 2]
          - element1  [Type] 'a
          - element2  [Type] 'a
        [Outputs: 1]
          - return    [Type] 'a
  .inf
        [Inputs: 2]
          - element1  [Type] 'a
          - element2  [Type] 'a
        [Outputs: 1]
          - infimum   [Type] 'a
  .presence
        [Inputs: 1]
          - element   [Type] 'a
        [Outputs: 1]
          - presence  [Type] bool
                              
[General description] 
  This class models the features of a pre-ordered set. The pre-order relations are specified through either a file [name_of_file] or another PreOrder item passed to the constructor [__init__]. The method [closure] computes the transitive closure of the pre-order relations stored in the object [relations]; the method [geq] returns a Boolean value specifying whether there is a pre-order relation between two given elements of the pre-ordered set; the method [inf] returns the infimum of two elements of the pre-ordered set; and the method [presence] returns a Boolean value specifying whether an element belongs to the pre-ordered set.
   
>>> Method: .__init__
  [Actions] 
    .relations  <- use(name_of_file,*args)
    .transitive <- use(*args)
    .mask       <- use(name_of_file,*args)
    .cartesian  <- use(cartesian)
  [Description] 
    This method is the constructor of the class. 

>>> Method: .closure
  [Actions] 
    .transitive <- use()
    .relations  <- use(self.relations)
  [Description] 
    Computes the transitive closure of the pre-order relations in the object 
  [relations]

>>> Method: ._qeq
  [Actions] 
    return <- use(self.relations,element1,element2)
  [Description] 
    Specifies whether element1 is greater than or equal to element2.

>>> Method: .qeq
  [Actions] 
    return <- use(self.cartesian,self._geq,element1,element2)
  [Description] 
    Cartesian version of the method [_geq].

>>> Method: ._inf
  [Actions] 
    return <- use(self.relations,self.mask,self.geq,element1,element2)
  [Description] 
    Computes the infimum of element1 and element2.

>>> Method: .inf
  [Actions] 
    infimum <- use(self.cartesian,self._inf,element1,element2)
  [Description] 
    Cartesian version of the method [_inf].
    
>>> Method: .presence
  [Actions] 
    presence <- use(self.relations)
  [Description] 
    Specifies whether [element] belongs to the pre-ordered set.
'''
#------------------------------------------------------------------------------
#Global variables
#------------------------------------------------------------------------------
'''
The list _ascii_for_text defined below specifies the characters that can be used 
as a variable name for the elements of the pre-ordered set.
ASCII code 33: !
ASCII code between 48 to 57 : [0-9]
ASCII code 64 : @
ASCII code between 65 to 90 : [A-Z]
ASCII code 95 : _
ASCII code between 97 to 122 : [a-z]
'''
heading_separators = range(0,33) + range(34,48) + range(58,64) + range(91,95) + [96] + range(123,256)

for i in range(len(heading_separators)):
  heading_separators[i] = chr(heading_separators[i])

separators = heading_separators + ['!']
#------------------------------------------------------------------------------
#Dependencies: current, Useful
#------------------------------------------------------------------------------
import sys
sys.path.insert(0, '../Useful/')
from usf import usf
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class PreOrder(object):
#------------------------------------------------------------------------------  
  def __init__(self,name_of_file,cartesian = 0,*args):
    if cartesian > 0 and len(args)==1:
      self.relations = args[0].relations
      self.transitive = args[0].transitive
      self.mask = args[0].mask
      self.cartesian = cartesian
    else:  
      if name_of_file == '':
        print("Error in PreOrder.__init__: name of file is empty")
        exit()
      else:
        self.relations = list()
        self.transitive = False
        self.mask = False
        self.cartesian = cartesian

        with open(name_of_file,"r") as the_file:
        
          #Search the key words '!obj:' or 'obj:'
          list_of_objects = list()
          flag_obj = False
          while not(flag_obj):
            heading = usf.read_until(the_file,heading_separators,[':'])
            if heading != [] and heading[len(heading)-1] == "!obj":
              self.mask = True
              flag_obj = True
            elif heading != [] and heading[len(heading)-1] == "obj":
              flag_obj = True
            elif heading == []:
              print("Error in PreOrder.__init__: in \'"+\
              name_of_file+"\': \'obj:\' was not found")
              exit()
              
          #Search the key word 'rel:'
          flag_rel = False
          while not(flag_rel):
            line = usf.read_until(the_file,separators,['#',':'],inclusive=True)
            objects = list()
            if len(line) > 1 and line[len(line)-2:len(line)] == ["rel",":"]:
              objects = line[:len(line)-2]
              flag_rel = True
            elif line == ['']:
              break
            else:
              objects = line[:len(line)-1]
              usf.read_until(the_file,separators,['\n'])
              
            #Construct [list_of_objects] and [self.relations] 
            for i in range(len(objects)):
                usf.add_to(objects[i],list_of_objects)
                usf.add_to([objects[i]],self.relations)
                
          #If the key word 'rel:' is not found      
          if flag_rel == False:
            return
            
          #If the key word 'rel:' was found, search the symbols '>' and ';' 
          flag_EOF = False
          while not(flag_EOF):
            
            all_successors = list()
            flag_succ = False
            while not(flag_succ):
              line = usf.read_until(the_file,separators,['#','>'],inclusive=True)
              successors = list()
              if line[len(line)-1] == ">":
                successors = line[:len(line)-1]
                flag_succ = True
              elif line == ['']:
                break
              else:
                successors = line[:len(line)-1]
                usf.read_until(the_file,separators,['\n'])
                
            #Construct [all_successors]    
            for i in range(len(successors)):
                usf.add_to(successors[i],all_successors)  
            
            #Complete [self.relations] with [predecessors] for each successor
            predecessors = usf.read_until(the_file,separators,[';'])
            if all_successors == [] or predecessors == []:
              flag_EOF = True
            for i in range(len(all_successors)):
             try:
               index = list_of_objects.index(all_successors[i])
               for j in range(len(predecessors)):
                 usf.add_to(predecessors[j],self.relations[index])
             except:
               print("Warning in PreOrder.__init__: in \'"+\
               name_of_file+"\': "+ all_successors[i]+" is not an object")
#------------------------------------------------------------------------------
  def closure(self):
    if self.transitive == False:
      self.transitive = True
      for i in range(len(self.relations)):
        keep_going = True
        while keep_going:
          keep_going = False
          for elt in self.relations[i]:
            for j in range(len(self.relations)):
              if (j != i) and elt == self.relations[j][0]:
                for new_elt in self.relations[j]:
                  keep_going = usf.add_to(new_elt,self.relations[i])
#------------------------------------------------------------------------------                  
  def _geq(self,element1,element2):
    self.closure()
    flag = False
    index = 0
    for i in range(len(self.relations)):
      if self.relations[i][0] == element1:
        flag = True
        index = i
        break
    return flag and (element2 in self.relations[index]) 
#------------------------------------------------------------------------------   
  def geq(self,element1,element2):
    if self.cartesian == 0:
      return self._geq(element1,element2)
    else:
      for i in range(self.cartesian):
        if element2[i] != True and not(self._geq(element1[i],element2[i])):
          return False
      return True
#------------------------------------------------------------------------------    
  def _inf(self,element1,element2):
    self.closure()
    flag1 = False
    index1 = 0
    flag2 = False
    index2 = 0
    for i in range(len(self.relations)):
      if self.relations[i][0] == element1:
        flag1 = True
        index1 = i
      if self.relations[i][0] == element2:
        flag2 = True
        index2 = i
      if flag1 and flag2:
        break
    if not(flag1 and flag2):
      return self.mask
    else:
      copy1 = self.relations[index1][:]
      copy2 = self.relations[index2][:]
      intersect = list()
      for i in range(len(copy1)):
        for j in range(len(copy2)):
          if copy1[i] == copy2[j]:
            intersect.append(copy1[i])
            break
      if intersect != []:
        sup = intersect[0]
        for i in range(1,len(intersect)):
          if self.geq(intersect[i],sup):
            sup = intersect[i]
        return sup
      else:
        return self.mask
#------------------------------------------------------------------------------  
  def inf(self,element1,element2):
    if self.cartesian == 0:
      return self._inf(element1,element2)
    else:
      infimum = list()
      for i in range(self.cartesian):
        infimum.append(self._inf(element1[i],element2[i]))
      return infimum
#------------------------------------------------------------------------------  
  def presence(self,element):
      presence = False
      for j in range(len(self.relations)):
        if element == self.relations[j][0]:
          presence = True
          break
      return presence
#------------------------------------------------------------------------------          
