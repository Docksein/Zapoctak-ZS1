import re
import sys

if len(sys.argv) < 2:
	print("Chybí argument markdown souboru")
	sys.exit(1)	
elif sys.argv[1][-3:] != ".md":
	print("Argument není markdown soubor")
	sys.exit9(1)
else:
	html_soubor = open(f"{sys.argv[1][:-3]}.html", "w", encoding='utf8')

with open(sys.argv[1], 'r', encoding='utf8') as f:
	txt = f.read()

class Converter():
	"""
	Abstraktní třída, kterou dědí všechny další třídy.
	"""
	def convert(self, source):
		"""
		Konvertuje element dané třídy z markdownu do html
		"""
		return self.regex.sub(self.replace, source)

	def replace(self, match):
		pass

# Třída na konvertování elementů markdownu do html bez změny konverterem 
class SyntaxElements(Converter):
	"""
	Převede elementy markdownu na html kódy, které zobrazují daný znak
	"""
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
	"""
	převádí zalomené znaky na html symboly
	"""
	regex = re.compile(r"(\\\*)|(\\\`)|(\\\-)|(\\\>)")

	def replace(self, match):
		if match.group(0) == "\*":
			return f"&#42;"
		elif match.group(0) == "\-":
			return f"&#45;"
		elif  match.group(0) == "\>":
			return f"&#62;"
		else:
			return f"&#96;"
#Třída na konvertování nadpisů
class HeadingConverter(Converter):
	"""
	Konvertuje markdown nadpisy #(1-6krát) na html <h(1-6)>
	"""
	regex = re.compile(r"^\s*(#{1,6})(.*?)$", flags=re.MULTILINE)

	def replace(self, match):
		level = len(match.group(1))
		
		return f"<h{level}>{match.group(2)}</h{level}>"

#Třída na konvertování paragrafů
class ParagraphConverter(Converter):
	"""
	Konvertuje markdown paragrafy ohraničené prázdnými řádky na html <p>
	"""
	regex = re.compile(r"^\s*\n(^[^<])(.*?)(^\s*$|^<)", flags=re.MULTILINE | re.DOTALL)
	
	def replace(self, match):
		return f"<p>\n{match.group(1)}{match.group(2)}</p>\n{match.group(3)}"

# Třída na konvertování horizontálních čar
class HorizontalRuleConverter(Converter):
	"""
	Konvertuje markdown horizontální čáry --- na html <hr>
	"""
	regex = re.compile(r"\*\*\*|---")

	def replace(self, match):
		return f"<hr>"

# Třídy na konvertování odkazů, obrázků
class LinkConverter(Converter):
	"""
	Konvertuje markdown odkazy [title](https://www.example.com) na html <a href='https://www.example.com'>title</a>
	"""
	regex = re.compile(r"\[(.+?)\]\((.*?)\)", flags=re.MULTILINE)

	def replace(self, match):
		return f"<a href='{match.group(2)}'>{match.group(1)}</a>"

class ImageConverter(Converter):
	"""
	Konvertuje markdown obrázků ![alt text](image.jpg "title(nepovinně)") na html <img src="image.jpg" alt="alt text" title="title")>
	"""
	regex = re.compile(r"\!\[(.+?)\]\((.*?)\)")

	def replace(self, match):
		title = re.search(r'".*?"', match.group(2))
		match_group2 = re.sub(r'".*?"', "", match.group(2))
		if title:
			return f'<img src="{match.group(2)}" alt="{match.group(1)}" title = {title.group()}>'
		else:
			return f'<img src="{match_group2}" alt="{match.group(1)}">'

class NewLineConverter(Converter):
	"""
	Přidá na koncích řádků <br>.
	"""
	regex = re.compile(r"(.*?$)", flags=re.MULTILINE)

	def replace(self, match):
		return f"{match.object(0)}<br>"


#Třída na konvertování kódu
class CodeConverter(Converter):
	"""
	Konvertuje markdown kód uvozovaný zpětnými uvozovkami `kód` na html <code>kód</code>
	"""
	regex = re.compile(r"`(.*?)`", flags=re.DOTALL)

	def replace(self, match):
		text = SyntaxElements().convert(match.group(1))
		text = re.sub(r"\n", "<br>\n", text)
		return f"<code>{text}</code>"

# Třídy na konvertování bloků textu nebo seznamu
class BlockQuoteConverter(Converter):
	"""
	Konvertuje markdown blok citace, dokud začíná řádek znakem >, na html <blockquote>
	"""

	regex = re.compile(r"^>(.*?)(^[^>]|\Z)", flags=re.MULTILINE | re.DOTALL)

	def replace(self, match):
		match_group1 = re.sub(r'>', "", match.group(1))
		return f"<blockquote>\n{match_group1}</blockquote>\n{match.group(2)}"

class NestedListConverter(Converter):
	"""
	Konvertuje seznamy neočíslované - a očíslované 1. na <ul> a <ol>
	"""
	
	regex = re.compile(r"^(\t*)((\d+)\.|\s?-)\s*(.*)$", flags= re.MULTILINE)

	def convert(self, source):
		res = []
		levels = []

		for line in source.split("\n"):
			match = self.regex.match(line)
			if match:
				if match.group(3):
					tag = "ol"
				else:
					tag = "ul"

				this_level = len(match.group(1))+1

				if this_level > len(levels):
					levels.append(tag)
					res.append("<" + tag + ">")
				elif this_level < len(levels):
					for i in range(len(levels) - this_level):
						res.append("</"+levels.pop()+">")

				res.append("<li>" + match.group(4) + "</li>")
			else:
				for i in range(len(levels)):
					res.append("</"+levels.pop()+">")
				res.append(line)

		return "\n".join(res)


# Třídy na konvertování elementů uprostřed textu
class InlineConverter(Converter):
	
	def replace(self, match):
		return f"<{self.tag}>{match.group(1)}</{self.tag}>"

class BoldConverter(InlineConverter):
	"""
	Konvertuje tučně napsané písmo z **text** na <strong>text</strong>
	"""
	regex = re.compile(r"\*\*([^\*]+)\*\*")
	tag  = "b"

class ItalicConverter(InlineConverter):
	"""
	Konvertuje písmo napsané kurzívou z *text* na <em>text</em>
	"""
	regex = re.compile(r"\*([^\*]+)\*")
	tag  = "em"


converters = [
	Escapers(),	
	BlockQuoteConverter(),
	NestedListConverter(),
	ParagraphConverter(),
	CodeConverter(),
	LinkConverter(),
	ImageConverter(),
	HeadingConverter(),
	BoldConverter(),
	ItalicConverter(),
	BoldConverter(),
	HorizontalRuleConverter(),

]

for c in converters:
	txt = c.convert(txt)

html_soubor.write(txt)

f.close()
html_soubor.close()