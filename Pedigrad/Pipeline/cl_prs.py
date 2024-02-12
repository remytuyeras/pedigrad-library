
from __future__ import annotations
from typing import  Any, Callable, IO, Union

PSchemaArg = lambda prs: Callable[[prs,int,str,Any],bool]
PSchemaOut = lambda prs: Callable[[prs,IO],Callable[[Any],IO]]

class Parser(object):

	__slots__ = ("separators","bracketors","line_values","line_pointers")

	def __init__(self,
							 #List of inputs and their types
							 separators: list[str],
							 bracketors: list[str]
							 #The output type
							 ) -> None:
		#Special characters used for splitting the text during parsing
		self.separators: list[str] = separators
		#Special characters to be parsed as key words
		self.bracketors: list[str] = bracketors
		#Parsed words for each line
		self.line_values: list[str] = []
		#Positions of the parsed words for each line
		self.line_pointers: list[int] = []

	def _format_bracketors(self,
												 #List of inputs and their types
												 file_format: str
												 #The output type
												 ) -> list[str]:
		'''
		Adds format-specific special characters to the list of "bracketors".
		'''
		symbols = []
		if file_format.lower() in ["csv"]:
			symbols.extend([",","\""])
		if file_format.lower() in ["vcf"]:
			symbols.extend(["#","=","<",">",",","\""])
		if file_format.lower() in ["fa", "fasta", "fna", "ffn", "faa", "frn"]:
			symbols.extend([">","|"])
		return symbols

	def _read(self,
						#List of inputs and their types
						string: str,
						file_format: str,
						threshold: Union[None,int] = None
						#The output type
						) -> None:
		'''
		Parses a string (e.g. a line in a text file) according to the list 
		of bracketors and separators given to the class. 
		Specifically, the separators are ignored while the bracketors are 
		parsed as distinctive key words. The function fills the variables
		self.line_values and self.line_pointers with the parsed words and 
		the position of each corresponding word, respectively. The code of
		the function is optimized for the parsing of large files.
		''' 
		#Constains the parsed words for a given string
		self.line_values = []
		#Constains the positions of each parsed words for a given string
		self.line_pointers = []
		#Additinal bracketors to add to the parsing due to the file extension
		fbracketors = self._format_bracketors(file_format)
		#Indices memorizing the word positions
		i_previous, i_current = 0, 0
		#Loop for the parsing of the input string
		while i_current < len(string) and (threshold == None or len(self.line_values) < threshold):
			if (string[i_current] in self.separators) or (string[i_current] in (self.bracketors + fbracketors)):
				#Adds a word to the list of parsed words
				if i_previous != i_current:
					self.line_values.append(string[i_previous:i_current])
					self.line_pointers.append(i_previous)
				#Parses the bracketors given as an input and those related to the file format
				if string[i_current] in (self.bracketors+fbracketors):
					self.line_values.append(string[i_current:i_current+1])
					self.line_pointers.append(i_current)
				i_previous = i_current + 1
			i_current = i_current + 1
		#Takes care of the last word in the text file
		if i_previous != i_current and (threshold == None or len(self.line_values) < threshold):
			self.line_values.append(string[i_previous:i_current])
			self.line_pointers.append(i_previous)

	def read_line(self,
								#List of inputs and their types
								string: str,
								decoding: bool,
								file_format: str,
								threshold: Union[None,int] = None
								#The output type
								) -> None:
		'''
		Decodes input strings if given in binary format and applies the private 
		method _read on the resulting strings.
		'''
		#Decodes the input string if this string originates from a compressed file
		if decoding:
			string = string.decode()
		#Parses the resulting string (which is stripped from any " " or "\r" charaters at the end)
		self._read(string.rstrip(),file_format,threshold = threshold)

	def metadata(self,
							 #List of inputs and their types
							 file_format: str
							 #The output type
							 ) -> bool:
		'''
		Returns a Boolean value indicating whether the line is metadata.
		'''
		if file_format.lower() in ["vcf"]:
			return self.line_values[:2] == ["#","#"]
		return False

	def attributes(self,
								 #List of inputs and their types
								 row: int,
								 file_format: str
								 #The output type
								 ) -> bool:
		'''
		Returns a Boolean value indicating whether the line contains (column) attributes and labels
		to be asscociated with the data.
		'''
		if file_format.lower() in ["vcf"]:
			return self.line_values[:1] == ["#"] and not "#" in self.line_values[1:2]
		if file_format.lower() in ["fa", "fasta", "fna", "ffn", "faa", "frn"]:
			return self.line_values[:1] == [">"]
		if file_format.lower() in ["txt", "csv"]:
			return row == 0
		return False

	@staticmethod
	def PipelineSchema(#List of inputs and their types
										 f: PSchemaArg[Parser]
										 #The output type
										 ) -> PSchemaOut[Parser]:
		"""
		Decorates the input function f as the function wrapper shown below. The decorator
		iterates on the lines of a file starting from the position of the file pointer 
		given as an input to the wrapper. The decorator stops when the input function f
		returns a value logically equivalent to False.
		"""
		def wrapper(self: Parser,filepointer: IO) -> Callable[[Any],IO]:
			#This additional function allows us to use arbitrary parameters	
			def analyzer(*parameters: Any) -> IO:
				for row, string in enumerate(filepointer):
					#Apply the function f on each line information
					if f(self,row,string,*parameters):
						#Continue if f returns True
						pass
					else:
						#Stop if f returns False
						break
				#Return the file pointer
				return filepointer
			#Return the intermediate function handling the arbitrary parameters
			return analyzer
		#Return the wrapper decorating the input function f
		return wrapper
