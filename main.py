import re
import sys

if len(sys.argv) < 2:
	print("Enter the name of the file")
	sys.exit(1)	

with open(sys.argv[1], 'r', encoding='utf8') as f:
	txt = f.read()
	
class Converter():

	def convert(self, source):
		return self.regex.sub(self.replace, source)

	def replace(self, match):
		pass

class HeadingConverter(Converter):
	regex = re.compile(r"^\s*#({1,6})(.*?)$", flags=re.MULTILINE)

	def replace(self, match):
		level = len(match.group(1))
		
		return f"<h{level}>{match.group(1)}</h{len(level)>\n"

class BoldItalicConverter(Converter):


class InlineConverter(Converter):
	
	def replace(self, match):
		return f"<{self.tag}>{match.group(1)}<{self.tag}>\n"

class BoldConverter(Converter):
	regex = re.compile(r"\*\*(.*?)\*\*")
	tag  = "strong"
