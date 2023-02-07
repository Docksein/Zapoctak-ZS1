import re
import sys
"""
if len(sys.argv) < 2:
	print("Chybí argument markdown souboru")
	sys.exit(1)	

with open(sys.argv[1], 'r', encoding='utf8') as f:
	txt = f.read()
"""
class Converter():

	def convert(self, source):
		return self.regex.sub(self.replace, source)

	def replace(self, match):
		pass

# Třída na konvertování elementů markdownu do html bez změny konverterem 
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
# Třída na ignorování konvertování markdown elementů
class Escapers(Converter):
	regex = re.compile(r"(\\\*)|(\\\`)")

	def replace(self, match):
		if match.group(0) == "\*":
			return f"&#42;"
		else:
			return f"&#96;"
#Třída na konvertování nadpisů
class HeadingConverter(Converter):
	regex = re.compile(r"^\s*(#{1,6})(.*?)$", flags=re.MULTILINE)

	def replace(self, match):
		level = len(match.group(1))
		
		return f"<h{level}>{match.group(2)}</h{level}>"

# Třída na konvertování horizontálních čar
class HorizontalRuleConverter(Converter):
	regex = re.compile(r"\*\*\*|---")

	def replace(self, match):
		return f"<hr>"

# Třídy na konvertování odkazů, obrázků
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
#Třída na konvertování kódu
class CodeConverter(Converter):
	regex = re.compile(r"`(.*?)`", flags=re.DOTALL)

	def replace(self, match):
		text = SyntaxElements().convert(match.group(1))
		return f"<code>{text}</code>"

# Třídy na konvertování bloků textu nebo seznamu
class BlockQuoteConverter(Converter):
	regex = re.compile(r"^>(.*?)(^[^>]|\Z)", flags=re.MULTILINE | re.DOTALL)

	def replace(self, match):
		match_group1 = re.sub(r'>', "", match.group(1))
		return f"<blockquote>\n{match_group1}</blockquote>\n{match.group(2)}"


class ListItemsConverter(Converter):
	regex = re.compile(r"^\d*\.(.*?)$|-(\s*.*?)$", flags = re.MULTILINE)

	def replace(self, match):
		if match.group(1):
			return f"<li>{match.group(1)}</li>"
		else:
			return f"<li>{match.group(2)}</li>"

class OrderedListConverter(Converter):
	regex = re.compile(r"^(\d*\..*?)(^[^\d]|\Z)", flags=re.MULTILINE | re.DOTALL)

	def replace(self, match):
		match_group1 = ListItemsConverter().convert(match.group(1))
		return f"<ol>\n{match_group1}</ol>\n{match.group(2)}"

class UnorderedListConverter(Converter):
	regex = re.compile(r"^(-.*?)(^[^-]|\Z)", flags=re.MULTILINE | re.DOTALL)

	def replace(self, match):
		match_group1 = ListItemsConverter().convert(match.group(1))
		return f"<ul>\n{match_group1}</ul>\n{match.group(2)}"

# Třídy na konvertování elementů uprostřed textu
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


1. First item
2. Second item
3. Third item
> #### The quarterly results look great!
>

>
>  *Everything* is going according to `**plan**.`

- Revenue was off the chart.
- Profits were higher than ever.
1. First item
20 Second item
Third item


piss
'''
converters = [
	Escapers(),
	OrderedListConverter(),
	UnorderedListConverter(),
	BlockQuoteConverter(),
	CodeConverter(),
	LinkConverter(),
	ImageConverter(),
	HeadingConverter(),
	HorizontalRuleConverter(),
	BoldConverter(),
	ItalicConverter()

]

for c in converters:
	txt = c.convert(txt)

print(txt)