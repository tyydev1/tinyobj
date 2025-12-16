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
	
	def skip_comment(self) -> None:
		"""Skip characters until the end of the line"""
		while self.current_char is not None and self.current_char != '\n':
			self.advance()
	
	def tokenize(self) -> List[Token]:
		tokens: List[Token] = []
		
		while self.current_char is not None:
			# skip whitespace
			if self.current_char in WHITESPACE:
				self.skip_whitespace()
				continue
			
			# 1. Handle # comments
			if self.current_char == '#':
				self.skip_comment()
				continue
			
			# 2. Handle // comments
			# check if current is '/' and the next one is also '/'
			if self.current_char == '/' and self.peek() == '/':
				self.skip_comment()
				continue

			if self.current_char == '.' and self.peek() == '.' and self.peek(2) == '.':
				self.skip_comment()
				continue

			# handle newlines
			if self.current_char == '\n':
				tokens.append(Token(NEWLINE, '\n', self.line, self.column))
				self.advance()
			
			# handle single tokens by giving them a girlfriend
			elif self.current_char == '*':
				tokens.append(Token(STAR, '*', self.line, self.column))
				self.advance()
			
			elif self.current_char == '>':
				tokens.append(Token(ARROW, '>', self.line, self.column))
				self.advance()
			
			# handle numbers
			elif self.current_char.isdigit() or (self.current_char == '-' and self.peek() and self.peek().isdigit()):
				start_line = self.line
				start_column = self.column
				
				number = ''
				
				# handle negatives
				if self.current_char == '-':
					number += '-'
					self.advance()
				
				# read them digits
				while self.current_char is not None and self.current_char.isdigit():
					number += self.current_char
					self.advance()
				
				# handle decimal dots for floating (i'm floating!)
				if self.current_char == '.' and self.peek() and self.peek().isdigit():
					number += '.'
					self.advance()
					while self.current_char is not None and self.current_char.isdigit():
						number += self.current_char
						self.advance()
				
				tokens.append(Token(NUMBER, number, start_line, start_column))
			

			elif self.current_char == '-':
				tokens.append(Token(DASH, '-', self.line, self.column))
				self.advance()
			
			# handle strings
			elif self.current_char == '"':
				start_line: int = self.line
				start_column: int = self.column
				self.advance()
				
				string_value: List[str] = []

				while self.current_char is not None and self.current_char != '"':
					# is ts escape?
					if self.current_char == '\\':
						# oh boy it's escaping time
						self.advance()
						if self.current_char == 'n':
							string_value.append('\n')
						elif self.current_char == 't':
							string_value.append('\t')
						elif self.current_char == '"':
							string_value.append('"')
						elif self.current_char == '\\':
							string_value.append('\\')
						else: # unknown escape
							string_value.append(self.current_char)
						self.advance()
					else:
						string_value.append(self.current_char)
						self.advance()
				
				# oh boy errors!
				if self.current_char != '"':
					raise SyntaxError(f"Unterminated string (you didn't close the string) at {start_line}:{start_column}")

				self.advance()
				tokens.append(Token(STRING, "".join(string_value), start_line, start_column))

			
			# handle identifiers and keywords (true, false, nothing)
			elif self.current_char.isalpha() or self.current_char in '_$':
				# save position for good errors (im looking at you C++)
				start_line = self.line
				start_column = self.column
				
				# we collect the tasty characters
				identifier = ''
				while self.current_char is not None and (
					self.current_char.isalnum() or
					self.current_char in '._$+'
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
	lexer = Lexer("*Temps >readings - -5 - 10 - -3.14")
	pprint.pprint(lexer.tokenize())

if __name__ == "__main__":
	main()