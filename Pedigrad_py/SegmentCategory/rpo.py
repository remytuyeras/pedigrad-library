#------------------------------------------------------------------------------
#_read_pre_order(name_of_file): 2-tuple (Boolean value, list of lists)
#------------------------------------------------------------------------------
'''
This function takes the name of a file (called name_of_file) and returns a Boolean value and a list of lists.

The input file is supposed to describe a pre-ordered set as follows. Its set of elements should be specified in terms of a list of words succeeding one of the key words 'obj:' or '!obj:' as follows

[obj:][name1][separator][name2][separator] (etc.)

The labels [name1] and [name2] stand for words that should only be made of the characters [0-9], @, [A-Z], _ and [a-z] while the label [separator] stands any character that is not in this list of characters.

While the key word [obj:] is only supposed to present the list of elements of the pre-ordered set, the key word [!obj:] should only be used to add a formal initial object to the pre-ordered set.

For their parts, the pre-order relations of the set should be specified after the key word 'rel:' by a list of phrase satisfying the following syntax.

[dominant_object]>[predecessor1][separator][predecessor2] (etc.) ;

Such a line means that [dominant_object] is greater than or equal to all the elements listed after the symbol '>'. The list of 'predecessors' stops at the symbol ';'. Note that the symbol ';' can be omitted for the last line of the file. 

The labels [dominant_object] and [predecessor(n)] stand for words that should only be made of the characters [0-9], @, [A-Z], _ and [a-z] while the label [separator] stands any character that is not in this list of characters.

Comments are also allowed and are specified as in python, with the character #. An example of such a file is given below:

------------------------------------------------
#This is a example of pre-ordered set

!obj:  
- color_1    #object with color 1
- color_2    #object with color 2
- color_3    #object with color 3
- color_4    #object with color 4

rel: #these are generating relations for the preorder
 - color_1> color_2, color_3;
 - color_1 > color_3, color_1;
 - color_3>color_4 ;
 - color_2 >color_4
------------------------------------------------

The output then is a pair 

(flag_zero_obj,the_pre_order) 

 - whose first component flag_zero_obj is a Boolean value specifying by False or True whether the word 'obj:' (False) or '!obj:' (True) was used to define the list of objects 
 - and whose second component the_pre_order is a list of lists giving the non-transitive down-closures of the elements of the pre-ordered set in the order in which these were given in the input file.

A list in the list the_pre_order will always start with the element of which it is supposed to give the down-closure, as shown below.

[dominant_object, predecessor1, predecessor2, etc.]

For instance, the ouput of previous example is as follows:

flag_zero_obj = True

the_pre_order = [
['color_1', 'color_2', 'color_3'],
['color_2', 'color_4'],
['color_3', 'color_4'],
['color_4'],
]

'''
#The following list specifies the characters that can define 
#a valid name for the elements of the pre-ordered set.
#ascii code between 48 to 57 : [0-9]
#ascii code 64 : @
#ascii code between 65 to 90 : [A-Z]
#ascii code 95 : _
#ascii code between 97 to 122 : [a-z]
_ascii_for_text = range(48,58)+[64]+range(65,91)+[95]+range(97,123)


