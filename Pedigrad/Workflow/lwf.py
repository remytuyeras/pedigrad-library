from Pedigrad.Pipeline.opf import open_file
from Pedigrad.Pipeline.cl_prs import Parser
from .cl_pro import PreOrder
from typing import IO

keyword_chars = "#!:>;@_" + "0123456789" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "abcdefghijklmnopqrstuvwxyz"
pro_separators = [chr(k) for k in range(256) if not(chr(k) in keyword_chars)]
pro_bracketors = ["#",">",";","@"]

def load_workflow(# List of inputs and their types
                  filename: IO
                  # The output type
                  ) -> tuple[PreOrder,list[str]]:
  '''
  Takes a text file with a preorder specification and returns 2 outputs consiting of the corresponding preorder
  structure as a (closed) PreOrder instance and a list of special strings contained in the input text file. 
  To specify the preorder structure in a text file, use:
  - the key word "obj:" before specifying the list of objects in the preorder
  - the key word "rel:" before specifying the list of relations in the preorder
    e.g. the string "object1 object2 > object3 object4;" is translated as the following four relations:
      object1 > object3
      object1 > object4
      object2 > object3
      object2 > object4
  - the key word "!obj:" instead of "obj:" to add a (formal) initial element to the preorder structure.
  - the character "#" to start a single-line comment.
  - the character "@" to start a special instruction.
  '''
  #Objects used to initialize a PreOrder instance
  relations, transitive, mask = {}, False, False
  #Parsing the file containing the preorder specification
  filepointer, decoding, file_format = open_file(filename)
  parser = Parser(pro_separators,pro_bracketors)
  #Variables encoding the parsing automaton states
  collect_obj, collect_rel, collect_rel_source, collect_rel_target = False, False, False, False
  ignore_text, special_info = False, False
  sources, targets, special = [], [], []
  #Parsing loop
  for row, string in enumerate(filepointer):
    parser.read_line(string,decoding, file_format)
    #Goes through the parsing automaton
    for word in parser.line_values:
      #Updates the automaton state for each key word
      if word in ["#"]:
        ignore_text = True
        break
      if word in ["@"]:
        special_info = True
        continue
      if word == "!obj:":
        mask, collect_obj = True, True
        continue
      if word == "obj:":
        collect_obj = True
        continue
      if collect_obj and word == "rel:":
        collect_obj, collect_rel, collect_rel_source = False, True, True
        continue
      if not collect_obj and word == "rel:":
        raise Exception("List of objects undefined. The key word \"obj:\" or \"!obj\" is missing.")
      #Distinguishes the sources from the targets when parsing each preorder relations
      if collect_rel:
        if word == ">":
          collect_rel_source, collect_rel_target = False, True
          continue
        if word == ";":
          for source in sources:
            for target in targets:
              if not target in relations[source]:
                relations[source].append(target)
          sources, targets = [], []
          collect_rel_source, collect_rel_target = True, False
          continue
      #Memorizes course code associated with an object
      if special_info:
        special_info = False
        special.append(word)
        continue
      #Initializes the preorder relations with the reflexive relations
      if collect_obj and not special_info:
        relations[word] = []
        continue
      #Completes the relations as specified in the file
      if collect_rel and collect_rel_source:
        sources.append(word)
        continue
      if collect_rel and collect_rel_target:
        targets.append(word)
        continue
    #Skips text if starting with the character "#"
    if ignore_text:
      ignore_text = False
      continue
  return PreOrder(relations, transitive, mask), special