
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
[graphicx](#package-graphicx),
[hyperref](#package-hyperref),
[listings](#package-listings),
[xcolor](#package-xcolor)

**Document classes**

[article](#class-article),
[book](#class-book),
[report](#class-report),
[scrartcl](#class-scrartcl),
[scrbook](#class-scrbook),
[scrreprt](#class-scrreprt)


## LaTeX builtins

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
\\LTinput (excutes code in file),
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

**Macros**

\\DeclareMathOperator,
\\text,
\\eqref,
\\medspace,
\\negmedspace,
\\negthickspace,
\\negthinspace,
\\notag,
\\numberwithin,
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

**Macros**

\\qedhere,
\\theoremstyle

**Environments**

proof


## Package graphicx

**Macros**

\\includegraphics


## Package hyperref

**Macros**

\\texorpdfstring


## Package listings

We simply remove the listings, inserting a paragraph break.

**Macros**

\\lstinputlisting,
\\lstset

**Environments**

lstlisting


## Package xcolor

**Macros**

\\color,
\\colorbox,
\\definecolor,
\\fcolorbox,
\\textcolor


## Class article

&mdash;


## Class book

&mdash;


## Class report

&mdash;


## Class scrartcl

**Macros**

\\KOMAoption,
\\KOMAoptions


## Class scrbook

**Macros**

\\KOMAoption,
\\KOMAoptions


## Class scrreprt

**Macros**

\\KOMAoption,
\\KOMAoptions

