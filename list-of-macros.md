
# List of macros and environments

Please note that not everything has to be declared.

- Unknown macros are ignored with arguments kept, {} braces are removed.
- Unknwon environment frames \\begin, \\end are removed.
  If \\begin accepts arguments, the environment should be declared.
- Math mode macros only need to be declared, if they should not leave
  output that constitutes a part of a term or operator.

**Packages**

[LaTeX builtins](#latex-builtins),
[amsmath](#package-amsmath),
[amsthm](#package-amsthm),
[biblatex](#package-biblatex),
[glossaries](#package-glossaries),
[glossaries-extra](#package-glossaries-extra),
[graphicx](#package-graphicx),
[hyperref](#package-hyperref),
[listings](#package-listings),
[tikz](#package-tikz),
[xcolor](#package-xcolor)

**Document classes**

[article](#class-article),
[book](#class-book),
[report](#class-report),
[scrartcl](#class-scrartcl),
[scrbook](#class-scrbook),
[scrreprt](#class-scrreprt)


## LaTeX builtins

[yalafi/parameters.py](yalafi/parameters.py),
[tests/test\_packages/test\_latex\_builtins.py](tests/test_packages/test_latex_builtins.py)

**Macros**
(Major side-effects for the filter are noted in parantheses.)

\\AA,
\\aa,
\\AE,
\\ae,
\\caption (separates text),
\\chapter,
\\cite,
\\documentclass (activates module),
\\footnote (separates text),
\\footnotemark,
\\footnotetext (separates text),
\\framebox,
\\hfill,
\\hphantom,
\\hspace,
\\include,
\\input,
\\L,
\\l,
\\label,
\\LTadd,
\\LTalter,
\\LTinput (executes code in file),
\\LTskip,
\\newcommand (defines macro),
\\newline,
\\newtheorem (defines environment),
\\O,
\\o,
\\OE,
\\oe,
\\pageref,
\\par,
\\part,
\\phantom,
\\qquad,
\\quad,
\\ref,
\\renewcommand (defines macro),
\\S,
\\section,
\\ss,
\\subsection,
\\subsubsection,
\\textasciicircum,
\\textasciitilde,
\\textbackslash,
\\title,
\\usepackage (activates module),
\\vphantom,
\\vspace

**Environments**

displaymath,
enumerate,
eqnarray(\*),
equation,
figure,
itemize,
minipage,
table,
verbatim


## Package amsmath

[yalafi/packages/amsmath.py](yalafi/packages/amsmath.py),
[tests/test\_packages/test\_amsmath.py](tests/test_packages/test_amsmath.py)

**Macros**

\\DeclareMathOperator,
\\eqref,
\\medspace,
\\negmedspace,
\\negthickspace,
\\negthinspace,
\\notag,
\\numberwithin,
\\text,
\\thickspace,
\\thinspace

**Environments**

align(\*),
alignat(\*),
equation(\*),
flalign(\*),
gather(\*),
multiline(\*)


## Package amsthm

[yalafi/packages/amsthm.py](yalafi/packages/amsthm.py),
[tests/test\_packages/test\_amsthm.py](tests/test_packages/test_amsthm.py)

**Macros**

\\qedhere,
\\theoremstyle

**Environments**

proof


## Package biblatex

[yalafi/packages/biblatex.py](yalafi/packages/biblatex.py),
[tests/test\_packages/test\_biblatex.py](tests/test_packages/test_biblatex.py)

**Macros**

\\cite,
\\Cite,
\\footcite,
\\footcitetext,
\\parencite,
\\Parencite


## Package glossaries

[yalafi/packages/glossaries.py](yalafi/packages/glossaries.py),
[tests/test\_packages/test\_glossaries.py](tests/test_packages/test_glossaries.py)

Please note the comments at the beginning of file
[yalafi/packages/glossaries.py](yalafi/packages/glossaries.py).

**Macros**

\\longnewglossaryentry,
\\GLS,
\\Gls,
\\gls,
\\GLSpl,
\\Glspl,
\\glspl,
\\GLSdesc,
\\Glsdesc,
\\glsdesc,
\\glsdisp,
\\glslink,
\\GLStext,
\\Glstext,
\\glstext,
\\newacronym,
\\newglossaryentry


## Package glossaries-extra

[yalafi/packages/glossaries\_extra.py](yalafi/packages/glossaries_extra.py),
[tests/test\_packages/test\_glossaries\_extra.py](tests/test_packages/test_glossaries_extra.py)

Please note the comments at the beginning of file
[yalafi/packages/glossaries.py](yalafi/packages/glossaries.py).

**Macros**

\\newabbreviation


## Package graphicx

[yalafi/packages/graphicx.py](yalafi/packages/graphicx.py),
[tests/test\_packages/test\_graphicx.py](tests/test_packages/test_graphicx.py)

**Macros**

\\includegraphics


## Package hyperref

[yalafi/packages/hyperref.py](yalafi/packages/hyperref.py),
[tests/test\_packages/test\_hyperref.py](tests/test_packages/test_hyperref.py)

**Macros**

\\href,
\\texorpdfstring,
\\url


## Package listings

[yalafi/packages/listings.py](yalafi/packages/listings.py),
[tests/test\_packages/test\_listings.py](tests/test_packages/test_listings.py)

We simply remove the listings, inserting a paragraph break.

**Macros**

\\lstinputlisting,
\\lstset

**Environments**

lstlisting


## Package tikz

[yalafi/packages/tikz.py](yalafi/packages/tikz.py),
[tests/test\_packages/test\_tikz.py](tests/test_packages/test_tikz.py)

We simply remove the picture in environment 'tikzpicture'.

**Macros**

\\tikzset,
\\usetikzlibrary

**Environments**

tikzpicture


## Package xcolor

[yalafi/packages/xcolor.py](yalafi/packages/xcolor.py),
[tests/test\_packages/test\_xcolor.py](tests/test_packages/test_xcolor.py)

**Macros**

\\color,
\\colorbox,
\\definecolor,
\\fcolorbox,
\\textcolor


## Class article

[yalafi/documentclasses/article.py](yalafi/documentclasses/article.py),
[tests/test\_documentclasses/test\_article.py](tests/test_documentclasses/test_article.py)

&mdash;


## Class book

[yalafi/documentclasses/book.py](yalafi/documentclasses/book.py),
[tests/test\_documentclasses/test\_book.py](tests/test_documentclasses/test_book.py)

&mdash;


## Class report

[yalafi/documentclasses/report.py](yalafi/documentclasses/report.py),
[tests/test\_documentclasses/test\_report.py](tests/test_documentclasses/test_report.py)

&mdash;


## Class scrartcl

[yalafi/documentclasses/scrartcl.py](yalafi/documentclasses/scrartcl.py),
[tests/test\_documentclasses/test\_scrartcl.py](tests/test_documentclasses/test_scrartcl.py)

**Macros**

\\KOMAoption,
\\KOMAoptions


## Class scrbook

[yalafi/documentclasses/scrbook.py](yalafi/documentclasses/scrbook.py),
[tests/test\_documentclasses/test\_scrbook.py](tests/test_documentclasses/test_scrbook.py)

**Macros**

\\KOMAoption,
\\KOMAoptions


## Class scrreprt

[yalafi/documentclasses/scrreprt.py](yalafi/documentclasses/scrreprt.py),
[tests/test\_documentclasses/test\_scrreprt.py](tests/test_documentclasses/test_scrreprt.py)

**Macros**

\\KOMAoption,
\\KOMAoptions

