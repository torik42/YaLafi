
# YaLafi: Yet another LaTeX filter

**Notice.**
The library of LaTeX macros, environments, document classes, and packages is
still rather restricted, compare the [list of macros](list-of-macros.md).
Please don't hesitate to
[raise an Issue](../../issues),
if you would like to have added something.

**Summary.**
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

The sample Python application yalafi.shell from section
[Example application](#example-application) integrates the LaTeX filter
with the proofreading software [LanguageTool](https://www.languagetool.org).
It sends the extracted plain text to the proofreader,
maps position information in returned messages back to the LaTeX text,
and generates results in different formats.
You may easily
- create a proofreading report in text or HTML format for a complete
  document tree,
- check LaTeX texts in the editors Vim, Emacs and Atom via several plugins,
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
<a name="example-html-report"></a>
This is the corresponding HTML report
(for an example with a Vim plugin, [see here](#example-vimtex-plugin)):

![HTML report](figs/shell.png)

The tool builds on results from project
[Tex2txt](https://github.com/matze-dd/Tex2txt),
but differs in the internal processing method.
Instead of using recursive regular expressions, a simple tokeniser
and a small machinery for macro expansion are implemented; see sections
[Differences to Tex2txt](#differences-to-tex2txt) and
[Remarks on implementation](#remarks-on-implementation).

Beside the interface from section
[Python package interface](#python-package-interface),
application Python scripts like [yalafi/shell/shell.py](yalafi/shell/shell.py)
from section [Example application](#example-application)
can access an interface emulating tex2txt.py from repository
[Tex2txt](https://github.com/matze-dd/Tex2txt)
by 'from yalafi import tex2txt'.
The pure LaTeX filter can be directly used in scripts via a command-line
interface, it is described in section
[Command-line of pure filter](#command-line-of-pure-filter).

If you use this software and encounter a bug or have other suggestions
for improvement, please leave a note under category [Issues](../../issues),
or initiate a pull request.
Many thanks in advance.

Happy TeXing!


## Contents

[Installation](#installation)<br>
[Example application](#example-application)<br>
[Interfaces to Vim](#interfaces-to-vim)<br>
[Interface to Emacs](#interface-to-emacs)<br>
[Interface to Atom](#interface-to-atom)<br>
[Usage under Windows](#usage-under-windows)<br>
[Related projects](#related-projects)<br>
<br>
[Filter actions](#filter-actions)<br>
[Fundamental limitations](#fundamental-limitations)<br>
[Adaptation of LaTeX and plain text](#adaptation-of-latex-and-plain-text)<br>
[Extension modules for LaTeX packages](#extension-modules-for-latex-packages)<br>
[Inclusion of own macros](#inclusion-of-own-macros)<br>
<br>
[Multi-file projects](#multi-file-projects)<br>
[Handling of displayed equations](#handling-of-displayed-equations)<br>
[Multi-language documents](#multi-language-documents)<br>
[Python package interface](#python-package-interface)<br>
[Command-line of pure filter](#command-line-of-pure-filter)<br>
[Differences to Tex2txt](#differences-to-tex2txt)<br>
[Remarks on implementation](#remarks-on-implementation)


## Installation

**YaLafi (at least with Python version 3.6).**
Choose one of the following possibilities.

- Use `python -m pip install [--user] yalafi`.
  This installs the last version uploaded to [PyPI](https://www.pypi.org).
  Module pip itself can be installed with `python -m ensurepip`.
- Say `python -m pip install [--user] git+https://github.com/matze-dd/YaLafi.git@master`.
  This installs the current snapshot from here.
- Download the archive from here and unpack it.
  Place yalafi/ in the working directory, or in a standard directory like
  `/usr/lib/python3.8/` or `~/.local/lib/python3.8/site-packages/`.
  You can also locate it somewhere else and set environment variable
  PYTHONPATH accordingly.

**LanguageTool.**
On most systems, you have to install the software “manually” (1).
At least under Arch Linux, you can also use a package manager (2).
Please note that, for example under Ubuntu,
`sudo snap install languagetool` will *not* install the components required
here.

1. The LanguageTool zip archive, for example LanguageTool-5.0.zip, can be
obtained from the
[LanguageTool download page](https://www.languagetool.org/download).
Option --lt-directory of application yalafi.shell from section
[Example application](#example-application)
has to point to the directory created after uncompressing the archive
at a suitable place.
For instance, the directory has to contain file 'languagetool-server.jar'.

2. Under Arch Linux, you can simply say `sudo pacman -S languagetool`.
In this case, it is not necessary to set option --lt-directory from
variant 1.
Instead, you have to specify `--lt-command languagetool`.

[Back to contents](#contents)


## Example application

**Remark.**
You can find examples for tool integration with Bash scripts in
[Tex2txt/README.md](https://github.com/matze-dd/Tex2txt#tool-integration).

Example Python script [yalafi/shell/shell.py](yalafi/shell/shell.py)
will generate a proofreading report in text or HTML format from filtering
the LaTeX input and application of
[LanguageTool](https://www.languagetool.org) (LT).
It is best called as module as shown below, but can also be placed elsewhere
and invoked as script.
A simple invocation producing an HTML report could be:
```
python -m yalafi.shell --lt-directory ~/lib/LT --output html t.tex > t.html
```
On option '--server lt', LT's Web server is contacted.
Otherwise, [Java](https://java.com) has to be present, and
the path to LT has to be specified with --lt-directory or --lt-command.
Note that from version 4.8, LT does not fully support 32-bit systems any more.
Both LT and the script will print some progress messages to stderr.
They can be suppressed with `python ... 2>/dev/null`.
```
python -m yalafi.shell [OPTIONS] latex_file [latex_file ...] [> text_or_html_file]
```
Option names may be abbreviated.
If present, options are also read from a configuration file designated by
script variable 'config\_file' (one option per line, possibly with argument),
unless --no-config is given.
Default option values are set at the Python script beginning.

- `--lt-directory dir`<br>
  Directory of the “manual” local LT installation (for variant 1 in section
  [Installation](#installation)).
  May be omitted on options '--server lt' and '--textgears apikey',
  or if script variable 'ltdirectory' has been set appropriately.
  See also the script comment at variable 'ltdirectory'.
- `--lt-command cmd`<br>
  Base command to call LT (for variant 2 in section
  [Installation](#installation)).
  For instance, this is '--lt-command languagetool'.
  If an LT server has to be started, the command is invoked with option --http.
  Note that option '--server stop' for stopping a local LT server will not
  work in this case.
- `--as-server port`<br>
  Emulate an LT server listening on the given port, for an example
  see section [Interface to Emacs](#interface-to-emacs).
  The fields of received HTML requests (settings for language, rules,
  categories) overwrite option values given in the command line.
  The internally used proofreader is influenced by options like --server.
  Other options like --single-letters remain effective.
- `--output mode`<br>
  Mode is one of 'plain', 'html', 'xml', 'xml-b', 'json'
  (default: 'plain' for text report).
  Variant 'html' generates an HTML report, see below for further details.
  Modes 'xml', 'xml-b' and 'json' are intended for Vim plugins, compare section
  [Interfaces to Vim](#interfaces-to-vim).
- `--link`<br>
  In an HTML report, left-click on a highlighted text part opens a
  Web link related to the problem, if provided by LT.
- `--context number`<br>
  Number of context lines displayed around each marked text region
  in HTML report (default: 2).
  A negative number shows the whole text.
- `--include`<br>
  Track file inclusions like \\input{...}.
  Script variable 'inclusion\_macros' contains a list of the corresponding
  LaTeX macro names.
- `--skip regex`<br>
  Skip files matching the given regular expression.
  This is useful, e.g., for the exclusion of figures on option --include.
- `--plain-input`<br>
  Assume plain-text input, do not evaluate LaTeX syntax.
  This cannot be used together with options --include or --replace.
- `--list-unknown`<br>
  Only print a list of unknown macros and environments seen outside of
  maths parts.
  Compare, for instance, [Issue #183](../../issues/183).
- `--language lang`<br>
  Language code as expected by LT (default: 'en-GB').
- `--encoding ienc`<br>
  Encoding for LaTeX input and files from options --define and --replace
  (default: UTF-8).
- `--replace file`<br>
  File with phrase replacements to be performed after the conversion to
  plain text; see section
  [Phrase replacement in the plain text](#phrase-replacement-in-the-plain-text).
- `--define file`<br>
  Read macro definitions as LaTeX code (using \\newcommand or \\def).
  If the code invokes \\documentclass or \\usepackage, then the corresponding
  modules are loaded.
- `--documentclass  class`<br>
  Load extension module for this class.
  See section
  [Extension modules for LaTeX packages](#extension-modules-for-latex-packages).
- `--packages modules`<br>
  Load these extension modules for LaTeX packages, given as comma-separated list
  (default: '\*').
  See section
  [Extension modules for LaTeX packages](#extension-modules-for-latex-packages).
- `--add-modules file`<br>
  Parse the given LaTeX file and prepend all modules included by macro
  \\usepackage to the list provided in option --packages.
  Value of option --documentclass is overridden by macro \\documentclass.
- `--extract macros`<br>
  Only check first mandatory argument of the LaTeX macros whose names are
  given as comma-separated list.
  The option only works properly for predefined macros, including those
  imported by options --documentclass, --define, and --packages.
  This is useful for check of foreign-language text, if marked accordingly.
  Internally used for detection of file inclusions on --include.
- `--simple-equations`<br>
  Replace a displayed equation only with a single placeholder from collections
  'math\_repl\_display\*' in file yalafi/parameters;
  append trailing interpunction, if present.
- `--no-specials`<br>
  Revert changes from special macros and magic comments described in section
  [Modification of LaTeX text](#Modification-of-latex-text).
- `--disable rules`<br>
  Comma-separated list of ignored LT rules, is passed as --disable to LT
  (default: 'WHITESPACE\_RULE').
- `--enable rules`<br>
  Comma-separated list of added LT rules, is passed as --enable to LT
  (default: '').
- `--disablecategories cats`<br>
  `--enablecategories cats`<br>
  Disable / enable LT rule categories, directly passed to LT
  (default for both: '').
- `--lt-options opts`<br>
  Pass additional options to LT, given as single string in argument 'opts'.
  The first character of 'opts' will be skipped and must not be '-'.
  Example:
  `--lt-options '~--languagemodel ../Ngrams --disablecategories PUNCTUATION'`.
  Some options are included into HTML requests to an LT server, see script
  variable 'lt\_option\_map'.
- `--single-letters accept`<br>
  Check for single letters, accepting those in the patterns given as list
  separated by '\|'.
  Example: `--single-letters 'A|a|I|e.g.|i.e.||'` for an English text,
  where the trailing '\|\|' causes the addition of equation and language-change
  replacements from collections 'math\_repl\_\*' and 'lang\_change\_repl\_\*'
  in file yalafi/parameters.py.
  All characters except '\|' are taken verbatim, but '~' and '\\,' are
  interpreted as UTF-8 non-breaking space and narrow non-breaking space.
- `--equation-punctuation mode`<br>
  This is an experimental hack for the check of punctuation after equations
  in English texts, compare section
  [Equation replacements in English documents](#equation-replacements-in-english-documents).
  An example is given in section
  [Differences to Tex2txt](#differences-to-tex2txt).
  The abbreviatable mode values indicate the checked equation type:
  'displayed', 'inline', 'all'.<br>
  The check generates a message, if an element of an equation is not
  terminated by a dot '.', and at the same time is not followed by a
  lower-case word or another equation element, both possibly separated by
  a punctuation mark from ',;:'.
  Patterns for equation elements are given by collections
  'math\_repl\_display\*' and 'math\_repl\_inline\*' in
  file yalafi/parameters.py.
- `--server mode`<br>
  Use LT's Web server (mode is 'lt') or a local LT server (mode is 'my')
  instead of LT's command-line tool.
  Stop the local server (mode is 'stop', currently only works under Linux
  and Cygwin).
  - LT's server: Server address is set in script variable 'ltserver'.
    For conditions and restrictions, please refer to
    [https://dev.languagetool.org/public-http-api](https://dev.languagetool.org/public-http-api).
  - Local server: If not yet running, then start it according to script
    variable 'ltserver\_local\_cmd'.
    On option --lt-command, the specified command is invoked with option
    --http.
    Additional server options can be passed with --lt-server-options.
    See also
    [https://dev.languagetool.org/http-server](https://dev.languagetool.org/http-server).
    This may be faster than the command-line tool used otherwise, especially
    when checking many LaTeX files or together with an editor plugin.
    The server will not be stopped at the end (use '--server stop').
- `--lt-server-options opts`<br>
  Pass additional options when starting a local LT server.
  Syntax is as for --lt-options.
- `--textgears apikey`<br>
  Use the TextGears server, see [https://textgears.com](https://textgears.com).
  Language is fixed to American English.
  The access key 'apikey' can be obtained on page
  [https://textgears.com/signup.php?givemethatgoddamnkey=please](https://textgears.com/signup.php?givemethatgoddamnkey=please),
  but the key 'DEMO\_KEY' seems to work for short input.
  The server address is given by script variable 'textgears\_server'.
- `--multi-language`<br>
  Activate support of multi-language documents;
  compare section [Multi-language documents](#multi-language-documents)
  for further related options.
- `--no-config`<br>
  Do not read config file, whose name is set in script variable 'config\_file'.

<a name="dictionary-adaptation"></a>
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

[Back to contents](#contents)


## Interfaces to Vim

As [\[Vim\]](https://www.vim.org)
is a great editor, there are several possibilities that build
on existing Vim plugins or use Vim's compiler interface:

[plugin vimtex](#plugin-vimtex)&nbsp;\|
[“plain Vim”](#plain-vim)&nbsp;\|
[plugin vim-grammarous](#plugin-vim-grammarous)&nbsp;\|
[plugin vim-LanguageTool](#plugin-vim-languagetool)&nbsp;\|
[plugin ALE](#plugin-ale)

### Plugin vimtex

The Vim plugin [\[vimtex\]](https://github.com/lervag/vimtex)
provides comprehensive support for writing LaTeX documents.
It includes an interface to YaLafi, documentation is available with
`:help vimtex-grammar-vlty`.
A copy of the corresponding Vim compiler script is
[editors/vlty.vim](editors/vlty.vim).

The following snippet demonstrates a basic vimrc setting and some useful
values for vlty option field 'shell\_options'.
```
map <F9> :w <bar> compiler vlty <bar> make <bar> :cw <cr><esc>
let g:tex_flavor = 'latex'
set spelllang=de_DE
let g:vimtex_grammar_vlty = {}
let g:vimtex_grammar_vlty.lt_directory = '~/lib/LanguageTool-5.0'
" let g:vimtex_grammar_vlty.lt_command = 'languagetool'
let g:vimtex_grammar_vlty.server = 'my'
let g:vimtex_grammar_vlty.show_suggestions = 1
let g:vimtex_grammar_vlty.shell_options =
        \   ' --multi-language'
        \ . ' --packages "*"'
        \ . ' --define ~/vlty/defs.tex'
        \ . ' --replace ~/vlty/repls.txt'
        \ . ' --equation-punctuation display'
        \ . ' --single-letters "i.\,A.\|z.\,B.\|\|"'
```
- Function key 'F9' saves the file, starts the compiler, and opens the quickfix
  window.
- Uncomment the line with `g:vimtex_grammar_vlty.lt_command`, if LanguageTool
  has been installed by variant 2 in section [Installation](#installation).
  In this case, specification of `g:vimtex_grammar_vlty.lt_directory` is
  not necessary.
- The option `g:vimtex_grammar_vlty.server = 'my'` usually results in faster 
  checks for small to medium LaTeX files.
  Start-up time is saved, and speed benefits from the internal sentence caching
  of the server.
- Saying `let g:vimtex_grammar_vlty.show_suggestions = 1` causes display of
  LanguageTool's replacement suggestions.
- With option `--multi-language`, commands from LaTeX package 'babel' switch
  the language for the proofreading program.
  See section [Multi-language documents](#multi-language-documents).
- By default, the vlty compiler passes names of all necessary LaTeX packages
  to YaLafi, which may result in annoying warnings.
  In multi-file projects, these are suppressed by `--packages "*"` that simply
  loads all packages known to the filter.
- YaLafi's expansion of project-specific macros can be controlled via
  option `--define ...`.
  Example for defs.tex (Note that the first three lines are only necessary,
  if the currently edited file does not directly contain these definitions.):
```
    \newcommand{\zB}{z.\,B. }   % LanguageTool correctly insists on
                                % narrow space in this German abbreviation
    \newtheorem{Satz}{Satz}     % correctly expand \begin{Satz}[siehe ...]
    \LTinput{main.glsdefs}      % read database of glossaries package
```
- Replacement of phrases may be performed via `--replace ...`, compare section
  [Phrase replacement in the plain text](#phrase-replacement-in-the-plain-text).
- Option `--equation-punctuation display` enables some additional
  interpunction checking for displayed equations in English texts, see
  section [Example application](#example-application) and
  [this example](#equation-html-report).
- Option `--single-letters ...` activates search for isolated single letters.
  Note that only the '\|' signs need to be escaped here; compare
  section [Example application](#example-application).

<a name="example-vimtex-plugin"></a>
Here is the [introductory example](#example-html-report) from above:

![Vim plugin vim-vimtex](figs/vim-vimtex.png)

### “Plain Vim”

File [editors/ltyc.vim](editors/ltyc.vim) proposes a simple application to
Vim's compiler interface.
The file has to be copied to a directory like `~/.vim/compiler/`.

For a Vim session, the component is activated with `:compiler ltyc`.
Command `:make` invokes yalafi.shell, and the cursor is set to the first
indicated problem.
The related error message is displayed in the status line.
Navigation between errors is possible with `:cn` and `:cp`, an error list
is shown with `:cl`.
The quickfix window appears on `:cw`.

The following snippet demonstrates a basic vimrc setting and some useful
values for option 'ltyc\_shelloptions'.
Please refer to section [Plugin vimtex](#plugin-vimtex)
for related comments.
```
map <F9> :w <bar> compiler ltyc <bar> make <bar> :cw <cr><esc>
let g:ltyc_ltdirectory = '~/lib/LanguageTool-5.0'
" let g:ltyc_ltcommand = 'languagetool'
let g:ltyc_server = 'my'
let g:ltyc_showsuggestions = 1
let g:ltyc_language = 'de-DE'
let g:ltyc_shelloptions =
        \   ' --multi-language'
        \ . ' --replace ~/ltyc/repls.txt'
        \ . ' --define ~/ltyc/defs.tex'
        \ . ' --equation-punctuation display'
        \ . ' --single-letters "i.\,A.\|z.\,B.\|\|"'
compiler ltyc
```
The screenshot resembles that from section [Plugin vimtex](#plugin-vimtex).

### Plugin vim-grammarous

For the Vim plugin
[\[vim-grammarous\]](https://github.com/rhysd/vim-grammarous),
it is possible to provide an interface for checking LaTeX texts.
With an entry in \~/.vimrc, one may simply replace the command that
invokes LanguageTool.
For instance, you can add to \~/.vimrc
```
let g:grammarous#languagetool_cmd = '/home/foo/bin/yalafi-grammarous'
map <F9> :GrammarousCheck --lang=en-GB<CR>
```
A proposal for Bash script /home/foo/bin/yalafi-grammarous (replace foo
with username ;-) is given in
[editors/yalafi-grammarous](editors/yalafi-grammarous).
It has to be made executable with `chmod +x ...`.
Please adapt script variable `ltdir`, compare option --lt-directory
in section [Example application](#example-application).
If you do not want to have started a local LT server, comment out the line
defining script variable `use_server`.

In order to avoid the problem described in
[Issue \#89\@vim-grammarous](https://github.com/rhysd/vim-grammarous/issues/89)
(shifted error highlighting, if after non-ASCII character on same line),
you can set `output=xml-b` in yalafi-grammarous.

<a name="troubleshooting-for-vim-interface"></a>
**Troubleshooting for Vim interface.**
If Vim reports a problem with running LT, you can do the following.
In `~/bin/yalafi-grammarous`, comment out the final `... 2>/dev/null`.
For instance, you can just place a '\#' in front: `... # 2>/dev/null`.
Then start, with a test file t.tex,
```
$ ~/bin/yalafi-grammarous t.tex
```
This should display some error message, if the problem goes back to
running the script, Python, yalafi.shell or LanguageTool.

Here is the [introductory example](#example-html-report) from above:

![Vim plugin vim-grammarous](figs/vim-grammarous.png)

### Plugin vim-LanguageTool

The Vim plugin
[\[vim-LanguageTool\]](https://github.com/dpelle/vim-LanguageTool)
relies on the same XML interface to LanguageTool as the variant in
section [Plugin vim-grammarous](#plugin-vim-grammarous).
Therefore, one can reuse the Bash script
[editors/yalafi-grammarous](editors/yalafi-grammarous).
You can add to \~/.vimrc
```
let g:languagetool_cmd = '$HOME/bin/yalafi-grammarous'
let g:languagetool_lang = 'en-GB'
let g:languagetool_disable_rules = 'WHITESPACE_RULE'
map <F9> :LanguageToolCheck<CR>
```
Please note the general problem indicated in
[Issue #17](../../issues/17).
Here is again the [introductory example](#example-html-report) from above.
Navigation between highlighted text parts is possible with `:lne` and `:lp`.

![Vim plugin vim-LanguageTool](figs/vim-languagetool.png)

### Plugin ALE

With [\[ALE\]](https://github.com/dense-analysis/ale),
the proofreader ('linter') by default is invoked as background task,
whenever one leaves insert mode.
You might add to \~/.vimrc
```
" if not yet set:
filetype plugin on
" F9: show detailed LT message for error under cursor, is left with 'q'
map <F9> :ALEDetail<CR>
" this turns off all other tex linters
let g:ale_linters = { 'plaintex': ['lty'], 'tex': ['lty'] }
" default place of LT installation: '~/lib/LanguageTool'
let g:ale_tex_lty_ltdirectory = '~/lib/LanguageTool-4.7'
" uncomment the following assignment, if LT has been installed via package
" manager; in this case, g:ale_tex_lty_ltdirectory hasn't to be specified
" let g:ale_tex_lty_command = 'languagetool'
" set to '' to disable server usage or to 'lt' for LT's Web server
let g:ale_tex_lty_server = 'my'
" default language: 'en-GB'
let g:ale_tex_lty_language = 'en-GB'
" default disabled LT rules: 'WHITESPACE_RULE'
let g:ale_tex_lty_disable = 'WHITESPACE_RULE'
```
Similarly to setting 'g:ale\_tex\_lty_disable', one can specify LT's options
--enable, --disablecategories, and --enablecategories.
Further options for yalafi.shell
(compare section [Plugin vimtex](#plugin-vimtex)) may be passed like
```
let g:ale_tex_lty_shelloptions = '--single-letters "A|a|I|e.g.|i.e.||"'
                \ . ' --equation-punctuation display'
```
Additionally, one has to install ALE and copy or link file
[editors/lty.vim](editors/lty.vim)
to directory `~/.vim/bundle/ale/ale_linters/tex/`, or a similar location.

Here is again the [introductory example](#example-html-report) from above.
The complete message for the error at the cursor is displayed on `F9`,
together with LT's rule ID, replacement suggestions, and the problem context
(left with `q`).
Navigation between highlighted text parts is possible with `:lne` and `:lp`,
an error list is shown with `:lli`.

![Vim plugin ALE](figs/vim-ale.png)

[Back to contents](#contents)


## Interface to Emacs

The Emacs plugin
[\[Emacs-langtool\]](https://github.com/mhayashi1120/Emacs-langtool)
may be used in two variants.
First, you can add to \~/.emacs
```
(setq langtool-bin "/home/foo/bin/yalafi-emacs")
(setq langtool-default-language "en-GB")
(setq langtool-disabled-rules "WHITESPACE_RULE")
(require 'langtool)
```
A proposal for Bash script /home/foo/bin/yalafi-emacs (replace foo
with username ;-) is given in [editors/yalafi-emacs](editors/yalafi-emacs).
It has to be made executable with `chmod +x ...`.
Please adapt script variable `ltdir`, compare option --lt-directory
in section [Example application](#example-application).
If you do not want to have started a local LT server, comment out the line
defining script variable `use_server`.

**Troubleshooting for Emacs interface.**
If Emacs reports a problem with running LT, you can apply the steps from
[\[Troubleshooting for Vim interface\]](#troubleshooting-for-vim-interface)
to `~/bin/yalafi-emacs`.

**Server interface.**
This variant may result in better tracking of character positions.
In order to use it, you can write in \~/.emacs
```
(setq langtool-http-server-host "localhost"
      langtool-http-server-port 8082)
(setq langtool-default-language "en-GB")
(setq langtool-disabled-rules "WHITESPACE_RULE")
(require 'langtool)
```
and start yalafi.shell as server in another terminal with
```
$ python -m yalafi.shell --as-server 8082 [--lt-directory /path/to/LT]
```
The server will print some progress messages and can be stopped with CTRL-C.
Further script arguments from section
[Example application](#example-application)
may be given.
If you add, for instance, '--server my', then a local LT server will be used.
It is started on the first HTML request received from Emacs-langtool,
if it is not yet running.

**Installation of Emacs-langtool.**
Download and unzip Emacs-langtool.
Place file langtool.el in directory \~/.emacs.d/lisp/.
Set in your \~/.profile or \~/.bash\_profile (and log in again)
```
export EMACSLOADPATH=~/.emacs.d/lisp:
```

Here is the [introductory example](#example-html-report) from above:

![Emacs plugin Emacs-langtool](figs/emacs-langtool.png)

[Back to contents](#contents)


## Interface to Atom

For the editor [\[Atom\]](https://atom.io), you can use the plugin
[\[linter-yalafi\]](https://github.com/mfbehrens99/linter-yalafi).
Please note that we have not yet tested this interface.

[Back to contents](#contents)


## Usage under Windows

Both yalafi.shell and yalafi can be directly used in a Windows command
script or console.
For example, this could look like
```
py -3 -m yalafi.shell --server lt --output html t.tex > t.html
```
or
```
"c:\Program Files\Python\Python37\python.exe" -m yalafi.shell --server lt --output html t.tex > t.html
```
if the Python launcher has not been installed.

Files with Windows-style line endings (CRLF) are accepted, but the text
output of the pure LaTeX filter will be Unix style (LF only), unless a
Windows Python interpreter is used.

Python's version for Windows by default prints Latin-1 encoded text to
standard output.
As this ensures proper work in a Windows command console, we do not change it
for yalafi.shell when generating a text report.
All other output is fixed to UTF-8 encoding.

[Back to contents](#contents)


## Related projects

This project relates to software like

[OpenDetex](https://github.com/pkubowicz/opendetex)&nbsp;\|
[pandoc](https://github.com/jgm/pandoc)&nbsp;\|
[plasTeX](https://github.com/tiarno/plastex)&nbsp;\|
[pylatexenc](https://github.com/phfaist/pylatexenc)&nbsp;\|
[TeXtidote](https://github.com/sylvainhalle/textidote)&nbsp;\|
[tex2txt](http://hackage.haskell.org/package/tex2txt)&nbsp;\|
[vscode-ltex](https://github.com/valentjn/vscode-ltex)

From these examples, currently (March 2020) only TeXtidote and vscode-ltex
provide position mapping between the LaTeX input text and the plain text
that is sent to the proofreading software.
Both use (simple) regular expressions for plain-text extraction and are
easy to install.
YaLafi, on the other hand, aims to achieve high flexibility and a
good filtering quality with minimal number of false positives from the
proofreading software.

[Back to contents](#contents)


## Filter actions

Here is a list of the most important filter operations.
When the filter encounters a LaTeX problem like a missing end of equation,
a message is printed to stderr.
Additionally, the mark from 'Parameters.mark\_latex\_error' in file
yalafi/parameters.py is included into the filter output.
This mark should raise a spelling error from the proofreader at the place
where the problem was detected.

- A collection of standard LaTeX macros and environments is already included,
  but very probably it has to be complemented.
  Compare variables 'Parameters.macro\_defs\_latex', 
  'Parameters.macro\_defs\_python', and
  'Parameters.environment\_defs' in file yalafi/parameters.py.
- The macros \\documentclass and \\usepackage load extension modules that
  define important macros and environments provided by the corresponding
  LaTeX packages.
  For other activation methods of these modules, see also section
  [Extension modules for LaTeX packages](#extension-modules-for-latex-packages).
- Macro definitions with \\(re)newcommand and \\def (the latter only roughly
  approximated) in the input text are processed.
  Statement \\LTinput{file.tex} reads macro definitions from the given file.
  Further own macros with arbitrary arguments can be defined on Python level,
  see section [Inclusion of own macros](#inclusion-of-own-macros).
- Unknown macros are silently ignored, keeping their arguments
  with enclosing \{\} braces removed.
  They can be listed with options --unkn and --list-unknown for yalafi
  and yalafi.shell, respectively.
- Environment frames \\begin\{...\} and \\end\{...\} are deleted.
  We implement tailored behaviour for environment types listed in
  'Parameters.environment\_defs' in file yalafi/parameters.py,
  see section [Inclusion of own macros](#inclusion-of-own-macros).
  For instance, environment bodies can be removed or replaced by fixed text.
- Text in heading macros as \\section\{...\} is extracted with
  added interpunction, see variable 'Parameters.heading\_punct' in 
  file yalafi/parameters.py.
  This suppresses false positives from LanguageTool.
- For macros as \\ref, \\eqref, \\pageref, and \\cite, suitable placeholders
  are inserted.
- Arguments of macros like \\footnote are appended to the main text,
  separated by blank lines.
  This preserves text flows.
- Inline maths material $...$ and \\(...\\) is replaced with text from the
  rotating collections 'math\_repl\_inline\*' in file yalafi/parameters.py.
  Trailing interpunction from 'Parameters.math\_punctuation' is appended.
- Equation environments are resolved in a way suitable for check of
  interpunction and spacing.
  The argument of macros like \\mbox and \\text is included into the output
  text.
  Versions \\\[...\\\] and $$...$$ are handled like environment displaymath.
  See also sections
  [Handling of displayed equations](#handling-of-displayed-equations)
  and
  [Parser for maths material](#parser-for-maths-material).
- We generate numbered default \\item labels for environment enumerate.
- For \\item with specified \[...\] label, some treatment is provided.
  If the text before ends with a punctuation mark from collection
  'Parameters.item\_punctuation' in file yalafi/parameters.py, then this mark
  is appended to the label.
  This works well for German texts, it is turned off with the setting
  'item\_punctuation = []'.
- Letters with text-mode accents as '\\\`' or '\\v' are translated to the
  corresponding UTF-8 characters.
- Things like double quotes '\`\`' and dashes '\-\-' are replaced with
  the corresponding UTF-8 characters.
  Additionally, we replace '\~' and '\\,' by UTF-8 non-breaking space and
  narrow non-breaking space.
- For language 'de', suitable replacements for macros like '"\`' and '"='
  are inserted, see method 'Parameters.init\_parser\_languages()' in
  file yalafi/parameters.py.
- Macro \\verb and environment verbatim are processed.
  Environment verbatim can be replaced or removed like other environments
  with an appropriate entry in 'Parameters.environment\_defs' in
  yalafi/parameters.py.
- Rare warnings from the proofreading program can be suppressed using
  \\LTadd{...}, \\LTskip{...}, \\LTalter{...}{...} in the LaTeX text;
  compare section
  [Adaptation of LaTeX and plain text](#adaptation-of-latex-and-plain-text).
- Complete text sections, for instance parts of the LaTeX preamble, may be
  skipped with the special LaTeX comment '%%% LT-SKIP-BEGIN'; see section
  [Adaptation of LaTeX and plain text](#adaptation-of-latex-and-plain-text).

[Back to contents](#contents)


## Fundamental limitations

The implemented parsing mechanism can only roughly approximate the behaviour
of a real LaTeX system.
We assume that only “reasonable” macros are used, lower-level TeX operations
are not supported.
If necessary, they should be enclosed in \\LTskip{...} (see section
[Adaptation of LaTeX and plain text](#adaptation-of-latex-and-plain-text))
or be placed in a LaTeX file “hidden” for the filter
(compare option --skip of yalafi.shell in section
[Example application](#example-application)).
With little additional work, it might be possible to include some plain-TeX
features like parsing of elastic length specifications.
A list of remaining incompatibilities must contain at least the following
points.

- Mathematical material is represented by simple replacements.
  As the main goal is application of a proofreading software, we have
  deliberately taken this approach.
- Parsing does not cross file boundaries.
  Tracking of file inclusions is possible though.
- Macros depending on (spacing) lengths may be treated incorrectly.
- Character '\@' always has category 'letter'.
  See [Issue #183](../../issues/183).

[Back to contents](#contents)


## Adaptation of LaTeX and plain text

In order to suppress unsuitable but annoying messages from the proofreading
tool, it is sometimes necessary to modify the input text.
You can do that in the LaTeX code, or after filtering in the plain text.

### Modification of LaTeX text

The following operations can be deactivated with options --nosp and
--no-specials of yalafi and yalafi.shell, respectively.
For instance, macro \\LTadd will be defined, but it will *not* add its
argument to the plain text.

**Special macros.**
Small modifications, for instance concerning interpunction, can be made
with the predefined macros \\LTadd, \\LTalter and \\LTskip.
In order to add a full stop for the proofreader only, you would write
```
... some text\LTadd{.}
```
For LaTeX itself, the macros also have to be defined.
A good place is the document preamble.
(For the last line, compare section
[Inclusion of own macros](#inclusion-of-own-macros).)
```
\newcommand{\LTadd}[1]{}
\newcommand{\LTalter}[2]{#1}
\newcommand{\LTskip}[1]{#1}
\newcommand{\LTinput}[1]{}
```
The LaTeX filter will ignore these statements.
In turn, it will include the argument of \\LTadd, use the second argument
of \\LTalter, and neglect the argument of \\LTskip.
The macro names for \\LTadd etc. are defined by variables
'Parameters.macro\_filter\_add' etc. in file yalafi/parameters.py.

**Special comments.**
Mainly the document preamble often contains statements not properly
processed “out-of-the-box”.
Placing the critical parts in \\LTskip{...} may lead to problems, as the
statements now are executed slightly differently by the TeX system.
As “brute-force” variant, the LaTeX filter therefore ignores input enclosed
in comments starting with `%%% LT-SKIP-BEGIN` and `%%% LT-SKIP-END`.
Note that the single space after `%%%` is significant.
The opening special comment is given in variable
'Parameters.comment\_skip\_begin' of file yalafi/parameters.py.

A preamble could look as follows.
```
\documentclass{article}
%%% LT-SKIP-BEGIN
... disturbing stuff ...
%%% LT-SKIP-END
\title{A paper}
\begin{document}
```

### Phrase replacement in the plain text

Yalafi.shell and yalafi provide options `--replace file` and `--repl file`,
respectively.
They may be valuable, if you often use a phrase (possibly of multiple
words) that is not accepted by the proofreader.
In the given file, a '\#' sign marks the rest of the line as comment.
The first '\&' separated by space splits a line into two parts;
the first part is replaced by the second one.
Space in the first part may correspond to arbitrary space in the plain
text that does not break the paragraph.

**Remark.**
With option --multi-language, yalafi.shell only replaces in text parts with
language according to option --language.

This German example replaces two words by a single one and vice versa:
```
so dass & sodass
nichtlineare & nicht lineare
nichtlineares & nicht lineares
```
Finally, please note the comment on
[dictionary adaptation](#dictionary-adaptation).

[Back to contents](#contents)


## Extension modules for LaTeX packages

The modules yalafi.documentclasses and yalafi.packages contain further
submodules that are activated by the LaTeX filter when executing
\\documentclass or \\usepackage, and on other occasions.

- Options `--pack mods` (yalafi) and `--packages mods` (yalafi.shell)<br>
  They expect a comma-separated list of package names or placeholders
  (default: '\*').
  For a name not starting with '.', the submodule is loaded from
  yalafi.packages (variable 'Parameters.package\_modules' in file
  yalafi/parameters.py).
  Otherwise, the leading '.' is removed, and the module is loaded from
  the current directory or a directory in PYTHONPATH.
  This allows inclusion of project-specific modules.
  File yalafi/packages/\_\_init\_\_.py contains lists of modules to
  be loaded for placeholders like '\*'.
- Options `--dcls cls` (yalafi) and `--documentclass cls` (yalafi.shell)<br>
  This is similar to --pack and --packages (default: '').
  The submodule is loaded from yalafi.documentclasses (variable
  'Parameters.class\_modules'), if 'cls' does not start with '.'.
- See also option `--add-modules file` in section
  [Example application](#example-application).
- Side-effect of options `--defs file` (yalafi)
  and `--define file` (yalafi.shell)<br>
  If the given file invokes \\documentclass or \\usepackage, then the
  corresponding modules are loaded.
- Side-effect of executing macro `\LTinput{file}`<br>
  This is similar to the previous case.

Each extension module has to provide a list 'require\_packages' of strings
that causes loading of other modules, and a function 'init\_module()'.
It is called by the parser and can modify the object of class 'Parameters'.
In order to add macros and environments, it has to construct strings or
object lists that are included in the returned object of class 'InitModule'.
Classes for definition of macros and environments are described in the
sections starting at [Definition of macros](#definition-of-macros).
For an example, see file
[yalafi/packages/amsmath.py](yalafi/packages/amsmath.py).

[Back to contents](#contents)


## Inclusion of own macros

Unknown macros and environment frames are silently ignored.
As all input files are processed independently, it may be necessary to
provide project-specific definitions in advance.

For macros, which may be declared with \\newcommand or \\def (the latter is
only roughly approximated), you can apply `\LTinput{file.tex}` as a simple
solution.
This adds the macros defined in the given file, skipping all other content.
For the “real” LaTeX, macro \\LTinput has to be defined as
`\newcommand{\LTinput}[1]{}` that is in turn ignored by the filter.

If LaTeX files have to stay untouched, you can use options
--defs and --define for yalafi and yalafi.shell, respectively.
Alternatively, one can add the definitions to member
'Parameters.macro\_defs\_latex' in file yalafi/parameters.py.
Here are examples from this file and extension module
yalafi/packages/xcolor.py:
```
        \newcommand{\quad}{\;}
        \newcommand{\textasciicircum}{\verb?^?} % \^ is accent
---
        \newcommand{\textcolor}[3][]{#3}
```

More complicated macros as well as environments have to be registered
with Python code.
This may be done with options --pack and --packages for yalafi and
yalafi.shell, respectively;
compare section
[Extension modules for LaTeX packages](#extension-modules-for-latex-packages).
Alternatively, you can modify the collections
'Parameters.macro\_defs\_python' and 'Parameters.environment\_defs'
in yalafi/parameters.py.

### Definition of macros

`Macro(parms, name, args='', repl='', defaults=[], extract='')`

- `parms`: current object of type Parameters
- `name`: macro name with '\\'
- `args`: string that codes the argument sequence
    - 'A': mandatory argument, may be a single token or a sequence
      enclosed in {} braces
    - 'O': optional argument in \[\] brackets
    - '\*': optional asterisk
- `repl`: replacement string as for \\newcommand ('\*' does count as argument),
  or a function (see point [Macro handler functions](#macro-handler-functions)
  below)
- `defaults`: an optional list of replacement strings for absent optional
  arguments
- `extract`: like `repl`, but the resulting text is appended to the main
  text, separated by blank lines; for an example, see declaration of macro
  \\footnote in 'Parameters.macro\_defs\_python' in yalafi/parameters.py

### Definition of environments

`Environ(parms, name, args='', repl='', defaults=[], remove=False, add_pars=True, items=None, end_func=None)`

Parameters `parms` to `defaults` are the same as for `Macro()`, where
`name` does not start with a backslash.
The arguments are those behind the opening '\\begin{xyz}'.
This means that the environment name 'xyz' does not yet count as argument
in `args` and `repl`.

- `remove`: if True, then the complete environment body is skipped;
  a fixed replacement can be given in `repl`
- `add_pars`: if True, then paragraph breaks (blank lines) are generated
  before and behind the environment body
- `items`: for inclusion of specific \\item labels;
  a generator taking a nesting level argument has to be specified;
  compare declaration of environment enumerate in yalafi/parameters.py
- `end_func`: optional function to be called at \\end{...};
  for an example, see file yalafi/packages/babel.py

### Definition of equation environments

`EquEnv(parms, name, args='', repl='', defaults=[], remove=False)`

This is equivalent to `Environ()`, but maths material is replaced according to
section
[Handling of displayed equations](#handling-of-displayed-equations).
Replacements in `repl` and `defaults` are still interpreted in text mode.

- `remove`: if True, then a fixed replacement can be specified in `repl`,
and trailing interpunction given by 'Parameters.math\_punctuation' in
file yalafi/parameters.py is appended

### Macro handler functions

Parameter `repl` of class `Macro` may specify a function with the following
arguments.

`handler(parser, buf, mac, args, delim, pos)`

It has to return a possibly empty list of tokens that are used as result of
the macro expansion.
The list may include tokens of class `VoidToken` (see argument `args`).
- `parser`: The active parser object.
  For instance, member `parser.parms` is the current `Parameter` object from
  file [yalafi/parameters.py](yalafi/parameters.py).
- `buf`: The token buffer we are reading from.
  The macro token, subsequent space, and all declared macro arguments already
  have been read.
  For instance, you can check the next token with `buf.cur()`;
  see file [yalafi/packages/xspace.py](yalafi/packages/xspace.py) for an
  application.
- `mac`: The object created with `Macro()`.
- `args`: A list of token lists.
  For each argument declared with `Macro()`, a possibly empty token list is
  passed.
  - `'*'`: If the asterisk was present, the token is given.
    Otherwise, the list is empty.
  - `'A'`: The argument tokens are given, excluding possibly surrounding curly
    braces.
    If the argument was empty (pure \{\}, paragraph break, or end of group or
    text), the list consists of a single `VoidToken`.
  - `'O'`: If the optional argument has not been specified, the list is empty.
    Otherwise, the tokens excluding the surrounding square brackets are given.
    If the option was a pure \[\], the list consists of a single `VoidToken`.
- `delim`: A list of booleans, indicating the presence of delimiters around the
  arguments.
  - `'*'`: Always False.
  - `'A'`: True, if the argument has been delimited by curly braces.
  - `'O'`: True, if the argument is present.
- `pos`: Character position of the leading backslash of the macro invocation,
  counting from zero.

For examples, see file [yalafi/handlers.py](yalafi/handlers.py).

[Back to contents](#contents)


## Multi-file projects

Here, we present one of several possibilities to cope with multiple files.
The main point is that the base LaTeX filter currently cannot directly
follow file inclusions like \\input{...}.
Assume you have the following file main.tex.
```
% (load document class and packages)
% possibly: load own macro definitions etc.
\input{defs.tex}
% the previous command is ignored by the filter, thus:
\LTinput{defs.tex}
\begin{document}
Test text.
\input{ch1/intro.tex}
\end{document}
```
Please provide the definition of \\LTinput as in section
[Adaptation of LaTeX and plain text](#adaptation-of-latex-and-plain-text).

In order to check the “normal text” only in file main.tex, you say
```
python -m yalafi.shell [...] --packages "" main.tex
```
Macros like \\input are ignored, in this case.
With the optional '--packages ""', default loading of all packages known
to the filter is suppressed.

The check of file ch1/intro.tex may look like
```
python -m yalafi.shell [...] --packages "" --define main.tex ch1/intro.tex
```
Option '--define main.tex' ensures that all settings and definitions from
file main.tex are available.
“Normal text” from that file is ignored.
Alternatively, you can add '\\LTinput{main.tex}' at the beginning of
file ch1/intro.tex.

A recursive check of all files is initiated by
```
python -m yalafi.shell [...] --packages "" --include --define main.tex main.tex
```
During a first phase, all file names are collected by evaluation of \\include,
\\input, \\subfile and \\subfileinclude commands.
Then, each file is processed on its own.
If you want to exclude certain files, for instance figures given in TeX code,
you can use option --skip from section
[Example application](#example-application).

**Remark.**
An alternative version is as follows.
Write all commands that YaLafi needs in an own file, say yy-defs.tex.
Then use option '--define yy-defs.tex', or place '\\LTinput{yy-defs.tex}' in
all sources.

[Back to contents](#contents)


## Handling of displayed equations

Displayed equations should be part of the text flow and include the
necessary interpunction.
The German version of
[LanguageTool](https://www.languagetool.org) (LT)
will detect a missing dot in the following snippet.
For English texts, see the comments in section
[Equation replacements in English documents](#equation-replacements-in-english-documents)
ahead.
```
Wir folgern
\begin{align}
    a   &= b \\
    c   &= d
\end{align}
Daher ...
```
Here, 'a' to 'd' stand for arbitrary mathematical
terms (meaning: “We conclude \<maths\> Therefore, ...”).
In fact, LT complains about the capital “Daher” that should start a
new sentence.

### Trivial version

With the entry
```
    Environ(self, 'align', remove=True, add_pars=False),
```
in list 'environments' of file
[yalafi/packages/amsmath.py](yalafi/packages/amsmath.py),
the equation environment is simply removed.
We get the following filter output that will probably cause a problem,
even if the equation itself ends with a correct interpunction sign.
```
Wir folgern
Daher ...
```

### Simple version

With the entry
```
    EquEnv(self, 'align', repl='  Relation', remove=True),
```
in 'Parameters.environment\_defs', one gets:
```
Wir folgern
  Relation
Daher ...
```
Adding a dot '= d.' in the equation will lead to 'Relation.' in the output.
This will also hold true, if the interpunction sign
('Parameters.math\_punctuation') is followed by maths space or by macros
as \\label and \\nonumber.

### Full version

**Remark.**
Our equation parsing currently assumes that aligned operators like '=' and '+'
are placed on the right side of the alignment character '\&'.
LaTeX does not enforce that, but it is the style found in examples of the
documentation for package amsmath.

**Remark.**
For a simplification, see option --simple-equations in section
[Example application](#example-application).

With the default entry
```
    EquEnv(self, 'align'),
```
we obtain (“gleich” means equal, and setting language to English will
produce “equal”):
```
Wir folgern
  V-V-V  gleich W-W-W
  W-W-W  gleich X-X-X.
Daher ...
```
The replacements like 'V-V-V' are taken from collections
'math\_repl\_display\*' in file yalafi/parameters.py that depend on
language setting, too.
Now, LT will additionally complain about repetition of 'W-W-W'.
Finally, writing '= b,' and '= d.' in the equation leads to the output:
```
Wir folgern
  V-V-V  gleich W-W-W,
  X-X-X  gleich Y-Y-Y.
Daher ...
```
The rules for equation parsing are described in section
[Parser for maths material](#parser-for-maths-material).
They ensure that variations like
```
    a   &= b \\
        &= c.
```
and
```
    a   &= b \\
        &\qquad -c.
```
also will work properly.
In contrast, the text
```
    a   &= b \\
    -c  &= d.
```
will again produce an LT warning due to the missing comma after 'b',
since the filter replaces both 'b' and '-c' by 'W-W-W' without
intermediate text.

In rare cases, manipulation with \\LTadd{...} or \\LTskip{...} may be
necessary to avoid false warnings from the proofreader; compare section
[Adaptation of LaTeX and plain text](#adaptation-of-latex-and-plain-text).

### Inclusion of “normal” text

In variant “Full version”, the argument of \\mbox (macro names: collection
'Parameters.math\_text\_macros', loading of LaTeX package amsmath adds \\text)
is directly copied.
Outside of \\mbox etc., only maths space like \\; and \\quad
(see 'Parameters.math\_space') is considered as space.
Therefore, one will get warnings from the proofreading program, if subsequent
\\text and maths parts are not properly separated.

### Equation replacements in English documents

The replacement collections 'math\_repl\_display\*' in file
yalafi/parameters.py do not work well, if single letters are taken as
replacements.
For instance, 'V.' cannot be safely considered as end of a sentence.
We now have chosen replacements as 'U-U-U' for German and English texts.

Furthermore, the English version of LanguageTool (like other proofreading
tools) rarely detects mistakenly capital words inside of a sentence;
they are probably considered as proper names.
Therefore, a missing dot at the end of a displayed equation is hardly found.
An experimental hack is provided by option --equation-punctuation of
application script [yalafi/shell/shell.py](yalafi/shell/shell.py)
described in section
[Example application](#example-application).

[Back to contents](#contents)


## Multi-language documents

**Remarks.**
This feature is experimental, any comments are welcome.
Operation may be slow, unless a LanguageTool server is used, for instance,
via option '--server my'.

As an example, assume option '--multi-language' for yalafi.shell and the LaTeX
text:
```
\documentclass{article}
\usepackage[german,english]{babel}
\newcommand{\german}[1]{\textit{\foreignlanguage{german}{#1}}}

\begin{document}
This is thex German word \german{excellent}..
\end{document}
```
Then, the Vim example from section [“Plain Vim”](#plain-vim)
with setting `let g:ltyc_showsuggestions = 1` will produce this quickfix
window:
```
t.tex|6 col 9 info|  Possible spelling mistake found. Suggestion: the; then; they; them; thee; Theo; hex; THX; TeX; Tex; The; t hex; the x; Théo
t.tex|6 col 34 info|  Möglicher Tippfehler gefunden. Suggestion: exzellent; exzellente; exzellenten; exzellenter; Exzellenz; exzellentes; erzählend; exzellentem; erhellend; erkältend; exzelliert
t.tex|6 col 44 info|  Two consecutive dots Suggestion: .; …
```
The initial language is specified by option --language, it is overwritten
upon `\usepackage[...]{babel}`.
Commands like `\selectlanguage{...}` are also effective in files loaded via
option --define or with `\LTinput{...}`.
Language names in babel commands are mapped to xx-XX codes by dictionary
'language\_map' in file [yalafi/packages/babel.py](yalafi/packages/babel.py).

**Further options.**
In the above example, LanguageTool is invoked for
'This is thex German word L-L-L..' with language en-GB, and for 'excellent'
with language de-DE.
The following options for yalafi.shell can be used to adjust the behaviour.

- `--ml-continue-threshold num`<br>
  If a short inclusion, for instance via \\foreignlanguage, does not comprise
  more than `num` plain-text words (default: 2), then the main text flow is
  continued.
  The inclusion is represented by a placeholder from collections
  'lang\_change\_repl\*' in file yalafi/parameters.py.
  Language changes with \\selectlanguage always break the text flow.
- `--ml-rule-threshold num`<br>
  If an inserted foreign-language text part consists of at most `num` words
  (default: 2), then options --ml-disable and --ml-disablecategories become
  effective for this text part.
- `--ml-disable rules`<br>
  Additionally disable these LanguageTool rules for text parts matching option
  --ml-rule-threshold (default: '').
  For example, one might disable rule UPPERCASE\_SENTENCE\_START.
- `--ml-disablecategories cats`<br>
  Similar to --ml-disable for LanguageTool's rule categories (default: '').

Please consider also the tweaks in section
[Adaptation of LaTeX and plain text](#adaptation-of-latex-and-plain-text).

[Back to contents](#contents)


## Python package interface

We comment the central function in file
[yalafi/tex2txt.py](yalafi/tex2txt.py)
that uses the package interface to emulate the behaviour of
script tex2txt.py in repository
[Tex2txt](https://github.com/matze-dd/Tex2txt).
```
 1  def tex2txt(latex, opts, multi_language=False, modify_parms=None):
 2      def read(file):
 3          try:
 4              with open(file, encoding=opts.ienc) as f:
 5                  return True, f.read()
 6          except:
 7              return False, ''
 8
 9      parms = parameters.Parameters(opts.lang or '')
10      parms.multi_language = multi_language
11      packages = get_packages(opts.dcls, parms.class_modules)
12      packages.extend(get_packages(opts.pack, parms.package_modules))
13
14      if opts.extr:
15          extr = ['\\' + s for s in opts.extr.split(',')]
16      else:
17          extr = []
18      if opts.seqs:
19          parms.math_displayed_simple = True
20
21      if modify_parms:
22          modify_parms(parms)
23      p = parser.Parser(parms, packages, read_macros=read)
24      toks = p.parse(latex, define=opts.defs, extract=extr)
25
26      if not multi_language:
27          txt, pos = utils.get_txt_pos(toks)
28      if opts.repl:
29          txt, pos = utils.replace_phrases(txt, pos, opts.repl)
30      if opts.unkn:
31          txt = '\n'.join(p.get_unknowns()) + '\n'
32          pos = [0 for n in range(len(txt))]
33      pos = [n + 1 for n in pos]
34      return txt, pos
35
36  main_lang = opts.lang or ''
37  ml = utils.get_txt_pos_ml(toks, main_lang, parms)
38  if opts.repl and main_lang in ml:
39      for part in ml[main_lang]:
40          part[0], part[1] = utils.replace_phrases(part[0], part[1],
41                                                      opts.repl)
42  for lang in ml:
43      for part in ml[lang]:
44          part[1]= list(n + 1 for n in part[1])
45  return ml
```
- 2-7: This is an auxiliary function for the parser.
- 9: The created parameter object contains all default settings
  and definitions from file yalafi/parameters.py.
- 11: We read the LaTeX packages from option --pack and convert them to 
  a list of handler functions called later by the parser.
- 14-17: If option --extr requests only extraction of arguments of certain
  macros, this is prepared.
- 22: If call-back modify\_parms is specified, it may change the parameters.
- 23: We create a parser object, the passed function is called on \\LTinput.
- 24: The parsing method returns a list of tokens.
- 27: The token list is converted into a 2-tuple containing the plain-text
  string and a list of numbers.
  Each number in the list indicates the estimated position of the
  corresponding character in the text string.
- 29: If phrase replacements are requested by option --repl, this is done.
  String opts.repl contains the replacement specifications read from the file.
- 31: On option --unkn, a list of unknown macros and environments is
  generated.
- 33: This is necessary, since position numbers are zero-based in yalafi,
  but one-based in Tex2txt/tex2txt.py.
- 37: For a multi-language document, utils.get\_txt\_pos\_ml() returns a
  dictionary, containing plain-text strings and character position maps for
  each language.
- 38: Phrase replacements are performed for text parts written in the main
  language.
- 44: This corresponds to line 33.

[Back to contents](#contents)


## Command-line of pure filter

The LaTeX filter can be integrated in shell scripts, compare the examples in
[Tex2txt/README.md](https://github.com/matze-dd/Tex2txt#tool-integration).

```
python -m yalafi [--nums file] [--repl file] [--defs file] [--dcls class]
                 [--pack modules] [--extr macros] [--lang xy] [--ienc enc]
                 [--seqs] [--unkn] [--nosp] [--mula base] [latexfile]
```
Without positional argument `latexfile`, standard input is read.

- `--nums file`<br>
  File for storing estimated original position numbers for each character
  of plain text.
  This can be used later to correct position figures in proofreader messages.
- `--repl file`<br>
  As option --replace in section [Example application](#example-application).
- `--defs file`<br>
  As option --define in section [Example application](#example-application).
- `--dcls class` and `--pack modules`<br>
  As options --documentclass and --packages in section
  [Example application](#example-application).
- `--extr ma[,mb,...]`<br>
  As option --extract in section [Example application](#example-application).
- `--lang xy`<br>
  Language 'de', 'en' or 'ru' (default: 'en', also taken in case of unknown
  language).
  Is used for adaptation of equation replacements, maths operator names,
  proof titles, and for handling of macros like '\"\='.
- `--ienc enc`<br>
  As option --encoding in section [Example application](#example-application).
- `--seqs`<br>
  As option --simple-equations in section
  [Example application](#example-application).
- `--unkn`<br>
  As option --list-unknown in section
  [Example application](#example-application).
- `--nosp`<br>
  As option --no-specials in section
  [Example application](#example-application).
- `--mula base`<br>
  Turn on multi-language processing.
  The different text parts are stored in files `<base>.<part>.<language>`.
  If --nums has been specified, the position maps are written to files with
  similar naming scheme.

[Back to contents](#contents)


## Differences to Tex2txt

Invocation of `python -m yalafi ...` differs as follows from
`python tex2txt.py ...` (the script described in
[Tex2txt/README.md](https://github.com/matze-dd/Tex2txt#command-line)).

- Macro definitions with \\(re)newcommand in the LaTeX input are processed,
  as well as \\documentclass and \\usepackage.
- Macro arguments need not be delimited by {} braces or \[\] brackets.
- Macros are expanded in the order they appear in the text.
- Character position tracking for displayed equations is improved,
  see [the example below](#equation-html-report).
- Added options --dcls and --pack allow modification of predefined LaTeX
  macros and environments at Python level.
- Added option --seqs.
- Added option --nosp.
- Added option --mula.
- Option --defs expects a file containing macro definitions as LaTeX code.
- Option --ienc is also effective for file from --defs.
- Option --char (position tracking for single characters) is always activated.
- Default language is English. It is also used for an unknown language.

YaLafi/yalafi/tex2txt.py is faster for input texts till about 30 Kilobytes,
for larger files it can be slower than 'Tex2txt/tex2txt.py --char'.
Run-time increases quasi linearly with file size.
Due to token generation for each single “normal” character, memory usage
may be substantial for long input texts.

<a name="equation-html-report"></a>
With
```
python -m yalafi.shell --equation-punct all --output html test.tex > test.html
```
and input 
```
For each $\epsilon > 0$, there is a $\delta > 0$ so that
%
\begin{equation}
\norm{y-x} < \delta \text{\quad implies\quad}
    \norm{A(y) - A(x)} < \epsilon, \label{lab}
\end{equation}
%
Therefore, operator $A$ is continuous at point $x$.
```
we get

![HTML report](figs/example-equation.png)


[Back to contents](#contents)


## Remarks on implementation

### Scanner / tokeniser

The scanner identifies token types defined in yalafi/defs.py.

- All “normal” characters yield an own token.
- Many character combinations like '{', '\\\[' or '---' are recognised
  as “special tokens”.
- Names of “normal” macros formed by a backslash and subsequent letters
  (method 'Parameters.macro\_character()') result in a token, macros
  '\\begin', '\\end', '\\item', and '\\verb' are treated separately.
- For space, we distinguish between character sequences that do or do not
  represent a paragraph break.
  In both cases, a single token is generated.
- Comments starting with '%' consume the rest of the line and leading space
  on the next line, if it is not blank.
  A single token is generated.

### Parser

The central method 'Parser.expand\_sequence()' does not directly read from
the scanner, but from an intermediate buffer that can take back tokens.
On macro expansion, the parser simply pushes back all tokens generated by
argument substitution.
(Method 'Parser.expand\_arguments()' collects tokens forming macro arguments
and returns a list of replacement tokens that is eventually pushed back
in the main loop.)
The result is close to the “real” TeX behaviour, compare the tests in
directory tests/.

A method important for simple implementation is 'Parser.arg\_buffer()'.
It creates a new buffer that subsequently returns tokens forming a macro
argument (only a single token or all tokens enclosed in paired {} braces
or \[\] brackets).

### Parser for maths material

We follow the ideas described in section
[Handling of displayed equations](#handling-of-displayed-equations),
compare the tests in [tests/test\_display.py](tests/test_display.py).
All unknown macros, which are not in the blacklist 'Parameters.math\_ignore',
are assumed to generate some “visible” output.
Thus, it is not necessary to declare all the maths macros like \\alpha
and \\sum.

Displayed equations are parsed as follows.

- Equation environments are split into “lines” separated by '\\\\'.
- Each “line” is split into “sections” delimited by '\&'.
- Each “section” is split into “maths parts” only consisting of maths
  material separated by intermediate \\text{...} or \\mbox{...}
  ('Parameters.math\_text\_macros').
- Arguments of \\text and \\mbox are directly copied.
- A “maths part” is substituted with a placeholder from rotating collections
  'math\_repl\_display\*', if it does not consist only of punctuation
  marks from 'Parameters.math\_punctuation' or of operators from
  'Parameters.math\_operators'.
- A leading maths operator is displayed using 'math\_op\_text'
  (language-dependent), if the “maths part” is first in “section” and
  the “section” is not first on “line”.
- Trailing interpunction of a “maths part” is appended to the placeholder.
- If the “maths part” includes leading or trailing maths space from
  'Parameters.math\_space', then white space is prepended or appended to the
  replacement.
- Replacements from 'math\_repl\_display\*' are rotated
    - if a non-blank \\text part is detected,
    - if a “maths part” starts with an operator and is first in “section”,
      but not on “line”,
    - if a “maths part” only consists of an operator,
    - if a “maths part” includes trailing interpunction.

### Removal of unnecessary blank lines

In order to avoid creation of new blank lines by macros expanding to space or
“nothing”, we include a token of type 'ActionToken' whenever
expanding a macro.
Method 'Parser.remove\_pure\_action\_lines()' removes all lines only
containing space and at least one such token.
Initially empty lines are retained.
Together with the extraction of special text flows, for instance from
footnotes, this preserves sentences and paragraphs, thus improving checks
and reducing false positives from the proofreading software.

[Back to contents](#contents)

