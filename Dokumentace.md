Program na konvertování markdownu do html
===
Program, který pomocí regulárních výrazů konvertuje markdown elementy do html

Program potřebuje:
- python 3.x
- knihovny sys, re

Program spustíte pomocí následujícího příkazu na příkazové řádce:
`python3 main.py (daný markdown soubor)`

Uživatelská dokumentace
---
Program podporuje základní markdown syntaxi, která se řídí podle [Markdown příručkové stránky](https://www.markdownguide.org/)

### Nadpisy
Podobně jako v html, program podporuje 6 úrovní nadpisů. Pro vytvoření nadpisu, začněte řádek jedním až šesti \#. Celý řádek se počítá jako nadpis.
| Markdown | Html | 
|----------|------|
| \# Nadpis úrovně 1 | \<h1\> Nadpis úrovně 1 \</h1\> |
| \#\# Nadpis úrovně 2 | \<h2\> Nadpis úrovně 2 \</h2\> |
| \#\#\#\#\#\# Nadpis úrovně 6 | \<h6\> Nadpis úrovně 6 \</h6\> |

### Paragrafy
Paragraf začíná a končí prázdným řádkem. Pokud chcete vytvořit paragraf, je potřeba prázdný řádek vytvořit jak před paragrafem, tak i za ním. Paragraf může mít více řádků.
| Markdown | Html | 
|----------|------|
| <br>jeden paragraf<br><br>druhý paragraf<br> |<br> \<p\>jeden paragraf\</p\><br><br> \<p\>druhý paragraf\</p\>|

### Blockquote
Pro citování sekce textu, použijte `\>` na začátku řádku. Pokud chcete, aby citace měla více řádků, tak každý další řádek začněte dalším `\>`, dokud má citace pokračovat.
| Markdown | Html | 
|----------|------|
| \>citace<br>\>přes několik řádků. | \<blockquote\><br> citace<br>přes několik řádků.<br> \</blockquote\> |
### Seznamy

### Kód
 

### Odkazy

### Obrázky

### Horizontální čára

### Kurzíva

### Tučné písmo
