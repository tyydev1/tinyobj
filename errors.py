"""
TinyObj's Custom Errors
"""

from typing import Optional

class Position:
	"""Tracks position in source code"""
	def __init__(self, idx: int, 
			  ln: int, col: int, 
			  filename: str, 
			  text: str) -> None:
		self.idx: int = idx
		self.ln: int = ln
		self.col: int = col
		self.filename: str = filename
		self.text: str = text
		
	def advance(self, current_char: Optional[str] = None) -> 'Position': 
		"""Move position forward one character"""
		self.idx += 1
		self.col += 1

		if current_char == '\n':
			self.ln += 1
			self.col = 0

		return self

	def copy(self) -> 'Position':
		copy_position = Position(self.idx, self.ln, self.col, self.filename, self.text)
		return copy_position
	
###########################################

# ERRORS

###########################################