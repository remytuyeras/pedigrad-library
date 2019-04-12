#------------------------------------------------------------------------------
#name (Class item) | _ objects | _ methods
#------------------------------------------------------------------------------
'''
[Objects] 
  .name [Type] type

[Methods] 
  .name
        [Inputs: ]
          - name [Type] type
        [Outputs: ]
          - name [Type] type
           
[General description] 
  This structure 
    
>>> Method: .name

  [Actions] 
    .object  <- use(class & arg)
    .output <- use(class & arg)
  
  [Description] 
    This method


'''
#------------------------------------------------------------------------------
#CODE
#------------------------------------------------------------------------------
class _Useful:
#------------------------------------------------------------------------------  
  def fasta(self,name_of_file):
    names = list()
    sequences = list()
    with open(name_of_file,"r") as the_file:
      flag_EOF = False
      usf.read_until(the_file,[],['>'])
      while not(flag_EOF):
        name = usf.read_until(the_file,[':'],['\n','\r'])
        if name == []:
          flag_EOF = True
        else:
          names.append(name)
          sequences.append(usf.list_to_string(usf.read_until(the_file,['\n','\r'],['>'])))
    return (names,sequences)
#------------------------------------------------------------------------------  
  def trim_suffix(self,string,character):
    index = 0
    for i in range(len(string)):
      if string[len(string)-1-i] == character:
        index = i
        break
    return (string[:len(string)-1-i],string[len(string)-i:])
#------------------------------------------------------------------------------
  def trim_preffix(self,string,character):
    index = 0
    for i in range(len(string)):
      if string[i] == character:
        index = i
        break
    return (string[:i],string[i+1:])
#------------------------------------------------------------------------------ 
  def list_to_string(self,a_list):
    if a_list == []:
      return ''
    else:
      return a_list[0] + self.list_to_string(a_list[1:])
#------------------------------------------------------------------------------  
  def string_to_list(self,a_string):
    output = list()
    for i in range(len(a_string)):
      output.append(a_string[i])
    return output
#------------------------------------------------------------------------------  
  def cut_at(self,a_list,an_index):
    return a_list[0:an_index]+a_list[an_index+1:len(a_list)]
#------------------------------------------------------------------------------
  def add_to(self,element,a_list):
      flag_presence = False
      for i in range(len(a_list)):
        if a_list[i] == element:
          flag_presence = True
          break
      if flag_presence == False:
        a_list.append(element)
      return not(flag_presence)
#------------------------------------------------------------------------------   
  def read_until(self,a_file,separators,EOL_symbols,inclusive = False):
    words = list()
    read = a_file.read(1) 
    while not(read in EOL_symbols+['']):
      while read in separators and not(read in EOL_symbols+['']):
        read = a_file.read(1)
      if not(read in EOL_symbols+['']):
        word = ''
        while not(read in separators) and not(read in EOL_symbols+['']):
          word = word + read
          read = a_file.read(1)
        words.append(word)
    if inclusive == True:
      words = words+[read]
    return words
#------------------------------------------------------------------------------
  def inclusions(self,s,n,k):
      if k != 0 and k > n:
        return []
      elif k == 0:
        output = list()
        for i in range(n):
          output.append(s+i)
        return [output]
      else:
        l = list()
        for i in self.inclusions(s+1,n-1,k):
          for x in self.inclusions(s,1,0):
            l.append(x + i)
        return l + self.inclusions(s+1,n-1,k-1)
#------------------------------------------------------------------------------
usf = _Useful()
#------------------------------------------------------------------------------
