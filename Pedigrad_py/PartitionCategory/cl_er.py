#------------------------------------------------------------------------------
#EquivalenceRelation: .classes, .range, .closure, .quotient
#------------------------------------------------------------------------------
'''
This class possesses two objects, namely
- .classes (list of lists);
- .range (integer);
and three methods, namely
- .__init__ (constructor);
- .closure;
- .quotient.

The constructor .__init__ takes between 1 and 2 arguments: the first argument should either be an empty list or a list of lists of indices (i.e. non-negative integers) and the second argument, which is optional, should an integer that is greater than or equal to the maximum index contained in the first input. 

If the first input is not empty, then it is stored in the object .classes while the object .range receives 
- either the second input, when it is given;
- or the maximum index contained in the first input when no second input is given.

E.g.
eq1 = EquivalenceRelation([[0,1,2,9],[7,3,8,6],[4,9,5]])
eq2 = EquivalenceRelation([[0,1,2,9],[7,3,8,7],[9,15]],18)

If the first input is empty, then the second argument is required. In this case, the object .classes receive the lists containing all the singleton lists containing the integers from 0 to the integer given in the second argument, which is, for its part, stored in the object .range.

E.g.
eq3 = EquivalenceRelation([],5)
eq3.classes = [[0], [1], [2], [3], [4], [5]]


The method .closure replaces the content of the object .classes with the transitive closure of its classes. After this procedure, the object .classes describes an actually equivalence relation (modulo the singleton equivalence classes, which do not need to be specified for obvious reasons).

eq1.closure() 
eq1.classes = [[7, 3, 8, 6], [4, 9, 5, 0, 1, 2]]
eq2.closure() 
eq2.classes = [[7, 3, 8], [9, 15, 0, 1, 2]]

The method .quotient() returns a list of integers whose length is equal to the integer stored in the object .range decreased by 1 and whose non-trivial fibers are those contained in the object .classes.

eq1.quotient() = [1, 1, 1, 0, 1, 1, 0, 0, 0, 1] 
eq2.quotient() = [1, 1, 1, 0, 2, 3, 4, 0, 0, 1, 5, 6, 7, 8, 9, 1, 10, 11, 12]

'''

from jpop import _join_preimages_of_partitions


class EquivalenceRelation:
  #The objects of the class are:
  #. classes (list of lists);
  #. range (integer);
  #The following constructor takes between 1 and 2 arguments, 
  #the first one being a list and the second being an integer.
  def __init__(self,*args):
    #The local function is_index allows us to check whether an variable contains
    #an non-negative integer or not. It returns True if an non-negative integer
    #is given.
    def is_index(x):
      try: 
        return (int(x) == x) and (x >= 0)
      except:
        return False 
    #Checks that the number of arguments is correct.
    if not(len(args) in [1,2]):
      print("Error: in EquivalenceRelation.__init__: takes between 1 and 2 arguments ("+len(args)+" given).")
      exit()
    else:
      #The variable 'elements' records the set of indices on which the
      #the list of lists of indices given in a first input is defined.
      elements = list()
      for i in range(len(args[0])):
        for j in args[0][i]:
          #The elements should be non-negative integers. If there are not, the 
          #procedure outputs an error message and exits the program.
          if not(is_index(j)):
            print("Error: in EquivalenceRelation.__init__: the first input should be a list of lists of non-negative integers.")
            exit()
          #Elements that appear several are only counted once.
          elif not(j in elements):
            elements.append(j)
      #The variable 'individuals' contains the number of distinct elements that
      #the first input contains.
      if elements != []:
        individuals = max(elements)
        #If a second input is given, the following lines check that it is greater
        #then or equal to the maximum index contained in the first input.
        if len(args) == 2:
          if args[1] < individuals:
            print("Error: in EquivalenceRelation.__init__: the given range is smaller than the maximum element of the given classes.")
            exit()
          else:
            #If so, we want to assign the value of args[1] to the object .range.
            #This is done by firs passing it 'individuals' and self.range (as
            #shown below).
            individuals = args[1]
        #The object range contains the cardinal of the set on which the first input
        #is defined while the object .classes stores the list of lists given in the
        #first input.
        self.range = individuals
        self.classes = args[0]
      else:
        if len(args)!= 2:
          print("Error: in EquivalenceRelation.__init__: the first argument is trivial; a second argument required.")
          exit()
        else:
          if is_index(args[1]):
            self.range = args[1]
          else:
            print("Error: in EquivalenceRelation.__init__: the second argument should be a non-negative integer.")
            exit()
          self.classes = list()
          for i in range(self.range+1):
            self.classes.append([i])
      
  #The following function replaces the content of the object .classes with
  #the transitive closure of its classes. After this procedure, the object
  #.classes describes an actually equivalence relation (modulo the singleton
  #equivalence classes, which do not need to be specifid for obvious reasons).
  def closure(self):
    self.classes = _join_preimages_of_partitions(self.classes,self.classes)
    
  def quotient(self):
    #The quotient cannot be given if the lists contained in the object .classes
    #do not define an equivalence relation. To prevent an ill-defined quotient,
    #the classes are turned into an actual equivalence relation by completing
    #.classes transitively.
    self.closure()
    #Allocates a space in the memory to store the partition associated
    #with the equivalence relation defined by self.classes.
    the_quotient = list()
    #Allocates spaces in the memory in order to allow the access 
    #to the positions of the elements of the partition without 
    #using the method .append (at the end of the procedure).
    for i in range(self.range+1):
      the_quotient.append("?")
    #Now that the partition has the right number of allocated spaces in 
    #the memory, we can fill it by using the positions instead of 
    #appending elements.
    for i in range(len(self.classes)):
      for j in range(len(self.classes[i])):
        #The partition contains the integer i at the position self.classes[i][j].
        the_quotient[self.classes[i][j]]=i
    #The following lines are meant to fill the missing images in. 
    #The indices of these images corresponds to those indices that either 
    #do not appear among the indices of the object .classes or belongs to
    #singleton classes in the object .classes. The quotient should therefore
    #give them images that are not shared with other indices.
    k = len(self.classes)
    for i in range(len(the_quotient)):
      if the_quotient[i] == "?":
        the_quotient[i] = k
        k = k + 1
    return the_quotient
