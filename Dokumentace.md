Program na konvertování markdownu do html
===
Program, který pomocí regulárních výrazů konvertuje markdown elementy do html

Program potřebuje:
- python 3.x
- knihovny sys, re

Program spustíte pomocí následujícího příkazu na příkazové řádce:
`python3 main.py (daný markdown soubor)`
A vytvoří vám konverovaný soubor se stejným názevem a příponou ".html"

Uživatelská dokumentace
---
Program podporuje základní markdown syntaxi, která se řídí podle [Markdown příručkové stránky](https://www.markdownguide.org/)

### Nadpisy
Podobně jako v html, program podporuje 6 úrovní nadpisů. Pro vytvoření nadpisu, začněte řádek jedním až šesti `\#`. Celý řádek se počítá jako nadpis.
| Markdown | Html | 
|----------|------|
| \# Nadpis úrovně 1 | \<h1\> Nadpis úrovně 1 \</h1\> |
| \#\# Nadpis úrovně 2 | \<h2\> Nadpis úrovně 2 \</h2\> |
| \#\#\#\#\#\# Nadpis úrovně 6 | \<h6\> Nadpis úrovně 6 \</h6\> |

### Paragrafy
Paragraf začíná a končí prázdným řádkem. Pokud chcete vytvořit paragraf, je potřeba prázdný řádek vytvořit jak před paragrafem, tak i za ním. Paragraf může mít více řádků.
| Markdown | Html | 
|----------|------|
| jeden paragraf<br><br>druhý paragraf<br> |\<p\>jeden paragraf\</p\><br><br> \<p\>druhý paragraf\</p\>|

### Únikové znaky
Pro vložení speciálních markdown znaků do textu, je nutné před nimi použít zpětné lomítko `\`.
Jsou to znaky:
- \* - hvězda
- \` - zpětné uvozovky

### Blockquote
Pro citování sekce textu, použijte `>` na začátku řádku. Pokud chcete, aby citace měla více řádků, tak každý další řádek začněte dalším `>`, dokud má citace pokračovat. 
Blockquote také podporuje markdown syntaxi uvnitř daných bloků.
| Markdown | Html | 
|----------|------|
| \>citace<br>\>přes několik řádků. | \<blockquote\><br> citace<br>přes několik řádků.<br> \</blockquote\> |
### Seznamy
Program podporuje seznamy jak neočíslované pomocí pomlčky `-`, tak i očíslované. Očíslované seznamy mohou mít libovolné čísla, ovšem zobrazí se běžně od jedné.

| Markdown | Html | 
|----------|------|
| \-neočíslovaný <br>\-seznam | \<ul\><br> \<li\>neočíslovaný\</li\><br>\<li\>seznam\</li\><br>\<ul\>|
| 1.očíslovaný <br>2.seznam | \<ol\><br> \<li\>očíslovaný\</li\><br>\<li\>seznam\</li\><br>\<ol\>|

### Kód
Pro označení části textu jako kódu, lze text ohraničit zpětnými uvozovkami `` ` ``. Všechny speciální markdown znaky jsou automaticky konvertovány na html kódové znaky a nemusí se používat zpětné lomítko.
| Markdown | Html | 
|----------|------|
| \` zde je kód \` | \<code\> zde je kód \</code\>|

### Odkazy
Pro přidání odkazu do textu, napište název odkazu do hranatých úvozovek název odkazu `[Jméno]`a hned za to napište odkaz do kulatých uvozovek odkaz `(www.odkaz.cz>).`
| Markdown | Html | 
|----------|------|
| \[Název\]\(www<span>.odkaz&period;cz</span>\) | \<a href="www<span>.odkaz&period;cz</span>"\>Název\</a\> |

### Obrázky
Pro přidání obrázku do textu, napiště vykřičník `!` následovaný hranatými uvozovkami s alt textem `[alt text]` a hned za ním kulaté závorky s cestou k obrázku a nepovinně i název obrázku v dvojitých uvozovkách `(cesta "Název")`.
| Markdown | Html | 
|----------|------|
| !\[alt text\]\(obrázek.jpg "Text k obrázku"\) | \<img src="obrázek.jpg" alt="alt text" title="Text k obrázku"\> |

### Horizontální čára
Pro přidání horizontální čáry, napiště do textu tři pomlčky nebo tři hvězdy za sebou: `---` nebo `***`
| Markdown | Html | 
|----------|------|
| \-\-\- | \<hr\> |
| \*\*\* | \<hr\> | 

### Kurzíva
Pro označení části textu kurzívou, ohraničte daný text jednou hvězdou `*kurzivní text*`
| Markdown | Html | 
|----------|------|
| \*Kurzivní text\*  | \<em\>Kurzivní text\</em\>  |

### Tučné písmo
Pro označení části textu, ohraničte daný text dvěmi hvězdami `**tučný text**`
| Markdown | Html | 
|----------|------|
| \*\*tučný text\*\*  | \<b\>tučný text\</b\>  |

Programátorská dokumentace
---
Program používá regulární výrazy, aby našel v textu určité syntaktické znaky popisované výše, které postupně převede.
Samotné znaky nahradí příslušnými html ekvivalenty a zbytek textu zachová.  
Pro regulární výrazy je použita knihovna re, která je do pythonu přímo zabudovaná. 

Program se dělí na třídy, která každá konvertuje jeden syntaktický element. 
Každá třída dědí z abstraktní třídy `Converter()`, která definuje metodu `convert()`, která jako argument bere daný text, který chceme konvertovat.  
Všechny konkrétní třídy musí nadefinovat proměnnou `regex`, do které se přiřadí funkce `re.compile()`, kde určíme vzorec, který bychom měli v textu najít.  
Funkce `replace()` pak vrací string, kterým chceme nahradit