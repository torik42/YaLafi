
# YaLafi: Yet another LaTeX filter

This Python package extracts plain text from LaTeX documents.
The software may be integrated with a proofreading tool and an editor.
It provides

- mapping of character positions between LaTeX and plain text,
- simple inclusion of own LaTeX macros and environments with tailored
  treatment,
- careful conservation of text flows,
- some parsing of displayed equations for detection of included “normal” text
  and of interpunction problems,
- support of multi-language documents (experimental).

A complete description is available at the
[GitHub page](https://github.com/matze-dd/YaLafi).

The sample Python application script yalafi/shell/shell.py
integrates the LaTeX filter with the proofreading software
[LanguageTool](https://www.languagetool.org).
It sends the extracted plain text to the proofreader,
maps position information in returned messages back to the LaTeX text,
and generates results in different formats.
You may easily

- create a proofreading report in text or HTML format for a complete
  document tree,
- check LaTeX texts in the editors Emacs and Vim via several plug-ins,
- run the script as emulation of a LanguageTool server with integrated
  LaTeX filtering.

For instance, the LaTeX input
```
Only few people\footnote{We use
\textcolor{red}{redx colour.}}
is lazy.
```
will lead to the text report
```
1.) Line 2, column 17, Rule ID: MORFOLOGIK_RULE_EN_GB
Message: Possible spelling mistake found
Suggestion: red; Rex; reds; redo; Red; Rede; redox; red x
Only few people is lazy.    We use redx colour. 
                                   ^^^^
2.) Line 3, column 1, Rule ID: PEOPLE_VBZ[1]
Message: If 'people' is plural here, don't use the third-person singular verb.
Suggestion: am; are; aren
Only few people is lazy.    We use redx colour. 
                ^^
```
This is the corresponding HTML report:

![HTML report](https://raw.githubusercontent.com/matze-dd/YaLafi/master/figs/shell.png)

