"""
The TinyObj Parser
"""

# -------------------
# Errors
# -------------------

class UnexpectedTokenError(Exception):
	pass

class PropertyError(Exception):
	pass

# -------------------
# Nodes
# -------------------

class ASTNode:
	"""Base class for all AST nodes"""
	def __init__(self, line: int, column: int):
		self.line = line
		self.column = column

class ObjectNode(ASTNode):
	"""Represents an object declaration: *ObjectName"""
	def __init__(self, path: str, line: int, column: int):
		super().__init__(line, column)
		self.path = path  # "User" or "User.profile.settings"
	
	def __repr__(self) -> str:
		return f"ObjectNode({self.path!r})"

class PropertyNode(ASTNode):
	"""Represents a property assignment: >key value"""
	def __init__(self, key: str, value, line: int, column: int):
		super().__init__(line, column)
		self.key = key      # "name" or "User.name"
		self.value = value  # Python value
	
	def __repr__(self) -> str:
		return f"PropertyNode({self.key!r}, {self.value!r})"

# -----------------
# Parser
# -----------------

from typing import List, Optional
from lexer import Token, STAR, ARROW, DASH, IDENTIFIER, STRING, NUMBER, BOOLEAN, NOTHING, NEWLINE, EOF

class Parser:
	"""The TinyObj Parser"""
	def __init__(self, tokens: List[Token]):
		self.tokens: List[Token] = tokens
		self.pos: int = 0
		self.current_token: Token = self.tokens[0] if tokens else None
	
	def advance(self) -> None:
		"""Move to next token"""
		# TODO: Implement this
		self.pos += 1
		self.current_token = self.peek(0)
	
	def peek(self, offset: int = 1) -> Optional[Token]:
		"""Look ahead at future tokens"""
		# TODO: Implement this
		peek_pos: int = self.pos + offset
		if peek_pos < len(self.tokens):
			return self.tokens[peek_pos]
		return None
	
	def expect(self, token_type: str) -> Token:
		"""Consume a token of expected type, or raise error"""
		# TODO: Implement this
		if self.current_token.type == token_type:
			token: Token = self.current_token
			self.advance()
			return token
		else:
			raise UnexpectedTokenError(
				f"Expected {token_type}, but got {self.current_token.type} "
				f"at {self.current_token.line}:{self.current_token.column}"
			)		
	
	def skip_newlines(self) -> None:
		"""Skip any NEWLINE tokens"""
		while self.current_token is not None and self.current_token.type == NEWLINE:
			self.advance()
	
	def token_to_value(self, token: Token):
		"""Convert a token to its Python value"""
		if token.type == STRING:
			return token.value
		elif token.type == NUMBER:
			if '.' in token.value:
				return float(token.value)
			else:
				return int(token.value)
		elif token.type == BOOLEAN:
			return token.value == 'true'
		elif token.type == NOTHING:
			return None
		elif token.type == IDENTIFIER:
			return token.value
		else:
			raise UnexpectedTokenError(f"Unexpected value token: {token.type}")

	def parse_object(self) -> ObjectNode:
		"""Parse object declaration: *ObjectName"""
		star_tok: Token = self.expect('STAR')
		name_tok: Token = self.expect('IDENTIFIER')

		return ObjectNode(
			path=name_tok.value,
			line=star_tok.line,
			column=star_tok.column
		)

	def parse_list_items(self) -> List:
		"""Parse list items (handles both one-line and multi-line)"""
		items: List = []
		
		while self.current_token.type == DASH:
			# TODO: You implement this
			self.expect(DASH)  # Consume the dash
				
			# Read the value
			value_tok: Token = self.current_token
			self.advance()
			value = self.token_to_value(value_tok)
			items.append(value)
			
			if self.current_token.type == NEWLINE:
				self.skip_newlines()
		
		return items

	def parse_property(self) -> PropertyNode:
		arrow_tok: Token = self.expect(ARROW)

		if self.current_token.type in (BOOLEAN, NOTHING):
			raise UnexpectedTokenError(
				f"Cannot use keyword '{self.current_token.value}' as property key. "
				f"Use quotes if you want a literal key: >\"{self.current_token.value}\" "
				f"at {self.current_token.line}:{self.current_token.column}"
			)

		if self.current_token.type == IDENTIFIER:
			key_tok: Token = self.expect(IDENTIFIER)
		elif self.current_token.type == STRING:
			key_tok: Token = self.expect(STRING)
		else:
			raise UnexpectedTokenError(
				f"Expected property key (identifier or string), got {self.current_token.type} "
				f"at {self.current_token.line}:{self.current_token.column}"
			)
		
		# what's next? come at me!
		if self.current_token.type == DASH:
			return PropertyNode(
				key_tok.value, 
				self.parse_list_items(),
				arrow_tok.line, 
				arrow_tok.column
			)
		
		elif self.current_token.type == NEWLINE:
			# might be multi-line list starting on next line
			self.skip_newlines()
			
			if self.current_token.type == DASH:
				return PropertyNode(
					key_tok.value, 
					self.parse_list_items(),
					arrow_tok.line, 
					arrow_tok.column
				)
			else:
				return PropertyNode(
					key_tok.value,
					None,
					arrow_tok.line,
					arrow_tok.column
				)
		
		else:
			# Simple property with value
			value_tok: Token = self.current_token
			self.advance()
			value = self.token_to_value(value_tok)
			return PropertyNode(key_tok.value, value, arrow_tok.line, arrow_tok.column)

	def parse(self) -> List[ASTNode]:
		"""Main parsing method"""
		nodes: List[ASTNode] = []
		
		while self.current_token is not None and self.current_token.type != EOF:
			self.skip_newlines()
			
			if self.current_token.type == STAR:
				node: ASTNode = self.parse_object()
				nodes.append(node)
			elif self.current_token.type == ARROW:
				node: ASTNode = self.parse_property()
				nodes.append(node)
			elif self.current_token.type == EOF:
				break
			else:
				raise UnexpectedTokenError(
					f"Unexpected token {self.current_token.type} "
					f"at {self.current_token.line}:{self.current_token.column}"
				)
		
		return nodes

def main():
	from lexer import Lexer
	import pprint
	
	tobj_code = """
*User
>name Alice
>age 30
>tags
- python
- rust
- C++
"""
	
	# Lex it
	lexer = Lexer(tobj_code)
	tokens = lexer.tokenize()
	print("=== TOKENS ===")
	pprint.pprint(tokens)
	
	# Parse it
	parser = Parser(tokens)
	ast = parser.parse()
	print("\n=== AST ===")
	pprint.pprint(ast)

if __name__ == "__main__":
	main()