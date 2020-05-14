Work in progress
----------------
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