def _read_pre_order(name_of_file):
  if name_of_file == '':
    return (False,[])
  else:  
    # Opens the input file.
    the_file = open(name_of_file,"r")
    # Saves the text at the address of the variable the_text.
    the_text = str(the_file.read())
    # Closes the file.
    the_file.close()
    #A space is allocated to store the input in the memory.
    the_pre_order = list()
    #A space is allocated to store the objects of the preorder 
    #independently of the input.
    list_of_objects = list()
    #Records the current reading position in the text saved in the memory.
    position = 0
    #The variables flag_obj and flag_rel indicate if the key 
    #words "obj:" and "rel:"
    flag_obj = False
    flag_rel = False
    #The variable flag_zero_obj indicates if the the pre-ordered set contains
    #an initial object (min) formally added (hence not specified via the input
    #file.
    flag_zero_obj = False
    #PART 1: The following loop reads the text until the end of file is 
    #reached or until the key word 'rel:' is found. The role of this part
    #is to record the list of objects of the pre-ordered set.
    while position < len(the_text):
      #STEP 1: Searches the key word 'obj:'. As long as 'obj:' is not found, 
      #the file is parser by following the procedure given below.
      if flag_obj == False:
        #Detects the key word "!obj:". If detected, then moves 
        #forward by len("!obj:").
        if position+5 <= len(the_text) and the_text[position:position+5] == "!obj:":
          position = position +6
          flag_obj = True
          flag_zero_obj = True
        #Detects the key word "!obj:". If detected, then moves 
        #forward by len("obj:").
        elif position+4 <= len(the_text) and the_text[position:position+4] == "obj:":
          position = position +5
          flag_obj = True
        #Otherwise, it moves by len(the_text[position]) (the length of a character).
        else:
          position = position +1
      #STEP 2: The key word 'obj:' was found and the procedure now searches 
      #the names of the objects until it finds the key word 'rel:'. 
      #Any word made of the characters in the list _ascii_for_text defines 
      #a valide object. The name of valid objects can be separated by any 
      #character that is not in the list _ascii_for_text and is not #  
      #(e.g. !,.?}; etc.). Comments starts with the symbol # and the text
      #following it is then ignored.
      if flag_obj == True:
        #Looks for a character _ascii_for_text. This character is, by definition
        #the first letter of the name of valid objects.
        while position < len(the_text) and not(ord(the_text[position]) in _ascii_for_text):
          #Takes care of the comments in the file.
          if the_text[position] == '#':
            while position < len(the_text) and the_text[position] != '\n':
              position = position + 1
          else:
            position = position + 1
        #The first letter of the name of a valid object has been found. 
        #The position of this letter is saved in the memory.
        save = position
        #Reads the name of the valid objects until it cannot find 
        #characters in the list _ascii_for_text or reaches the end of file.
        while position < len(the_text) and ord(the_text[position]) in _ascii_for_text:
          position = position + 1
        #Parses the word between the saved position (in 'save') and the 
        #current position in the text. If the word is 'rel' and in fact the key
        #word 'rel:' than the procedure exists the loop and set flag_rel to true.
        if position+1 <= len(the_text) and the_text[save:position+1] == "rel:":
          flag_rel = True
          break
        #If the word is not the key word 'rel:' and the name defines a valid 
        #object for the pre-ordered set. It is recorded in the lists 
        #list_of_objects and the_pre_order.
        else:
          if position < len(the_text) and not(the_text[save:position] in list_of_objects):
            list_of_objects.append(the_text[save:position])
            the_pre_order.append([the_text[save:position]])
    #PART 2: controls if the key word 'obj:' has been found. If not found, the
    #procedure outputs an error message and exits the program.
    if flag_obj == False:
      print("Error: in \'"+name_of_file+"\': \'obj:\' was not found")
      exit()
    #PART 3: This parts reads the pre-order relations existing between 
    #the objects of the pre-ordered set. The realtions are always 
    #specified by giving the dominant first and all its predecessors 
    #after a symbol '>'. The relation given are only 'generating relations',
    #which means the the actual pre-order structure is obtained after 
    #transitive completion.
    #----------------------------------------------------------------------------
    #The dominant objects are memorized in the variable 'dominant_object' 
    #and the variable 'flag_dominant' indicates whether a dominant object 
    #has just been read so that the objects being read have to be its
    #predecessors.  
    dominant_object = ''
    flag_dominant = False
    #If the key word 'rel:' has been found in the previous loop, the 
    #relations are read according to the format:
    #
    # [dominant_object][>][predecessor1][separator][predecessor2] etc. [;]
    #
    #Thus, there are two special characters to look for: the symbol > 
    #that initializes the list of predecessors and the symbol ; that 
    #indicates the end of the list of predecessors.
    while flag_rel == True and position < len(the_text):
        #STEP 1: Looks for a character _ascii_for_text. This character is, 
        #by definition the first letter of what could be the name of valid
        #objects recorded in the list list_of_objects.
        while position < len(the_text) and not(ord(the_text[position]) in _ascii_for_text):
          #Takes care of the comments in the file.
          if the_text[position] == '#':
            while position < len(the_text) and the_text[position] != '\n':
              position = position + 1
          #Detects the character ';' and set the variable flag_dominant to False
          elif the_text[position] == ';':
            dominant_object = ''
            flag_dominant = False
            position = position + 1
          #Detects the character '>' and set the variable flag_dominant to True
          elif the_text[position] == '>':
            #Checks if the character '>' has already been read and has not been
            #closed by a symbol ';'. In this case, the symbol ';' might have
            #been forgotten by the user.
            if flag_dominant == False:
              flag_dominant = True
              position = position + 1
            else:
              print("Error: in \'"+name_of_file+"\': key word '>' is repeated")
              exit()
          #All other characters that are not in list_of_objects in are ignored.
          else:
             position = position + 1
        #STEP 2: The first letter of what can be the name of a valid object has 
        #been found. The position of this letter is saved in the memory.
        save = position
        #Reads the name of the valid objects until it cannot find 
        #characters in the list _ascii_for_text or reaches the end of file.
        while position < len(the_text) and ord(the_text[position]) in _ascii_for_text:
          position = position + 1
        #Note that the following conditions does not prevent the reading of
        #the last word of the file since this last word should be always
        #succeeded by a formal character '\n' and then the end of file. 
        #This comes from the way the procedure open(-,"r") reads the file.
        if position < len(the_text):
          #The specification of the pre-order relations should not include
          #new objects. The following lines check if the name recorded from
          #'save' to 'position' is in the list 'list_of_objects'.
          if not(the_text[save:position] in list_of_objects):
            print("Error: in \'"+name_of_file+"\': "+the_text[save:position]+" is not an object")
            exit()
          #If the name read is actually part of the set of objects, the following
          #lines deals with this object differently depending on whether it is
          #a dominant object or a successor of a dominant object.
          else:
            #If a dominant object has not been attributed yet, then 
            #the_text[save:position] is the name of a dominant object.
            if flag_dominant == False:
              dominant_object = the_text[save:position]
            else:
              #If the symbol '>' has been read (i.e. flag_dominant == True), 
              #but the name of the dominant object is empty, then the relation
              #is missing its dominant object in the file. E.g.
              #
              #[ ][>][predecessor1][separator][predecessor2] etc. [;]
              #
              if dominant_object == '':
                print("Error: in \'"+name_of_file+"\': relation is missing a dominant object")
                exit()
              else:
                #Otherwise, the name of the object is appended to the down-
                #closure of the dominant object as follows.
                #1) The following line gets the index of the dominant object.
                index_dominant = list_of_objects.index(dominant_object)
                #2) Reflexive relations are ignored.
                if not(the_text[save:position] in the_pre_order[index_dominant]):
                  #3) The name is appended to the down-closure of the 
                  #dominant object
                  the_pre_order[index_dominant].append(the_text[save:position])
    #Returns a Boolean value indicating whether the pre-order has a 
    #formal initial object and a list of lists giving the down-closure of
    #the objects of the pre-ordered set.        
    return (flag_zero_obj,the_pre_order)   
