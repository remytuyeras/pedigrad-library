#------------------------------------------------------------------------------
#read_alignment_file(name_of_file,reading_mode): 2-tuple
#------------------------------------------------------------------------------
'''
This function takes the name of a file (called name_of_file) and an integer and returns a pair of lists (names, alignment)

The input file should be of the following form.

>Name of taxon1
Sequence1 (a text that does not contain the character >)
>Name of taxon2
Sequence2 (a text that does not contain the character >)
etc.

The first output 'names' is a list of strings containing the names placed after the symbol '>' in the input file; e.g. [Name of taxon1, Name of taxon2, etc.]

The second output 'alignment' is a list of lists of characters that spell each text displayed after the names saved in the list called 'names'; e.g. [Sequence1, Sequence2, etc.]

The index of a name in 'names' corresponds to the index of its associated text in 'alignment'.
'''
READ_DNA = 1

def read_alignment_file(name_of_file,reading_mode):
  # Opens the input file.
  the_file = open(name_of_file,"r")
  # Saves the text at the address of the variable the_text.
  the_text = str(the_file.read())
  # Closes the file.
  the_file.close()
  #Spaces are allocated to store the two inputs in the memory.
  alignment = list()
  names = list()
  #Records the current reading position in the text saved in the memory.
  position = 0
  #Reads the text until the last character.
  while position < len(the_text):
    #Detects the name of a taxon.
    if the_text[position] == '>':
      position = position+1
      #Remembers where the name of the taxon starts.
      save = position
      #Reads until reaching the end of text or a escape sequence
      #the excerpt read in this way is the name of the taxon.
      while position < len(the_text) and the_text[position] != '\n':
        position = position+1
      #Saves the name of the taxon in the list 'names'.
      names.append(the_text[save:position])
      position = position+1
      #Allocates a space in the memory to save the sequence
      #associated with the taxon.
      sequence = list()
      #Reads until reaching the end of text or the character '>'
      #the excerpt read in this way is the sequence asscoaited with the taxon.
      while position+1 < len(the_text) and the_text[position+1] != '>':
        #All characters except for the escape sequence character
        #are included in the text displayed below the taxon.
        if the_text[position]!= '\n':
          #If the global variable READ_DNA is given as input
          #Turns lower case letters 'a', 'c', 'g' and 't' into
          #their upper case versions 'A', 'C', 'G', 'T'.
          if reading_mode == 1 and ord(the_text[position]) in [97,99,103,116]:
            sequence.append(chr(ord(the_text[position])-32))
          #Any other character is read as is.
          else:
            sequence.append(the_text[position])
        #The reading position goes to the next character
        #the iteration starts again.
        position = position+1
      #After reaching '>', the text is appended to the list 'alignment'.
      alignment.append(sequence)
    #The reading position moves forward until it reaches
    #the next character '>' or the end of file.
    position = position+1
  #Outputs both the lists of names and the list of texts.
  return (names,alignment)
