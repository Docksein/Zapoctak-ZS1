import re
import sys
"""
if len(sys.argv) < 2:
	print("Enter the name of the file")
	sys.exit(1)	

with open(sys.argv[1], 'r', encoding='utf8') as f:
	txt = f.read()
"""
class Converter():

	def convert(self, source):
		return self.regex.sub(self.replace, source)

	def replace(self, match):
		pass

class HeadingConverter(Converter):
	regex = re.compile(r"^\s*(#{1,6})(.*?)$", flags=re.MULTILINE)

	def replace(self, match):
		level = len(match.group(1))
		
		return f"<h{level}>{match.group(2)}</h{level}>"

class Escapers(Converter):
	regex = re.compile(r"\\\*|\\\`")

	def replace(self,match):
		pass

class CodeConverter(Converter):
	regex = re.compile(r"`(.*?)`", flags=re.MULTILINE)

	def replace(self,match):
		return f"<code>{match.group(1)}</code>"

class InlineConverter(Converter):
	
	def replace(self, match):
		return f"<{self.tag}>{match.group(1)}</{self.tag}>"

class BoldConverter(InlineConverter):
	regex = re.compile(r"\*\*(.*?)\*\*")
	tag  = "strong"

class ItalicConverter(InlineConverter):
	regex = re.compile(r"\*(.*?)\*")
	tag  = "em"

txt = "**gejming**"
print(BoldConverter().convert(txt))