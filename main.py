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

class SyntaxElements(Converter):
	regex = re.compile(r"(\*)|(\`)|(#)|(>)|(<)|(---)")

	def replace(self, match):
		if match.group(0) == "*":
			return f"&#42;"
		elif match.group(0) == "`":
			return f"&#96;"
		elif match.group(0) == "#":
			return f"&#35;"
		elif match.group(0) == "<":
			return f"&lt;"
		elif match.group(0) == ">":
			return f"&gt;"
		else:
			return f"&#45;&#45;&#45;"

class Escapers(Converter):
	regex = re.compile(r"(\\\*)|(\\\`)")

	def replace(self, match):
		if match.group(0) == "\*":
			return f"&#42;"
		else:
			return f"&#96;"

class HorizontalRuleConverter(Converter):
	regex = re.compile(r"\*\*\*|---")

	def replace(self, match):
		return f"<hr>"

class LinkConverter(Converter):
	regex = re.compile(r"\[(.+?)\]\((.*?)\)", flags=re.MULTILINE)

	def replace(self, match):
		return f"<a href='{match.group(2)}'>{match.group(1)}</a>"

class ImageConverter(Converter):
	regex = re.compile(r"\!\[(.+?)\]\((.*?)\)")

	def replace(self, match):
		title = re.search(r'".*?"', match.group(2))
		match_group2 = re.sub(r'".*?"', "", match.group(2))
		if title:
			return f'<img src="{match.group(2)}" alt="{match.group(1)}" title = {title.group()}>'
		else:
			return f'<img src="{match_group2}" alt="{match.group(1)}">'

class CodeConverter(Converter):
	regex = re.compile(r"`(.*?)`", flags=re.DOTALL)

	def replace(self, match):
		text = SyntaxElements().convert(match.group(1))
		return f"<code>{text}</code>"

class BlockQuoteConverter(Converter):
	regex = re.compile(r"^>(.*)", flags=re.DOTALL)

	def replace(self, match):
		return f"<blockquote>{match.group(1)}</blockquote>"

class InlineConverter(Converter):
	
	def replace(self, match):
		return f"<{self.tag}>{match.group(1)}</{self.tag}>"

class BoldConverter(InlineConverter):
	regex = re.compile(r"\*\*(.*?)\*\*")
	tag  = "strong"

class ItalicConverter(InlineConverter):
	regex = re.compile(r"\*(.*?)\*")
	tag  = "em"

txt = '''
<h1>piss</h1>

`
<h1>piss</h1>
`
'''
print(CodeConverter().convert(txt))