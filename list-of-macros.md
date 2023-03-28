
# List of macros and environments

Please note that not everything has to be declared.

- Unknown macros are ignored with arguments kept, {} braces are removed.
- Unknown environment frames \\begin, \\end are removed.
  If \\begin accepts arguments, the environment should be declared.
- Math mode macros only need to be declared, if they should not leave
  output that constitutes a part of a term or operator.

**Packages**

[LaTeX builtins](#latex-builtins),<br>
[amsmath](#package-amsmath),
[amsthm](#package-amsthm),
[babel](#package-babel),
[biblatex](#package-biblatex),
[circuitikz](#package-circuitikz),
[cleveref](#package-cleveref),
[geometry](#package-geometry),
[glossaries](#package-glossaries),
[glossaries-extra](#package-glossaries-extra),
[graphicx](#package-graphicx),
[hyperref](#package-hyperref),
[inputenc](#package-inputenc),
[koma-script](#package-koma-script),
[listings](#package-listings),
[mathtools](#package-mathtools),
[pgfplots](#package-pgfplots),
[tikz](#package-tikz),
[unicode-math](#package-unicode-math),
[xcolor](#package-xcolor),
[xspace](#package-xspace)

**Document classes**

[article](#class-article),
[book](#class-book),
[report](#class-report),
[scrartcl](#class-scrartcl),
[scrbook](#class-scrbook),
[scrreprt](#class-scrreprt)


## LaTeX builtins

Source: [yalafi/parameters.py](yalafi/parameters.py),
tests: [tests/test\_packages/test\_latex\_builtins.py](tests/test_packages/test_latex_builtins.py)

**Macros**
(Major side effects for the filter are noted in parentheses.)

\\AA,
\\aa,
\\AE,
\\addtocounter,
\\ae,
\\author,
\\bibitem,
\\bibliographystyle,
\\caption (separates text),
\\chapter,
\\cite,
\\def (defines macro),
\\documentclass (activates module),
\\footnote (separates text),
\\footnotemark,
\\footnotetext (separates text),
\\framebox,
\\hfill,
\\hphantom,
\\hspace,
\\include,
\\includeonly,
\\index,
\\input,
\\item,
\\L,
\\l,
\\label,
\\LaTeX,
\\linebreak,
\\LTadd,
\\LTalter,
\\LTinput (executes code in file),
\\LTskip,
\\MakeLowercase,
\\MakeUppercase,
\\newcommand (defines macro),
\\newcounter,
\\newline,
\\newtheorem (defines environment),
\\nobreakspace
\\O,
\\o,
\\OE,
\\oe,
\\pagenumbering,
\\pageref,
\\pagestyle,
\\par,
\\paragraph,
\\part,
\\phantom,
\\providecommand (defines macro, but does not overwrite existing ones),
\\qquad,
\\quad,
\\ref,
\\refstepcounter,
\\renewcommand (defines macro),
\\S,
\\section,
\\setcounter,
\\ss,
\\stepcounter,
\\subsection,
\\subsubsection,
\\TeX,
\\textasciicircum,
\\textasciitilde,
\\textbackslash,
\\thispagestyle,
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
tabular,
thebibliography,
verbatim


## Package amsmath

Source: [yalafi/packages/amsmath.py](yalafi/packages/amsmath.py),
tests: [tests/test\_packages/test\_amsmath.py](tests/test_packages/test_amsmath.py)

**Macros**

\\DeclareMathOperator,
\\eqref,
\\medspace,
\\negmedspace,
\\negthickspace,
\\negthinspace,
\\notag,
\\numberwithin,
\\substack,
\\text,
\\thickspace,
\\thinspace

**Environments**

align(\*),
alignat(\*),
aligned,
equation(\*),
flalign(\*),
gather(\*),
multline(\*),
multlined


## Package amsthm

Source: [yalafi/packages/amsthm.py](yalafi/packages/amsthm.py),
tests: [tests/test\_packages/test\_amsthm.py](tests/test_packages/test_amsthm.py)

**Macros**

\\newtheoremstyle,
\\qedhere,
\\theoremstyle

**Environments**

proof


## Package babel

Source: [yalafi/packages/babel.py](yalafi/packages/babel.py),
tests: [tests/test\_packages/test\_babel.py](tests/test_packages/test_babel.py)

**Macros**

\\foreignlanguage,
\\selectlanguage

**Environments**

otherlanguage\(\*\)


## Package biblatex

Source: [yalafi/packages/biblatex.py](yalafi/packages/biblatex.py),
tests: [tests/test\_packages/test\_biblatex.py](tests/test_packages/test_biblatex.py)

**Macros**

\\addbibresource,
\\cite,
\\Cite,
\\footcite,
\\footcitetext,
\\parencite,
\\Parencite,
\\printbibliography


## Package circuitikz

Source: [yalafi/packages/circuitikz.py](yalafi/packages/circuitikz.py),
tests: [tests/test\_packages/test\_circuitikz.py](tests/test_packages/test_circuitikz.py)

We simply remove the circuit in environment 'circuitikz'.

**Loaded packages**

[tikz](#package-tikz)

**Macros**

\\ctikzset

**Environments**

circuitikz


## Package cleveref

Source: [yalafi/packages/cleveref.py](yalafi/packages/cleveref.py),
tests: [tests/test\_packages/test\_cleveref.py](tests/test_packages/test_cleveref.py)

The LaTeX package `cleveref` allows to automatically insert the type of a
reference, e.g. expand `\cref{sec:one}` to `section 1` if it indeed references
the first section.
The `cleveref` output is also highly customizable, and we do not intend to
replicate its functionality within YaLafi.
Luckily, `cleveref` has a `poorman` option with the following intention:
If you have written a document using `cleveref`, but a publisher does not
accept `cleveref`, you can use that option to create a `sed` file (during the
LaTeX run) which allows replacing all `cleveref` commands.
See the `cleveref` documentation for more details.
YaLafi makes use of that and reads this `sed` file to replace all `cleveref`
commands with their correct replacement.
As explained above, this requires that you load `cleveref` with the `poorman`
option, run LaTeX before YaLafi and passing the `sed` file to YaLafi via
`\YYCleverefInput`.
A sample file could look like
```latex
% file `main.tex`
\documentclass{scrartcl}
\newcommand{\YYCleverefInput}[1]{} % make the command known to LaTeX
\usepackage[poorman]{cleveref}
% See below for an example with hyperref!
\YYCleverefInput{main.sed} % tell YaLafi which sed file to use

\begin{document}

    \section{One}\label{sec:one}
    \Cref{sec:one}

\end{document}
```
As written above, you need to first run LaTeX to produce the file `main.sed`
and then use YaLafi.

The `sed` file is loaded to YaLafi via `\YYCleverefInput`.
The usage is similar to `\LTinput` and you should also define
`\newcommand{\YYCleverefInput}[1]{}` in your document.

**Known limitation (1):**
Unfortunately, the `cleveref` package does not always
create the `sed` file as expected.
Whenever you load the `hyperref` package as well, only the starred commands,
e.g. `\cref*{equation1}`, are written to the `sed` file.
This should be fixed within the `cleveref` LaTeX package.

**Workaround (1):**
Don’t use the starred variants and compile your document without loading
`hyperref` to create the `sed` script.
Only add the `hyperref` package if you don’t need the created `sed` file.
Unfortunately, `cleveref` will overwrite the `sed` file each time it is called
together with `hyperref` and the `poorman` option.
Hence, one need to remove the `poorman` option in this case.

To simplify the process of loading `cleveref` in a document where you also use
`hyperref`, one can use the following LaTeX code.
The idea is that one can comment or uncomment loading the `hyperref` package.
If the `hyperref` package is not loaded, `cleveref` is loaded with the
`poorman` option and produces a valid `sed` file on the next LaTeX run.
And if you load the `hyperref` package, `cleveref` is loaded without the
`poorman` option such that subsequent LaTeX calls don’t change the `sed` file.
All this is hidden from YaLafi within an `%%% LT-SKIP` block to avoid warnings.
Instead, the usage of `cleveref` with the `poorman` option is passed to YaLafi.

```latex
% file `main.tex`
\documentclass{scrartcl}
\newcommand{\YYCleverefInput}[1]{} % make the command known to LaTeX
\newcommand{\LTadd}[1]{} % make the command known to LaTeX

%%% LT-SKIP-BEGIN
% \usepackage{hyperref}
\makeatletter
\@ifpackageloaded{hyperref}{
    \usepackage{cleveref}
}{
    \usepackage[poorman]{cleveref}
}
\makeatother
%%% LT-SKIP-END

\LTadd{\usepackage[poorman]{cleveref}} % tell YaLafi to use cleveref
\YYCleverefInput{main.sed} % tell YaLafi which sed file to use

\begin{document}

    \section{One}\label{sec:one}
    \Cref{sec:one}

\end{document}
```

You only need to disable loading `hyperref`, whenever you use a new label (or
a different combination of labels).
But YaLafi will tell you, if it does not know a label yet.
After enabling `hyperref` again, you might need to run LaTeX twice to update
the auxiliary files.

**Known limitation (2):**
In multi-language documents, YaLafi uses the main language for all references.

**Macros**

\\cpageref,
\\Cpageref,
\\cpagerefrange,
\\Cpagerefrange,
\\cref(\*),
\\Cref(\*),
\\crefalias,
\\crefname,
\\Crefname,
\\crefrange(\*),
\\Crefrange(\*),
\\label,
\\labelcpageref,
\\labelcref,
\\lcnamecref,
\\lcnamecrefs,
\\namecref,
\\nameCref,
\\namecrefs,
\\nameCrefs,
\\YYCleverefInput,
all commands that would be replaced with the `sed` file
(e.g. \\crefrangeconjunction)


## Package geometry

Source: [yalafi/packages/geometry.py](yalafi/packages/geometry.py),
tests: [tests/test\_packages/test\_geometry.py](tests/test_packages/test_geometry.py)

**Macros**

\\geometry


## Package glossaries

Source: [yalafi/packages/glossaries.py](yalafi/packages/glossaries.py),
tests: [tests/test\_packages/test\_glossaries.py](tests/test_packages/test_glossaries.py)

Please note the comments at the beginning of file
[yalafi/packages/glossaries.py](yalafi/packages/glossaries.py).
You have to load the `.glsdefs` file into each LaTeX source and to place
all definitions of glossary entries inside
`\begin{document} ... \end{document}`.

**Macros**

\\acrpluralsuffix
\\GLS,
\\Gls,
\\gls,
\\glspluralsuffix
\\glsacrpluralsuffix
\\glsupacrpluralsuffix
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
\\longnewglossaryentry,
\\newacronym,
\\newglossaryentry


## Package glossaries-extra

Source: [yalafi/packages/glossaries\_extra.py](yalafi/packages/glossaries_extra.py),
tests: [tests/test\_packages/test\_glossaries\_extra.py](tests/test_packages/test_glossaries_extra.py)

Please note the comments at the beginning of file
[yalafi/packages/glossaries\_extra.py](yalafi/packages/glossaries_extra.py).
You have to load the `.glsdefs` file into each LaTeX source and to say
something like `\usepackage[docdef=true]{glossaries-extra}`
or `\usepackage[docdef=atom]{glossaries-extra}` in the preamble.
With `docdef=true`, all glossary entries have to be defined inside
`\begin{document} ... \end{document}`.

**Loaded packages**

[glossaries](#package-glossaries)

**Macros**

\\newabbreviation,
\\Glsxtrfull,
\\glsxtrfull,
\\Glsxtrlong,
\\glsxtrlong,
\\Glsxtrshort,
\\glsxtrshort


## Package graphicx

Source: [yalafi/packages/graphicx.py](yalafi/packages/graphicx.py),
tests: [tests/test\_packages/test\_graphicx.py](tests/test_packages/test_graphicx.py)

**Macros**

\\graphicspath
\\includegraphics


## Package hyperref

Source: [yalafi/packages/hyperref.py](yalafi/packages/hyperref.py),
tests: [tests/test\_packages/test\_hyperref.py](tests/test_packages/test_hyperref.py)

**Macros**

\\href,
\\ref\*,
\\texorpdfstring,
\\url


## Package inputenc

Source: [yalafi/packages/inputenc.py](yalafi/packages/inputenc.py),
tests: [tests/test\_packages/test\_inputenc.py](tests/test_packages/test_inputenc.py)

**Macros**

\\inputencoding


## Package koma-script

Source: [yalafi/packages/koma\_script.py](yalafi/packages/koma_script.py),
tests: [tests/test\_packages/test\_koma\_script.py](tests/test_packages/test_koma_script.py)

This is a helper package only available in YaLafi to implement commands used
by the KOMA classes
[scrartcl](#class-scrartcl),
[scrbook](#class-scrbook) and
[scrreprt](#class-scrreprt).

**Macros**

\\extratitle,
\\KOMAoption,
\\KOMAoptions,
\\subject,
\\subtitle


## Package listings

Source: [yalafi/packages/listings.py](yalafi/packages/listings.py),
tests: [tests/test\_packages/test\_listings.py](tests/test_packages/test_listings.py)

We simply remove the listings, inserting a paragraph break.

**Macros**

\\lstinputlisting,
\\lstset

**Environments**

lstlisting


## Package mathtools

Source: [yalafi/packages/mathtools.py](yalafi/packages/mathtools.py),
tests: [tests/test\_packages/test\_mathtools.py](tests/test_packages/test_mathtools.py)

**Loaded packages**

[amsmath](#package-amsmath)

**Macros**

\\mathtoolsset


## Package pgfplots

Source: [yalafi/packages/pgfplots.py](yalafi/packages/pgfplots.py),
tests: [tests/test\_packages/test\_pgfplots.py](tests/test_packages/test_pgfplots.py)

**Loaded packages**

[graphicx](#package-graphicx),
[tikz](#package-tikz)

**Macros**

\\pgfplotsset


## Package subfiles

Source: [yalafi/packages/subfiles.py](yalafi/packages/subfiles.py),
tests: [tests/test\_packages/test\_subfiles.py](tests/test_packages/test_subfiles.py)

**Macros**

\\subfile,
\\subfileinclude


## Package tikz

Source: [yalafi/packages/tikz.py](yalafi/packages/tikz.py),
tests: [tests/test\_packages/test\_tikz.py](tests/test_packages/test_tikz.py)

We simply remove the picture in environment 'tikzpicture'.

**Macros**

\\tikzset,
\\usetikzlibrary

**Environments**

tikzpicture


## Package unicode-math

Source: [yalafi/packages/unicode\_math.py](yalafi/packages/unicode_math.py),
tests: [tests/test\_packages/test\_unicode\_math.py](tests/test_packages/test_unicode_math.py)

Adds unicode ‘math operators’, i.e. also `≤` and similar are recognized in equations.

**Macros**

\\setmathfont,
\\unimathsetup


## Package xcolor

Source: [yalafi/packages/xcolor.py](yalafi/packages/xcolor.py),
tests: [tests/test\_packages/test\_xcolor.py](tests/test_packages/test_xcolor.py)

**Macros**

\\color,
\\colorbox,
\\definecolor,
\\fcolorbox,
\\textcolor


## Package xspace

Source: [yalafi/packages/xspace.py](yalafi/packages/xspace.py),
tests: [tests/test\_packages/test\_xspace.py](tests/test_packages/test_xspace.py)

**Macros**

\\xspace


## Class article

Source: [yalafi/documentclasses/article.py](yalafi/documentclasses/article.py),
tests: [tests/test\_documentclasses/test\_article.py](tests/test_documentclasses/test_article.py)

&mdash;


## Class book

Source: [yalafi/documentclasses/book.py](yalafi/documentclasses/book.py),
tests: [tests/test\_documentclasses/test\_book.py](tests/test_documentclasses/test_book.py)

&mdash;


## Class report

Source: [yalafi/documentclasses/report.py](yalafi/documentclasses/report.py),
tests: [tests/test\_documentclasses/test\_report.py](tests/test_documentclasses/test_report.py)

&mdash;


## Class scrartcl

Source: [yalafi/documentclasses/scrartcl.py](yalafi/documentclasses/scrartcl.py),
tests: [tests/test\_documentclasses/test\_scrartcl.py](tests/test_documentclasses/test_scrartcl.py)

**Macros**

For macros available in all KOMA classes see package
[koma-script](#package-koma-script).


## Class scrbook

Source: [yalafi/documentclasses/scrbook.py](yalafi/documentclasses/scrbook.py),
tests: [tests/test\_documentclasses/test\_scrbook.py](tests/test_documentclasses/test_scrbook.py)

**Macros**

For macros available in all KOMA classes see package
[koma-script](#package-koma-script).


## Class scrreprt

Source: [yalafi/documentclasses/scrreprt.py](yalafi/documentclasses/scrreprt.py),
tests: [tests/test\_documentclasses/test\_scrreprt.py](tests/test_documentclasses/test_scrreprt.py)

**Macros**

For macros available in all KOMA classes see package
[koma-script](#package-koma-script).

