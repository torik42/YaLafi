
# YaLafi: Yet another LaTeX filter

[Installation](#installation)&nbsp;\|
[Example application](#example-application)&nbsp;\|
[Differences to Tex2txt](#differences-to-tex2txt)

This Python program extracts plain text from LaTeX documents.
Due to the following characteristics, it may be integrated with a
proofreading software:
- tracking of character positions during text manipulations,
- simple inclusion of own LaTeX macros and environments with tailored
  treatment,
- careful conservation of text flows,
- detection of trailing interpunction in equations,
- proper handling of nestable LaTeX elements like {} braces.

For instance, the LaTeX input
```
Only few people\footnote{We use
\textcolor{red}{redx colour.}}
is lazy.
```
will lead to the subsequent output from example application script
[shell.py](yalafi/shell/shell.py) described in section
[Example application](#example-application) ahead.
The script invokes [LanguageTool](https://www.languagetool.org)
as proofreading software, using a local installation or the Web server
hosted by LanguageTool.
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
<a name="example-html-report"></a>
Run with option --html, the script produces an HTML report:

![HTML report](shell.png)

YaLafi is similar to [Tex2txt](https://github.com/matze-dd/Tex2txt),
but differs in the internal processing method.
Instead of using recursive regular expressions, a simple tokeniser
and a small machinery for macro expansion are implemented.

Application Python scripts like [shell.py](yalafi/shell/shell.py)
from section [Example application](#example-application)
can access an interface emulating Tex2txt/tex2txt.py by
```
from yalafi import tex2txt
```
Direct usage as script is almost the same as for Tex2txt/tex2txt.py, compare
[Tex2txt/README.md](https://github.com/matze-dd/Tex2txt/blob/master/README.md#command-line).
Please note the difference for option --defs described in section
[Differences to Tex2txt](#differences-to-tex2txt).
Invocation:
```
python -m yalafi [options] [files]
```

[Back to top](#yalafi-yet-another-latex-filter)


## Installation

There are several possibilities.
- Place yalafi/ or a link to it in the current directory.
- Place yalafi/ in a standard directory like `/usr/lib/python3.?/`
  or `~/.local/lib/python3.?/site-packages/`.
- Place yalafi/ somewhere else and set environment variable PYTHONPATH
  accordingly.

[Back to top](#yalafi-yet-another-latex-filter)


## Example application

Example Python script [shell.py](yalafi/shell/shell.py) will generate a
proofreading report in text or HTML format from filtering the LaTeX input
and application of [LanguageTool](https://www.languagetool.org) (LT).
It is best called as module as shown below.
On option '--server lt', LT's Web server is contacted.
Otherwise, [Java](https://java.com) has to be present, and
the path to LT has to be customised in script variable 'ltdirectory';
compare the corresponding comment in script.
Note that from version 4.8, LT does not fully support 32-bit systems any more.
Both LT and the script will print some progress messages to stderr.
They can be suppressed with `python ... 2>/dev/null`.
```
python -m yalafi.shell
                [--html] [--link] [--context number]
                [--include] [--skip regex] [--plain] [--list-unknown]
                [--language lang] [--t2t-lang lang] [--encoding ienc]
                [--replace file] [--define file] [--extract macros]
                [--disable rules] [--lt-options opts]
                [--single-letters accept] [--equation-punctuation mode]
                [--server mode] [--lt-server-options opts]
                [--textgears apikey]
                latex_file [latex_file ...] [> text_or_html_file]
```
Option names may be abbreviated.
If present, options are also read from a configuration file designated
by script variable config\_file (one option per line, possibly with argument).
Default option values are set at the Python script beginning.
- option `--html`:<br>
  generate HTML report; see below for further details
- option `--link`:<br>
  if HTML report : left-click on a highlighted text part opens Web link
  provided by LT
- option `--context number`:<br>
  number of context lines displayed around each marked text region
  in HTML report; default: 2; negative number: display whole text
- option `--include`:<br>
  track file inclusions like \\input\{...\}; script variable
  'inclusion\_macros' contains list of the corresponding LaTeX macro names
- option `--skip regex`:<br>
  skip files matching the given regular expression;
  useful, e.g., for exclusion of figures on option --include
- option `--plain`:<br>
  assume plain-text input: no evaluation of LaTeX syntax;
  cannot be used together with option --include or --replace
- option `--list-unknown`:<br>
  only print list of unknown macros and environments seen outside of
  maths parts
- option `--language lang`:<br>
  language code as expected by LT, default: 'en-GB';
  first two letters are passed to yalafi.tex2txt()
- option `--t2t-lang lang`:<br>
  overwrite option for yalafi.tex2txt() from --language
- options `--encoding ienc`, `--replace file`:<br>
  like options --ienc, --repl of Tex2txt/tex2txt.py, compare
  [Tex2Txt/README.md](https://github.com/matze-dd/Tex2txt/blob/master/README.md#command-line).
- option `--define file`:<br>
  read macro definitions as LaTeX code (using \\newcommand)
- option `--extract macros`:<br>
  only check arguments of the LaTeX macros whose names are given as
  comma-separated list; useful for check of foreign-language text,
  if marked accordingly
- option `--disable rules`:<br>
  comma-separated list of ignored LT rules, passed as --disable to LT;
  default: 'WHITESPACE\_RULE'
- option `--lt-options opts`:<br>
  pass additional options to LT as single string in argument 'opts';
  first character of 'opts' will be skipped and must not be '-';
  for instance: `--lt-options '~--languagemodel ../LT/Ngrams --mothertongue de-DE'`;
  some options are included into HTML requests to an LT server, see script
  variable lt\_option\_map
- option `--single-letters accept`:<br>
  check for single letters, accepting those in the patterns given as list
  separated by '\|';
  for instance `--singe-letters 'A|a|I|e.g.|i.e.||'` for an English text,
  where the trailing '\|\|' causes addition of equation replacements
  from script variable equation\_replacements;
  all characters except '\|' are taken verbatim, but '~' and '\\,' are
  interpreted as UTF-8 non-breaking space and narrow non-breaking space
- option `--equation-punctuation mode`:<br>
  experimental hack for check of punctuation after equations in English texts;
  abbreviatable mode values, indicating checked equation type:
  'displayed', 'inline', 'all';
  generates a message, if an element of an equation is not terminated
  by a dot '.' and at the same time is not followed by a lower-case word or
  another equation element, both possibly separated by a mark from ',;:';
  patterns for equations are given by script variables
  equation\_replacements\_display and equation\_replacements\_inline
  corresponding to member variables Parameters.math\_repl\_display and
  Parameters.math\_repl\_inline in file yalafi/parameters.py
- option `--server mode`:<br>
  use LT's Web server (mode is 'lt') or a local LT server (mode is 'my');
  stop the local server (mode is 'stop', currently only works under Linux
  and Cygwin)
  - LT's server: address set in script variable 'ltserver';
    for conditions and restrictions, please refer to
    [http://wiki.languagetool.org/public-http-api](http://wiki.languagetool.org/public-http-api)
  - local server: if not yet running, then start it according to script
    variable 'ltserver\_local\_cmd';
    additional server options can be passed with --lt-server-options;
    see also
    [http://wiki.languagetool.org/http-server](http://wiki.languagetool.org/http-server);
    may be faster than command-line tool used otherwise, especially for large
    number of LaTeX files;
    server will not be stopped at the end (use '--server stop')
- option `--lt-server-options opts`:<br>
  pass additional options when starting a local LT server;
  syntax as for --lt-options
- option `--textgears apikey`:<br>
  use the TextGears server, see [https://textgears.com](https://textgears.com);
  language is fixed to American English;
  access key 'apikey' can be obtained on page
  [https://textgears.com/signup.php?givemethatgoddamnkey=please](https://textgears.com/signup.php?givemethatgoddamnkey=please),
  but key 'DEMO\_KEY' seems to work for short input;
  server address is given by script variable textgears\_server

**Dictionary adaptation.**
LT evaluates the two files 'spelling.txt' and 'prohibit.txt' in directory
```
.../LanguageTool-?.?/org/languagetool/resource/<lang-code>/hunspell/
```
Additional words and words that shall raise an error can be appended here.
LT version 4.8 introduced additional files 'spelling\_custom.txt' and
'prohibit\_custom.txt'.

**HTML report.**
The idea of an HTML report goes back to Sylvain Hallé, who developed
[TeXtidote](https://github.com/sylvainhalle/textidote).
Opened in a Web browser, the report displays excerpts from the original 
LaTeX text, highlighting the problems indicated by LT.
The corresponding LT messages can be viewed when hovering the mouse
over these marked places, see the
[introductory example](#example-html-report) above.
With option --link, Web links provided by LT can be directly opened with
left-click.
Script option --context controls the number of lines displayed
around each tagged region;
a negative option value will show the complete LaTeX input text.
If the localisation of a problem is unsure, highlighting will use yellow
instead of orange colour.
For simplicity, marked text regions that intertwine with other ones
are separately repeated at the end.
In case of multiple input files, the HTML report starts with an index.

[Back to top](#yalafi-yet-another-latex-filter)


## Differences to Tex2txt

Invocation of `python -m yalafi ...` differs as follows from
`python tex2txt.py ...` (the script in repository Tex2txt).
- Script option --defs expects a file containing macro definitions as
  LaTeX code.
- Macro definitions with \\(re)newcommand in the LaTeX input are processed.
- Macro arguments need not be delimited by {} braces or \[\] brackets.
- Macros are expanded in the order they appear in the text.
- Position tracking for text parts inside of displayed equations is improved.
- Option --char (position tracking for single characters) is always activated.
- Parameters like predefined LaTeX macros and environments are set in file
  [yalafi/parameters.py](yalafi/parameters.py).
  You can modify them at run-time with script option '--pyth module'.
  The given Python module has to provide a function
  'modify\_parameters(parms)' receiving the parameter object 'parms'.
- Handling of specified \\item\[...\] labels currently is less sophisticated:
  trailing interpunction from a preceding sentence is not repeated after the
  item label.
  (This worked well for German texts.)
- Environments of type 'enumerate' do not yet generate numbered labels.
- Default language is English. It is also used for an unknown language.

[Back to top](#yalafi-yet-another-latex-filter)

