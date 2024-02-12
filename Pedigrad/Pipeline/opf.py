import gzip
from typing import IO

def open_file(filename: str,
              #List of inputs and their types
              mode: str = "r"
              #The output type
              ) -> tuple[IO,bool,str]:
  '''
  Takes the name of a file and a string specifying a file access mode.
  Returns a file pointer toward the input file sucht that the pointer is 
  set to the input access mode, a Boolean indicating whether the input file
  is compressed with gzip and a string indicating the extension of the input file.
  '''
  #Get the file format extension and the compression extension (if any)
  extensions = filename.split(".")[-2:]
  #Get the last extension
  file_format = extensions[-1] if extensions!=[] else None
  #Check if the last extension refers to a file format and a compression format
  isgzfile = file_format in ["gz","GZ"]
  #If the last extension is a compression format, get the file format from "extensions"
  if isgzfile:
    file_format = extensions[0]
    #return the file pointer with gzip
    return gzip.open(filename,mode), isgzfile, file_format
  #return the file pointer with the standard library
  return open(filename,mode), isgzfile, file_format
