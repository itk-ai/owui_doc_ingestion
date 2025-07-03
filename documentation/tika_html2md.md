# Tika xHTML output to markdown

It is [hardcoded into OWUI](
https://github.com/open-webui/open-webui/blob/b5f4c85bb196c16a775802907aedd87366f58b0f/backend/open_webui/retrieval/loaders/main.py#L114C1-L114C32
) to use *Tika*s text output.

Using instead the general endpoint `<tika server>/tika`, that delivers xHTML 
formatted output, it is possible to get a markdown formatted output.
It is assumed that markdown is a favourable format due to its simple markup, that
retains the most essential structure in a text, which _might help_ a 
_well-trained_ LLM understand how different parts of consecutive text are related
and its relative importance. 

To what extend markdown is actually better than the relative clean HTML delivered
by the `/tika` endpoint have not been tested - as have not the general assumption
that markdown is to be preferred to plain text (for a given LLM)

## HTML to md

Three alternatives have been compared in translating html to markdown:

- [pandoc](https://github.com/JessicaTegner/pypandoc): `pypandoc.convert_text(html_string, 'markdown', format='html')`
- [markdownify](https://github.com/matthewwithanm/python-markdownify): `markdownify.markdownify(html_string)`
- [html2text](https://github.com/Alir3z4/html2text): `html2text.html2text(html_string)`

They have been compared on the output from Tika's HTML output from the `/tika` 
endpoint from a [relatively well formatted pdf](
https://www.retsinformation.dk/api/pdf/233638
) and a realistic word documents with tables. 
The only preprocessing have been to remove 
the html-document header information. This was done using 
`re.sub(r'<head>.*?</head>', '', html_string, flags=re.DOTALL)`.

## Conclusion/preference

html2text is the suggested tool. The output of html2text looks slightly better 
and more standard compared to markdownify. Furthermore html2text have fewer 
dependencies than markdownify. 

Pandocs table output is visually superior (from plain text perspective), but is
expected to be hard for LLMs to comprehend. Trying to remove the multiline 
features from pandoc markdown all the table conversion seems to fallback to html
tables, so I didn't succeed in adjusting the
behaviour, although it should be easy to add/remove extensions.
The `pypandoc` package also require a pandoc system installation, which was 
initially considered a big drawback, but it turned out that it was already a OWUI
project requirement (but I couldn't find any use of pandoc in the codebase, when 
I searched for it, so it might be a leftover after some code rewriting, and so it
might disappear at some point). 