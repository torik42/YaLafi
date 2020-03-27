Work in progress
----------------
- added replication of punctuation marks at specified \\item labels
- verbatim environment now can removed or replaced like other environments
  with approriate entry in Parser.environment\_defs
- README.md: updated
  <br><br>
- yalafi/scanner.py: tested use of regular expression; only a bit faster for
  short texts, but much slower for large texts

Version 0.2.0
-------------
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

Version 0.1.0
-------------
- initial version

