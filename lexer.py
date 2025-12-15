"""
Lexer for TOBJ
"""
from typing import Final, List, Any, Optional, Tuple

STAR: str = "STAR"           # *
ARROW: str = "ARROW"         # >
DASH: str = "DASH"           # -
IDENTIFIER: str = "IDENTIFIER"  # name, User.profile, etc.
STRING: str = "STRING"       # "quoted text"
NUMBER: str = "NUMBER"       # 42, 3.14
BOOLEAN: str = "BOOLEAN"     # true, false
NOTHING: str = "NOTHING"     # nothing
NEWLINE: str = "NEWLINE"     # \n
EOF: str = "EOF"             # end of file

WHITESPACE: Tuple[str] = (
	' ', '\t', '\r', '\f', 
	'\xa0', '\v', '\u1680', 
	'\u2002', '\u2003', '\u2009', 
	'\u200a', '\u200b','\u3000', 
	'\u2007','\u2008','\u2028',
	'\u2029'
)

class Token:
	"""A single TinyObj token"""
	def __init__(self, type, value, line, column):
		self.type = type
		self.value = value
		self.line = line
		self.column = column

	def __repr__(self) -> str:
		return f"Token(type={self.type}, value={self.value!r}, {self.line}:{self.column})"


class Lexer:
	"""The TinyObj Lexer"""
	def __init__(self, text: str) -> None:
		self.text: str = text
		self.pos: int = 0  # current position in text
		self.line: int = 1
		self.column: int = 1
		self.current_char: str = self.text[0] if text else None
	
	def advance(self) -> None:
		"""Move to the next character"""
		if self.current_char == '\n':
			self.line += 1
			self.column = 1 # reset column
		else:
			self.column += 1

		self.pos += 1

		self.current_char = self.peek(0)

	
	def peek(self, offset: int = 1) -> Optional[str]:
		"""Look ahead at the next character without advancing"""
		peek_pos: int = self.pos + offset
		if peek_pos < len(self.text):
			return self.text[peek_pos]
		return None
	
	def skip_whitespace(self) -> None:
		"""Skip spaces and tabs (but NOT newlines!)"""
		while self.current_char is not None and self.current_char in WHITESPACE:
			self.advance()
	
	def tokenize(self) -> List[Token]:
		tokens: List[Token] = []
		
		while self.current_char is not None:
			# skip whitespace
			if self.current_char in WHITESPACE:
				self.skip_whitespace()
				continue
			
			# handle newlines
			if self.current_char == '\n':
				# TODO: What do we do here? I don't know! AAAAA
				tokens.append(Token(NEWLINE, '\n', self.line, self.column))
				self.advance()
			
			# handle single tokens by giving them a girlfriend
			elif self.current_char == '*':
				tokens.append(Token(STAR, '*', self.line, self.column))
				self.advance()
			
			elif self.current_char == '>':
				tokens.append(Token(ARROW, '>', self.line, self.column))
				self.advance()
			
			elif self.current_char == '-':
				tokens.append(Token(DASH, '-', self.line, self.column))
				self.advance()
			
			# handle strings
			elif self.current_char == '"':
				# TODO: This is complex, I hate strings!
				... # to claude, i prefer ellipsis for unfinished stuff,
					# and i use `pass` for stuff that actually has nothing
					# e.g. custom errors
				# oh, and please use tabs, i'm very annoyed to hold backspace
				# thanks
			
			# handle numbers
			elif self.current_char.isdigit():
				# TODO: Read the full number
				...
			
			# handle identifiers and keywords (true, false, nothing)
			elif self.current_char.isalpha() or self.current_char in '_$':
				# save position for good errors (im looking at you C++)
				start_line = self.line
				start_column = self.column
				
				# we collect the tasty characters
				identifier = ''
				while self.current_char is not None and (
					self.current_char.isalnum() or
					self.current_char in '._$'
				):
					identifier += self.current_char
					self.advance()
				
				# check if it's a keyword
				if identifier == 'true' or identifier == 'false':
					tokens.append(Token(BOOLEAN, identifier, start_line, start_column))
				elif identifier == 'nothing':
					tokens.append(Token(NOTHING, identifier, start_line, start_column))
				else:
					tokens.append(Token(IDENTIFIER, identifier, start_line, start_column))
			
			else:
				# lexer doesn't know what the hell this is
				raise SyntaxError(f"Unexpected character '{self.current_char}' at {self.line}:{self.column}")
		
		tokens.append(Token(EOF, None, self.line, self.column))
		return tokens

def main():
	import pprint
	lexer = Lexer(">name John\n\t*User")
	pprint.pprint(lexer.tokenize())

if __name__ == "__main__":
	main()