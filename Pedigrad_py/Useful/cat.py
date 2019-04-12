#------------------------------------------------------------------------------
#name (Class) | _ objects | _ methods
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
class CategoryItem(object):
  def __init__(self,level,*args):
    self.level = level
    if len(args) == 2 and args[0].level == level-1 and args[1].level == level-1:
      self.source = args[0]
      self.target = args[1]
#------------------------------------------------------------------------------
