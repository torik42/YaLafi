Work in progress
----------------
- LaTeX macros / environments
  - new package subfiles: macros \\subfile, \\subfileinclude
    (issue [#185](../../issues/185))
  - builtins
    - fixed \\hspace, only add space if argument is not of zero length;
      **thanks to @torik42** (PR [#182](../../pull/182))
    - added macro \\paragraph(\*) (issue [#192](../../issues/192))
    - added macros \\MakeLowercase, \\MakeUppercase;
      **thanks to @torik42** (PR …)
  - package graphicx: added macro \\graphicspath
    (issue [#186](../../issues/186))
  - package tikz: now loads package graphicx (issue [#186](../../issues/186))
- yalafi.shell: on --include, also respect \\subfile, \\subfileinclude
- yalafi core: added file names in LaTeX-related error messages to stderr
  (issue [#169](../../issues/169))
- added CONTRIBUTING.md (issue [#167](../../issues/167))
- README.md: added section on multi-file projects

Version 1.3.0 (2021/01/31)
--------------------------
- LaTeX macros / environments
  - new package geometry: macro \\geometry; **thanks to @blipp**
    (PR [#133](../../pull/133))
  - new package xspace: macro \\xspace; **thanks to @blipp**
    (PR [#134](../../pull/134), issue [#140](../../issues/140))
  - new package mathtools: macro \\mathtoolsset; **thanks to @torik42**
    (PR [#160](../../pull/160))
  - new package unicode-math, **thanks to @torik42**
    (PR [#162](../../pull/162))
    - macros \\setmathfont, \\unimathsetup
    - unicode math operators
  - new package circuitikz: environment circuitikz
    (issue [#158](../../issues/158))
  - new package celeveref, macros like \\cref and companions;
    **thanks to @torik42** (issue [#161](../../issues/161),
    PR [#171](../../pull/171))
  - package amsthm: added macro \\newtheoremstyle; **thanks to @torik42**
    (PR [#164](../../pull/164))
  - package amsmath: added macro \\substack (issue [#163](../../issues/163))
  - package babel
    - language now is also read from global options of \\documentclass
      (issue [#148](../../issues/148))
    - fixed a problem with parsing of package options
      (issue [#147](../../issues/147))
- yalafi.shell
  - added option --no-specials (issue [#131](../../issues/131))
  - options --single-letters and --equation-punctuation now use equation
    replacements according to setting from option --language
    (issue [#152](../../issues/152))
  - fixed problem with --add-modules (issue [#144](../../issues/144))
- yalafi core
  - **changed interface** to extension modules for packages and document
    classes (issue [#172](../../issues/172)):
    function init\_module() now has an additional argument 'position' that
    gives the position of the \\documentclass or \\usepackage token
  - **changed interface** to macro handler functions: added argument 'delim'
    (issue [#136](../../issues/136))
  - added approximation of macro \\def (issue [#125](../../issues/125))
  - added option --nosp (issue [#131](../../issues/131))
  - fixed bug: macro could consume a closing \} as argument token
    (issue [#135](../../issues/135))
  - added iterator for tokens and \{\} nesting levels (iter\_token\_levels()
    in yalafi/parser.py, for issue [#163](../../issues/163))
  - improved error message on recursive \\LTinput
    (issue [#169](../../issues/169))
- README.md: updated (issues [#137](../../issues/137),
  [#159](../../issues/159))
- CI tests: moved to GitHub Actions
- added file .gitignore; **thanks to @mfbehrens99** (PR [#156](../../pull/156))

Version 1.2.0 (2020/11/22)
--------------------------
- LaTeX macros / environments
  - package babel: added environments otherlanguage\(\*\)
    (issue [#114](../../issues/114))
  - builtins
    - fixed \\usepackage, now accepts multiple package names
      (issue [#121](../../issues/121))
    - added macros \\LaTeX, \\TeX (issue [#124](../../issues/124))
- Vim compiler scripts ltyc.vim and vlty.vim: small change for compatibility
  with vim-dispatch
- yalafi.shell
  - added support for multi-language documents (issue [#98](../../issues/98))
  - new options --multi-language, --ml-continue-threshold, --ml-rule-threshold,
    --ml-disable, --ml-disablecategories
  - added flushs for all messages to stderr (issue [#123](../../issues/123))
- yalafi core
  - **changed interface** to extension modules for packages and document
    classes (issue [#110](../../issues/110)).
    Entry point is now function init\_module() with two arguments: parser and
    list of package options.
    See for instance yalafi/packages/amsmath.py and yalafi/packages/babel.py.
  - added support for multi-language documents (issue [#98](../../issues/98));
    including fixed issues [#104](../../issues/104), [#108](../../issues/108),
    [#109](../../issues/109), [#117](../../issues/117)
  - added CLI option '--mula file' for multi-language output
    (issue [#115](../../issues/115))
  - added flushs for all messages to stderr (issue [#123](../../issues/123))
  - corrected character position mapping in verbatim environment
    (issue [#126](../../issues/126))
- README.md: updated, added section for multi-language support

Version 1.1.7 (2020/11/04)
--------------------------
- LaTeX macros / environments
  - builtins: added \\bibitem, \\bibliographystyle, \\begin{thebibliography}
    (issue [#80](../../issues/80))
  - package babel: added optional argument for \\foreignlanguage
- Vim scripts
  - vlty.vim, ltyc.vim: now pass Vim's 'fileencoding' to yalafi.shell
  - lty.vim: removed redundant key read\_temporary\_file
- yalafi.shell
  - added option --simple-equations for simple replacements of displayed
    equations (issue [#85](../../issues/85))
- yalafi core
  - added 'ru' for option --lang (issues [#84](../../issues/84),
    [#90](../../issues/90))
  - added option --seqs for simple replacements of displayed equations
    (issue [#85](../../issues/85))
  - fixed function name clash in tests/test_packages/test\_latex\_builtins.py
    (issue [#86](../../issues/86))
- added tests with Python 3.9
- README.md: updated

Version 1.1.6 (2020/10/19)
--------------------------
- new LaTeX packages
  - babel: macros \\foreignlanguage, \\selectlanguage
    (issue [#72](../../issues/72))
  - inputenc: macro \\inputencoding (issue [#72](../../issues/72))
- yalafi.shell
  - revised character position mapping for text report
    (issues [#73](../../issues/73), [#75](../../issues/75),
    and [#77](../../issues/77))
  - added tests, using option --lt-command and temporarily created LT
    emulations, see directory tests/test\_shell\_cmd/
- Vim script vlty.vim (for vimtex): minor update
- README.md: minor edits

Version 1.1.5 (2020/10/07)
--------------------------
- yalafi core
  - added special LaTeX comments '%%% LT-SKIP-BEGIN' and '%%% LT-SKIP-END',
    e.g., for skipping parts of LaTeX preamble (issue [#56](../../issues/56))
  - added math operators \\cdot and \\times (issue [#65](../../issues/65))
- yalafi.shell
  - fixed error message on unknown language for HTTP server
    (issue [#57](../../issues/57))
  - added option --lt-command, can be used together with '--server my';
    just using current directory if --lt-directory is not specified
    (issue [#60](../../issues/60))
  - updated references to deprecated wiki.languagetool.org
    (issue [#66](../../issues/66))
- Vim scripts
    - ltyc.vim: added option g:ltyc\_showsuggestions
    - vlty.vim, lty.vim, ltyc.vim: added option lt\_command or similar
      (issues [#60](../../issues/60), [#63](../../issues/63))
    - lty.vim, ltyc.vim: added comments for option setting
- Bash script yalafi-grammarous: assume plugin installed under ~/.vim/bundle
- new directory editors/ with all editor interfaces
- README.md: updated, shifted some sections, added screenshot for vimtex plugin

Version 1.1.4 (2020/09/01)
--------------------------
- new LaTeX packages: glossaries, glossaries-extra, pgfplots
- added macros
    - LaTeX builtins: \\index, \\pagenumbering, \\pagestyle, \\thispagestyle,
      \begin{tabular}
    - package biblatex: \\addbibresource, \\printbibliography
- list-of-macros.md: updated
- yalafi core
    - allow '@' in macro names (parameters.py:Parameters.macro\_characters())
    - added method parser.py:Parser.parse\_keyval\_list(): parses lists like
      `name=xxx, description={a b c}`
    - non-alphanumeric characters (except '.') in LaTeX package names are
      replaced by '\_' for corresponding Python module names
      (utils.py:get\_module\_handler())
- travis.yml: use 'python -m pytest' instead of 'pytest'
- added copy of vimtex compiler script vlty.vim

Version 1.1.3 (2020/08/07)
--------------------------
- added extension modules
    - packages: biblatex, graphicx, hyperref, listings, tikz
    - document classes: article, book, report, scrartcl, scrbook
- added file list-of-macros.md
- yalafi
    - added tests for extension modules
    - reduced error message in filter output on LaTeX syntax problem;
      full message now only with `Parameters.mark_latex_error_verbose = True`
      (full message unchanged to stderr)
- ltyc.vim: added file information to errorformat
- updated README

Version 1.1.2 (2020/05/28)
--------------------------
- yalafi
    - added submodule yalafi.packages, currently with:
      amsmath, amsthm, xcolor (incomplete initial versions)
    - added submodule yalafi.documentclasses
    - changed otion --pyth to --pack
    - added option --dcls
    - macros \\documentclass and \\usepackage activate package modules
      from yalafi.documentclasses and yalafi.packages
    - removed redundancies in Parameters.math\_space and
      Parameters.math\_ignore (issue #29)
    - shifted declarations from yalafi/parameters.py to extension modules
      (issue #29)
    - closed issue #30 (optional argument for figure environment,
      missing \\phantom macros)
    - changed definition of table environment
    - \\LTmacros renamed to \\LTinput: also may activate extension modules
- yalafi.shell
    - changed option --python-defs to --packages
    - added option --documentclass
    - added option --add-modules
- added Vim "compiler" ltyc.vim
- removed file definitions.py
- README: updated

Version 1.1.1 (2020/05/14)
--------------------------
- yalafi: fixed issue #26 (handling of \\\\\[...\]),
  added tests/test\_linebreak.py

Version 1.1.0 (2020/05/13)
--------------------------
- yalafi: fixed issue #23 (error recovery for missing \] or \}),
  added test to tests/test\_error.py
- yalafi.shell
    - yalafi/shell/proofreader.py: fixed issue #14
    - added output mode 'xml-b' for XML report, addresses issue #16
    - added some fields to JSON output
    - added option --lt-command, issue #19
    - added options --enable, --disablecategories, --enablecategories
      (issue #21)
- added ALE linter component lty.vim
- README.md
    - new section on related projects, added reference to vscode-ltex
    - added application of Vim plug-in vim-LanguageTool
    - added application of Vim plug-in ALE
- shifted screenshots to directory figs/
- this file: added dates to versions

Version 1.0.0 (2020/04/21)
--------------------------
- yalafi/shell/proofreader.py
    - fixed issue #12
    - more verbose error messages, if start of LT fails
- replaced screenshots for Vim and Emacs application
- updated README.md

Version 0.9.0 (2020/04/14)
--------------------------
- now hopefully close to 1.0.0 ;-)
- yalafi.shell
    - closed issue #7, option --as-server: emulate an LT server with
      integrated LaTeX filter
    - added interface for Emacs-langtool
    - added output mode --output json
    - added option --no-config
    - closed issue #9 (a hack): better highlighting, if a single backslash
      is tagged that actually starts a macro name
      (as before for HTML output only)
    - removed option --t2t-lang (just use 'en' on unknown language)
    - subdivided yalafi/shell/shell.py into several files
- README.md: updated

Version 0.4.0 (2020/04/07)
--------------------------
- yalafi.shell
    - option --lt-options: added passing of -l / --language to HTML request
    - fixed problem with Java under Cygwin: always first go to LT's
      directory, then start Java
    - fixed Issue #6
- closed Issue #2, except: cannot gracefully recover from wrong parameters
  of Python definitions in Macro() etc. in yalafi/paramters.py
- fixed Issue #3, added Bash script yalafi-grammarous
- closed Issue #4
- fixed Issue #5
- yalafi/mathparser.py: slightly improved character position tracking
  in displayed equations
- speed optimisation
    - for large input files, modifications at the start of the token list are
      expensive, producing roughly quadratic run-time of the complete filter
    - we now operate on reversed lists in class scanner.Buffer and in method
      parser.Parser.remove\_pure\_action\_lines()
    - result: faster, and run-time increases quasi linearly with file size
- renamed 'opts' parameter of Macro() etc. to 'defaults'
- README.md: updated

Version 0.3.1 (2020/03/31)
--------------------------
- yalafi.shell
    - added output in XML format for vim-grammarous
    - removed option --html
    - added option '--output mode', mode value in plain, html, xml
    - changed option name --plain to --plain-input
    - added option --lt-directory
- README.md: updated

Version 0.3.0 (2020/03/29)
--------------------------
- added replication of punctuation marks at specified \\item labels
- verbatim environment now can be removed or replaced like other environments
  with appropriate entry in Parser.environment\_defs
- added default labels for environment enumerate
- yalafi/tex2txt.py: option --ienc is effective for file from --defs, too
- README.md: updated
  <br><br>
- yalafi/scanner.py: tested use of regular expression; only a bit faster for
  short texts, but much slower for large texts

Version 0.2.0 (2020/03/25)
--------------------------
- yalafi/shell/shell.py
    - added option --python-defs
    - option --encoding now also effective for file from --define
- macro arguments: optional '*' appears in argument list (was skipped before);
  added tests/test\_asterisk.py
- yalafi/parameters.py: shifted some environment definitions
  to ./definitions.py
- fixed bug from Issue #1
- README.md: added sections
  <br><br>
- included file \_\_init\_\_.py in yalafi/ and yalafi/shell
- yalafi/defs.py: added check of argument references in
  Expandable.\_\_init\_\_()
- added this file

Version 0.1.0 (2020/03/22)
--------------------------
- initial version

