"""
TinyObj v0.1.0,
a tiny object format for freedom.
"""
from typing import Optional, Dict, Any, List
from tobj.interpreter import Interpreter
from tobj.parser import Parser
from tobj.lexer import Lexer

def load(string_code: Optional[str] = None, 
		  string_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
	"""Parse TinyObj from string or file path"""
	if string_code is None and string_path is None:
		return None
	if string_code and string_path:
		raise Exception("'load()' can take either string_code or string_path; not both.")
	
	if string_code:
		return Interpreter(Parser(Lexer(string_code).tokenize()).parse()).interpret()
	
	if string_path:
		with open(string_path, 'r') as f:
			content = "".join(f.readlines())
			return Interpreter(Parser(Lexer(content).tokenize()).parse()).interpret()
	
	return None

def objectify(data: Dict[str, Any]) -> str:
	"""
	Converts a Python dictionary into a TinyObj string format using a single
	recursive function.
	"""
	output: List[str] = []

	def format_value(value: Any) -> str:
		"""Converts a Python value into its TinyObj string representation."""
		import json
		if isinstance(value, str):
			# Use json.dumps for safe string escaping (e.g., handles quotes)
			return json.dumps(value)
		elif isinstance(value, bool):
			return str(value).lower()
		elif value is None:
			return "nothing"
		elif isinstance(value, (int, float)):
			return str(value)
		return str(value)

	def serialize_recursive(current_dict: Dict, path_prefix: str) -> None:
		"""
		The main recursive worker function.
		"""
		for key, value in current_dict.items():
			current_path = f"{path_prefix}.{key}" if path_prefix else key

			if isinstance(value, dict) and value:
				# --- 1. Object Declaration (Nested Dictionary) ---
				output.append(f"\n*{current_path}")
				
				# Recurse into the sub-object, using the full path
				serialize_recursive(value, current_path)

			elif isinstance(value, list):
				# --- 2. List Property ---
				# Write the key on its own line
				output.append(f"> {key}")
				
				# Write each list item with the '-' prefix
				for item in value:
					formatted_item = format_value(item)
					output.append(f"- {formatted_item}")

			elif not isinstance(value, dict):
				# --- 3. Simple Property ---
				# Write as a single line property assignment
				formatted_value = format_value(value)
				output.append(f"> {key} {formatted_value}")
				

	serialize_recursive(data, path_prefix="")
	
	# Return the final string, joining lines and ensuring a trailing newline
	return "\n".join(output) + "\n"

def write(data: Dict[str, Any], file_path: str) -> None:
	tobj_result = objectify(data)
	with open(file_path, 'w') as file:
		file.write(tobj_result)

def test_case(name: str, code: str) -> None:
	"""Run a single test case with error handling"""
	print(f"\n{'='*60}")
	print(f"TEST: {name}")
	print(f"{'='*60}")
	print("INPUT:")
	print(code)
	print("\n" + "-"*60)
	
	try:
		result = load(string_code=code)
		print("RESULT:")
		import json
		print(json.dumps(result, indent=2))
		print("✅ PASSED")
	except Exception as e:
		print(f"❌ ERROR: {type(e).__name__}: {e}")

def test_case_file(name: str, code: str) -> None:
	"""Run a single test case with error handling from a file"""
	print(f"\n{'='*60}")
	print(f"TEST: {name}")
	print(f"{'='*60}")
	print("INPUT:")
	print(code)
	print("\n" + "-"*60)
	
	try:
		result = load(string_path=code)
		print("RESULT:")
		import json
		print(json.dumps(result, indent=2))
		print("✅ PASSED")
	except Exception as e:
		print(f"❌ ERROR: {type(e).__name__}: {e}")

def main():
	"""Run all edge case tests"""
	
	# Test 1: Property before object
	test_case("Property before any object", """
>name Alice
""")
	
	# Test 2: Empty object
	test_case("Empty object", """
*User
*Config
>version 1
""")
	
	# Test 3: Multiple top-level objects
	test_case("Multiple top-level objects", """
*User
>name Alice

*Device
>model "Phone"
""")
	
	# Test 4: Empty list
	test_case("Empty list (property with no value)", """
*User
>items
""")
	
	# Test 5: Nested object without parent
	test_case("Nested object without explicit parent", """
*User.profile.settings
>theme dark
""")
	
	# Test 6: Basic working example
	test_case("Basic working example", """
*User
>name Alice
>age 30
>tags
- python
- rust
""")
	
	# Test 7: One-liner list
	test_case("One-liner list", """
*Config
>values - a - b - c
""")
	
	# Test 8: Mixed types
	test_case("Mixed types", """
*Data
>string "hello"
>number 42
>float 3.14
>bool true
>"nothing" nothing
""")

	test_case('Mixed lists + one-liner' , "*Temps >readings - -5 - 10 - -3.14")

	test_case_file("Reading from file and dollar signs", "samples/names.tobj")

if __name__ == "__main__":
	main()