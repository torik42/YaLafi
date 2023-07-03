.. note::

    This part is just copied from the old documentation. Some links may not work. It is also not complete or coherent since we remove parts after merging into the new documentation.

Remaining Old Documentation
===========================

**Notice.** The library of LaTeX macros, environments, document classes,
and packages is still rather restricted, compare the `list of
macros <list-of-macros.md>`__. Please don’t hesitate to `raise an
Issue <../../issues>`__, if you would like to have added something.

If you want to add something yourself, have a look at `Inclusion of own
macros <#inclusion-of-own-macros>`__ and
`CONTRIBUTING.md <./CONTRIBUTING.md>`__.

**Summary.** This Python package extracts plain text from LaTeX
documents. The software may be integrated with a proofreading tool and
an editor. It provides - mapping of character positions between LaTeX
and plain text, - simple inclusion of own LaTeX macros and environments
with tailored treatment, - careful conservation of text flows, - some
parsing of displayed equations for detection of included “normal” text
and of interpunction problems, - support of multi-language documents
(experimental).

The sample Python application ``yalafi.shell`` from section `Example
application <#example-application>`__ integrates the LaTeX filter with
the proofreading software
`LanguageTool <https://www.languagetool.org>`__. It sends the extracted
plain text to the proofreader, maps position information in returned
messages back to the LaTeX text, and generates results in different
formats. You may easily - create a proofreading report in text or HTML
format for a complete document tree, - check LaTeX texts in the editors
Vim, Emacs and Atom via several plugins, - run the script as emulation
of a LanguageTool server with integrated LaTeX filtering.

For instance, the LaTeX input

::

    Only few people\footnote{We use
    \textcolor{red}{redx colour.}}
    is lazy.

will lead to the text report

::

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

This is the corresponding HTML report (for an example with a Vim
plugin, `see here <#example-vimtex-plugin>`__):

.. figure:: _static/figs/shell.png
   :alt: HTML report

   HTML report

The tool builds on results from project
`Tex2txt <https://github.com/matze-dd/Tex2txt>`__, but differs in the
internal processing method. Instead of using recursive regular
expressions, a simple tokeniser and a small machinery for macro
expansion are implemented; see sections `Differences to
Tex2txt <#differences-to-tex2txt>`__ and `Remarks on
implementation <#remarks-on-implementation>`__.

Beside the interface from section `Python package
interface <#python-package-interface>`__, application Python scripts
like ```yalafi/shell/shell.py`` <yalafi/shell/shell.py>`__ from section
`Example application <#example-application>`__ can access an interface
emulating ``tex2txt.py`` from repository
`Tex2txt <https://github.com/matze-dd/Tex2txt>`__ by
``from yalafi import tex2txt``. The pure LaTeX filter can be directly
used in scripts via a command-line interface, it is described in section
`Command-line of pure filter <#command-line-of-pure-filter>`__.

If you use this software and encounter a bug or have other suggestions
for improvement, please leave a note under category
`Issues <../../issues>`__, or initiate a pull request. Many thanks in
advance.

Happy TeXing!

Contents
--------

`Authors and Maintainers <#authors-and-maintainers>`__\  `Example
application <#example-application>`__\  `Interfaces to
Vim <#interfaces-to-vim>`__\  `Interface to
Emacs <#interface-to-emacs>`__\  `Interface to
Atom <#interface-to-atom>`__\  `Usage under
Windows <#usage-under-windows>`__\  `Related
projects <#related-projects>`__\  `Filter actions <#filter-actions>`__\ 
`Fundamental limitations <#fundamental-limitations>`__\  `Adaptation of
LaTeX and plain text <#adaptation-of-latex-and-plain-text>`__\ 
`Extension modules for LaTeX
packages <#extension-modules-for-latex-packages>`__\  `Inclusion of own
macros <#inclusion-of-own-macros>`__\  `Multi-file
projects <#multi-file-projects>`__\  `Handling of displayed
equations <#handling-of-displayed-equations>`__\  `Multi-language
documents <#multi-language-documents>`__\  `Python package
interface <#python-package-interface>`__\  `Command-line of pure
filter <#command-line-of-pure-filter>`__\  `Differences to
Tex2txt <#differences-to-tex2txt>`__\  `Remarks on
implementation <#remarks-on-implementation>`__

Authors and Maintainers
-----------------------

-  `matze-dd <https://github.com/matze-dd>`__ (author till `version
   1.3.1 <https://github.com/matze-dd/YaLafi-1.3.1>`__ in 2022)
-  `torik42 <https://github.com/torik42>`__ (maintainer since 2022)

Example application
-------------------

**Remark.** You can find examples for tool integration with Bash scripts
in
`Tex2txt/README.md <https://github.com/matze-dd/Tex2txt#tool-integration>`__.

**HTML report.** The idea of an HTML report goes back to Sylvain Hallé,
who developed `TeXtidote <https://github.com/sylvainhalle/textidote>`__.
Opened in a Web browser, the report displays excerpts from the original
LaTeX text, highlighting the problems indicated by LT. The corresponding
LT messages can be viewed when hovering the mouse over these marked
places, see the `introductory example <#example-html-report>`__ above.
With option ``--link``, Web links provided by LT can be directly opened
with left-click. Script option ``--context`` controls the number of
lines displayed around each tagged region; a negative option value will
show the complete LaTeX input text. If the localisation of a problem is
unsure, highlighting will use yellow instead of orange colour. For
simplicity, marked text regions that intertwine with other ones are
separately repeated at the end. In case of multiple input files, the
HTML report starts with an index.

`Back to contents <#contents>`__

Interface to Vim
----------------

.. note::

    first part already copied

-  Function key ``F9`` saves the file, starts the compiler, and opens
   the quick fix window.
-  Uncomment the line with ``g:vimtex_grammar_vlty.lt_command``, if
   LanguageTool has been installed by variant 2 in section
   `Installation <#installation>`__. In this case, specification of
   ``g:vimtex_grammar_vlty.lt_directory`` is not necessary.
-  The option ``g:vimtex_grammar_vlty.server = 'my'`` usually results in
   faster checks for small to medium LaTeX files. Start-up time is
   saved, and speed benefits from the internal sentence caching of the
   server.
-  Saying ``let g:vimtex_grammar_vlty.show_suggestions = 1`` causes
   display of LanguageTool’s replacement suggestions.
-  With option ``--multi-language``, commands from LaTeX package
   ``babel`` switch the language for the proofreading program. See
   section `Multi-language documents <#multi-language-documents>`__.
-  By default, the vlty compiler passes names of all necessary LaTeX
   packages to YaLafi, which may result in annoying warnings. In
   multi-file projects, these are suppressed by ``--packages "*"`` that
   simply loads all packages known to the filter.
-  YaLafi’s expansion of project-specific macros can be controlled via
   option ``--define ...``. Example for ``defs.tex`` (Note that the
   first three lines are only necessary, if the currently edited file
   does not directly contain these definitions.):

   ::

       \newcommand{\zB}{z.\,B. }   % LanguageTool correctly insists on
                                   % narrow space in this German abbreviation
       \newtheorem{Satz}{Satz}     % correctly expand \begin{Satz}[siehe ...]
       \LTinput{main.glsdefs}      % read database of glossaries package

-  Replacement of phrases may be performed via ``--replace ...``,
   compare section `Phrase replacement in the plain
   text <#phrase-replacement-in-the-plain-text>`__.
-  Option ``--equation-punctuation display`` enables some additional
   interpunction checking for displayed equations in English texts, see
   section `Example application <#example-application>`__ and `this
   example <#equation-html-report>`__.
-  Option ``--single-letters ...`` activates search for isolated single
   letters. Note that only the ``|`` signs need to be escaped here;
   compare section `Example application <#example-application>`__.

 Here is the `introductory example <#example-html-report>`__ from above:

.. figure:: _static/figs/vim-vimtex.png
   :alt: Vim plugin vim-vimtex

   Vim plugin vim-vimtex

“Plain Vim”
~~~~~~~~~~~

File ```editors/ltyc.vim`` <editors/ltyc.vim>`__ proposes a simple
application to Vim’s compiler interface. The file has to be copied to a
directory like ``~/.vim/compiler/``.

For a Vim session, the component is activated with ``:compiler ltyc``.
Command ``:make`` invokes yalafi.shell, and the cursor is set to the
first indicated problem. The related error message is displayed in the
status line. Navigation between errors is possible with ``:cn`` and
``:cp``, an error list is shown with ``:cl``. The quick fix window
appears on ``:cw``.

The following snippet demonstrates a basic vimrc setting and some useful
values for option ``ltyc_shelloptions``. Please refer to section `Plugin
vimtex <#plugin-vimtex>`__ for related comments.

::

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

The screenshot resembles that from section `Plugin
vimtex <#plugin-vimtex>`__.

Plugin vim-grammarous
~~~~~~~~~~~~~~~~~~~~~

For the Vim plugin
`[vim-grammarous] <https://github.com/rhysd/vim-grammarous>`__, it is
possible to provide an interface for checking LaTeX texts. With an entry
in ``~/.vimrc, one may simply replace the command that`` invokes
LanguageTool. For instance, you can add to ``~/.vimrc``

::

    let g:grammarous#languagetool_cmd = '/home/foo/bin/yalafi-grammarous'
    map <F9> :GrammarousCheck --lang=en-GB<CR>

A proposal for Bash script /home/foo/bin/yalafi-grammarous (replace foo
with username ;-) is given in
`editors/yalafi-grammarous <editors/yalafi-grammarous>`__. It has to be
made executable with ``chmod +x ...``. Please adapt script variable
``ltdir``, compare option ``--lt-directory`` in section `Example
application <#example-application>`__. If you do not want to have
started a local LT server, comment out the line defining script variable
``use_server``.

In order to avoid the problem described in `Issue
#89@vim-grammarous <https://github.com/rhysd/vim-grammarous/issues/89>`__
(shifted error highlighting, if after non-ASCII character on same line),
you can set ``output=xml-b`` in yalafi-grammarous.

**Troubleshooting for Vim interface.** If Vim reports a problem with
running LT, you can do the following. In ``~/bin/yalafi-grammarous``,
comment out the final ``... 2>/dev/null``. For instance, you can just
place a ``#`` in front: ``... # 2>/dev/null``. Then start, with a test
file ``t.tex``,

::

    $ ~/bin/yalafi-grammarous t.tex

This should display some error message, if the problem goes back to
running the script, Python, yalafi.shell or LanguageTool.

Here is the `introductory example <#example-html-report>`__ from above:

.. figure:: _static/figs/vim-grammarous.png
   :alt: Vim plugin vim-grammarous

   Vim plugin vim-grammarous

Plugin vim-LanguageTool
~~~~~~~~~~~~~~~~~~~~~~~

The Vim plugin
`[vim-LanguageTool] <https://github.com/dpelle/vim-LanguageTool>`__
relies on the same XML interface to LanguageTool as the variant in
section `Plugin vim-grammarous <#plugin-vim-grammarous>`__. Therefore,
one can reuse the Bash script
`editors/yalafi-grammarous <editors/yalafi-grammarous>`__. You can add
to ``~/.vimrc``

::

    let g:languagetool_cmd = '$HOME/bin/yalafi-grammarous'
    let g:languagetool_lang = 'en-GB'
    let g:languagetool_disable_rules = 'WHITESPACE_RULE'
    map <F9> :LanguageToolCheck<CR>

Please note the general problem indicated in `Issue
#17 <../../issues/17>`__. Here is again the `introductory
example <#example-html-report>`__ from above. Navigation between
highlighted text parts is possible with ``:lne`` and ``:lp``.

.. figure:: _static/figs/vim-languagetool.png
   :alt: Vim plugin vim-LanguageTool

   Vim plugin vim-LanguageTool

Plugin ALE
~~~~~~~~~~

With `[ALE] <https://github.com/dense-analysis/ale>`__, the proofreader
('linter') by default is invoked as background task, whenever one leaves
insert mode. You might add to ``~/.vimrc``

::

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
    " set to '' to disable server usage or to 'lt' for LT’s Web server
    let g:ale_tex_lty_server = 'my'
    " default language: 'en-GB'
    let g:ale_tex_lty_language = 'en-GB'
    " default disabled LT rules: 'WHITESPACE_RULE'
    let g:ale_tex_lty_disable = 'WHITESPACE_RULE'

Similarly to setting ``g:ale_tex_lty_disable``, one can specify LT’s
options ``--enable``, ``--disablecategories``, and
``--enablecategories``. Further options for yalafi.shell (compare
section `Plugin vimtex <#plugin-vimtex>`__) may be passed like

::

    let g:ale_tex_lty_shelloptions = '--single-letters "A|a|I|e.g.|i.e.||"'
                    \ . ' --equation-punctuation display'

Additionally, one has to install ALE and copy or link file
`editors/lty.vim <editors/lty.vim>`__ to directory
``~/.vim/bundle/ale/ale_linters/tex/``, or a similar location.

Here is again the `introductory example <#example-html-report>`__ from
above. The complete message for the error at the cursor is displayed on
``F9``, together with LT’s rule ID, replacement suggestions, and the
problem context (left with ``q``). Navigation between highlighted text
parts is possible with ``:lne`` and ``:lp``, an error list is shown with
``:lli``.

.. figure:: _static/figs/vim-ale.png
   :alt: Vim plugin ALE

   Vim plugin ALE

`Back to contents <#contents>`__

Interface to Emacs
------------------

The Emacs plugin
`[Emacs-langtool] <https://github.com/mhayashi1120/Emacs-langtool>`__
may be used in two variants. First, you can add to ``~/.emacs``

::

    (setq langtool-bin "/home/foo/bin/yalafi-emacs")
    (setq langtool-default-language "en-GB")
    (setq langtool-disabled-rules "WHITESPACE_RULE")
    (require 'langtool)

A proposal for Bash script ``/home/foo/bin/yalafi-emacs`` (replace
``foo`` with username ;-) is given in
`editors/yalafi-emacs <editors/yalafi-emacs>`__. It has to be made
executable with ``chmod +x ...``. Please adapt script variable
``ltdir``, compare option ``--lt-directory`` in section `Example
application <#example-application>`__. If you do not want to have
started a local LT server, comment out the line defining script variable
``use_server``.

**Troubleshooting for Emacs interface.** If Emacs reports a problem with
running LT, you can apply the steps from `[Troubleshooting for Vim
interface] <#troubleshooting-for-vim-interface>`__ to
``~/bin/yalafi-emacs``.

**Server interface.** This variant may result in better tracking of
character positions. In order to use it, you can 5write in ``~/.emacs``

::

    (setq langtool-http-server-host "localhost"
          langtool-http-server-port 8082)
    (setq langtool-default-language "en-GB")
    (setq langtool-disabled-rules "WHITESPACE_RULE")
    (require 'langtool)

and start yalafi.shell as server in another terminal with

::

    $ python -m yalafi.shell --as-server 8082 [--lt-directory /path/to/LT]

The server will print some progress messages and can be stopped with
``ctrl-C``. Further script arguments from section `Example
application <#example-application>`__ may be given. If you add, for
instance, ``--server my``, then a local LT server will be used. It is
started on the first HTML request received from Emacs-langtool, if it is
not yet running.

**Installation of Emacs-langtool.** Download and unzip Emacs-langtool.
Place file ``langtool.el`` in directory ``~/.emacs.d/lisp/.`` Set in
your ``~/.profile`` or ``~/.bash_profile`` (and log in again)

::

    export EMACSLOADPATH=~/.emacs.d/lisp:

Here is the `introductory example <#example-html-report>`__ from above:

.. figure:: _static/figs/emacs-langtool.png
   :alt: Emacs plugin Emacs-langtool

   Emacs plugin Emacs-langtool

`Back to contents <#contents>`__

Interface to Atom
-----------------

For the editor `[Atom] <https://atom.io>`__, you can use the plugin
`[linter-yalafi] <https://github.com/mfbehrens99/linter-yalafi>`__.
Please note that we have not yet tested this interface.

`Back to contents <#contents>`__

Usage under Windows
-------------------

Both yalafi.shell and yalafi can be directly used in a Windows command
script or console. For example, this could look like

::

    py -3 -m yalafi.shell --server lt --output html t.tex > t.html

or

::

    "c:\Program Files\Python\Python37\python.exe" -m yalafi.shell --server lt --output html t.tex > t.html

if the Python launcher has not been installed.

Files with Windows-style line endings (CRLF) are accepted, but the text
output of the pure LaTeX filter will be Unix style (LF only), unless a
Windows Python interpreter is used.

Python's version for Windows by default prints Latin-1 encoded text to
standard output. As this ensures proper work in a Windows command
console, we do not change it for yalafi.shell when generating a text
report. All other output is fixed to UTF-8 encoding.

`Back to contents <#contents>`__

Related projects
----------------

This project relates to software like

`OpenDetex <https://github.com/pkubowicz/opendetex>`__ \|
`pandoc <https://github.com/jgm/pandoc>`__ \|
`plasTeX <https://github.com/tiarno/plastex>`__ \|
`pylatexenc <https://github.com/phfaist/pylatexenc>`__ \|
`TeXtidote <https://github.com/sylvainhalle/textidote>`__ \|
`tex2txt <http://hackage.haskell.org/package/tex2txt>`__ \|
`vscode-ltex <https://github.com/valentjn/vscode-ltex>`__

From these examples, currently (March 2020) only TeXtidote and
vscode-ltex provide position mapping between the LaTeX input text and
the plain text that is sent to the proofreading software. Both use
(simple) regular expressions for plain-text extraction and are easy to
install. YaLafi, on the other hand, aims to achieve high flexibility and
a good filtering quality with minimal number of false positives from the
proofreading software.

`Back to contents <#contents>`__

Filter actions
--------------

Here is a list of the most important filter operations. When the filter
encounters a LaTeX problem like a missing end of equation, a message is
printed to ``stderr``. Additionally, the mark from
``Parameters.mark_latex_error`` in file ``yalafi/parameters.py`` is
included into the filter output. This mark should raise a spelling error
from the proofreader at the place where the problem was detected.

-  A collection of standard LaTeX macros and environments is already
   included, but very probably it has to be complemented. Compare
   variables ``Parameters.macro_defs_latex``,
   ``Parameters.macro_defs_python``, and ``Parameters.environment_defs``
   in file ``yalafi/parameters.py``.
-  The macros ``\documentclass`` and ``\usepackage`` load extension
   modules that define important macros and environments provided by the
   corresponding LaTeX packages. For other activation methods of these
   modules, see also section `Extension modules for LaTeX
   packages <#extension-modules-for-latex-packages>`__.
-  Macro definitions with ``\(re)newcommand`` and ``\def`` (the latter
   only roughly approximated) in the input text are processed. Statement
   ``\LTinput{file.tex}`` reads macro definitions from the given file.
   Further own macros with arbitrary arguments can be defined on Python
   level, see section `Inclusion of own
   macros <#inclusion-of-own-macros>`__.
-  Unknown macros are silently ignored, keeping their arguments with
   enclosing ``{}`` braces removed. They can be listed with options
   ``--unkn`` and ``--list-unknown`` for yalafi and yalafi.shell,
   respectively.
-  Environment frames ``\begin{...}`` and ``\end{...}`` are deleted. We
   implement tailored behaviour for environment types listed in
   ``Parameters.environment_defs`` in file ``yalafi/parameters.py``, see
   section `Inclusion of own macros <#inclusion-of-own-macros>`__. For
   instance, environment bodies can be removed or replaced by fixed
   text.
-  Text in heading macros as ``\section{...}`` is extracted with added
   interpunction, see variable ``Parameters.heading_punct`` in file
   ``yalafi/parameters.py``. This suppresses false positives from
   LanguageTool.
-  For macros as ``\ref``, ``\eqref``, ``\pageref``, and ``\cite``,
   suitable placeholders are inserted.
-  Arguments of macros like ``\footnote`` are appended to the main text,
   separated by blank lines. This preserves text flows.
-  Inline math material ``$...$`` and ``\(...\)`` is replaced with text
   from the rotating collections ``math_repl_inline*`` in file
   ``yalafi/parameters.py``. Trailing interpunction from
   ``Parameters.math_punctuation`` is appended.
-  Equation environments are resolved in a way suitable for check of
   interpunction and spacing. The argument of macros like ``\mbox`` and
   ``\text`` is included into the output text. Versions ``\[...\]`` and
   ``$$...$$`` are handled like environment displaymath. See also
   sections `Handling of displayed
   equations <#handling-of-displayed-equations>`__ and `Parser for maths
   material <#parser-for-maths-material>`__.
-  We generate numbered default ``\item`` labels for environment
   enumerate.
-  For ``\item`` with specified [...] label, some treatment is provided.
   If the text before ends with a punctuation mark from collection
   ``Parameters.item_punctuation`` in file ``yalafi/parameters.py``,
   then this mark is appended to the label. This works well for German
   texts, it is turned off with the setting ``item_punctuation = []``.
-  Letters with text-mode accents as '\\\`' or '\\v' are translated to
   the corresponding UTF-8 characters.
-  Things like double quotes `````` and dashes ``--`` are replaced with
   the corresponding UTF-8 characters. Additionally, we replace ``~``
   and ``\,`` by UTF-8 non-breaking space and narrow non-breaking space.
-  For language ``de``, suitable replacements for macros like ``"``` and
   ``"=`` are inserted, see method
   ``Parameters.init_parser_languages()`` in file
   ``yalafi/parameters.py``.
-  Macro ``\verb`` and environment ``verbatim`` are processed.
   Environment ``verbatim`` can be replaced or removed like other
   environments with an appropriate entry in
   ``Parameters.environment_defs`` in ``yalafi/parameters.py``.
-  Rare warnings from the proofreading program can be suppressed using
   ``\LTadd{...}``, ``\LTskip{...}``, ``\LTalter{...}{...}`` in the
   LaTeX text; compare section `Adaptation of LaTeX and plain
   text <#adaptation-of-latex-and-plain-text>`__.
-  Complete text sections, for instance parts of the LaTeX preamble, may
   be skipped with the special LaTeX comments ``%%% LT-SKIP-BEGIN`` and
   ``%%% LT-SKIP-END``; see section `Adaptation of LaTeX and plain
   text <#adaptation-of-latex-and-plain-text>`__.

`Back to contents <#contents>`__

Fundamental limitations
-----------------------

The implemented parsing mechanism can only roughly approximate the
behaviour of a real LaTeX system. We assume that only “reasonable”
macros are used, lower-level TeX operations are not supported. If
necessary, they should be enclosed in ``\LTskip{...}`` (see section
`Adaptation of LaTeX and plain
text <#adaptation-of-latex-and-plain-text>`__) or be placed in a LaTeX
file “hidden” for the filter (compare option ``--skip`` of yalafi.shell
in section `Example application <#example-application>`__). With little
additional work, it might be possible to include some plain-TeX features
like parsing of elastic length specifications. A list of remaining
incompatibilities must contain at least the following points.

-  Mathematical material is represented by simple replacements. As the
   main goal is application of a proofreading software, we have
   deliberately taken this approach.
-  Parsing does not cross file boundaries. Tracking of file inclusions
   is possible though.
-  Macros depending on (spacing) lengths may be treated incorrectly.
-  Character ``@`` always has category ``$1``. See `Issue
   #183 <../../issues/183>`__.

`Back to contents <#contents>`__

Adaptation of LaTeX and plain text
----------------------------------

In order to suppress unsuitable but annoying messages from the
proofreading tool, it is sometimes necessary to modify the input text.
You can do that in the LaTeX code, or after filtering in the plain text.

Modification of LaTeX text
~~~~~~~~~~~~~~~~~~~~~~~~~~

The following operations can be deactivated with options ``--nosp`` and
``--no-specials`` of yalafi and yalafi.shell, respectively. For
instance, macro ``\LTadd`` will be defined, but it will *not* add its
argument to the plain text.

**Special macros.** Small modifications, for instance concerning
interpunction, can be made with the predefined macros ``\LTadd``,
``\LTalter`` and ``\LTskip.`` In order to add a full stop for the
proofreader only, you would write

::

    ... some text\LTadd{.}

For LaTeX itself, the macros also have to be defined. A good place is
the document preamble. (For the last line, compare section `Inclusion of
own macros <#inclusion-of-own-macros>`__.)

::

    \newcommand{\LTadd}[1]{}
    \newcommand{\LTalter}[2]{#1}
    \newcommand{\LTskip}[1]{#1}
    \newcommand{\LTinput}[1]{}

The LaTeX filter will ignore these statements. In turn, it will include
the argument of ``\LTadd``, use the second argument of ``\LTalter``, and
neglect the argument of ``\LTskip.`` The macro names for ``\LTadd`` etc.
are defined by variables ``Parameters.macro_filter_add`` etc. in file
``yalafi/parameters.py``.

**Special comments.** Mainly the document preamble often contains
statements not properly processed “out-of-the-box”. Placing the critical
parts in ``\LTskip{...}`` may lead to problems, as the statements now
are executed slightly differently by the TeX system. As “brute-force”
variant, the LaTeX filter therefore ignores input enclosed in comments
starting with ``%%% LT-SKIP-BEGIN`` and ``%%% LT-SKIP-END``. Note that
the single space after ``%%%`` is significant. The opening special
comment is given in variable ``Parameters.comment_skip_begin`` of file
``yalafi/parameters.py``.

A preamble could look as follows.

::

    \documentclass{article}
    %%% LT-SKIP-BEGIN
    ... disturbing stuff ...
    %%% LT-SKIP-END
    \title{A paper}
    \begin{document}

Phrase replacement in the plain text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yalafi.shell and yalafi provide options ``--replace file`` and
``--repl file``, respectively. They may be valuable, if you often use a
phrase (possibly of multiple words) that is not accepted by the
proofreader. In the given file, a ``#`` sign marks the rest of the line
as comment. The first ``&`` separated by space splits a line into two
parts; the first part is replaced by the second one. Space in the first
part may correspond to arbitrary space in the plain text that does not
break the paragraph.

**Remark.** With option ``--multi-language``, yalafi.shell only replaces
in text parts with language according to option ``--language``.

This German example replaces two words by a single one and vice versa:

::

    so dass & sodass
    nichtlineare & nicht lineare
    nichtlineares & nicht lineares

Finally, please note the comment on `dictionary
adaptation <#dictionary-adaptation>`__.

`Back to contents <#contents>`__

Extension modules for LaTeX packages
------------------------------------

The modules yalafi.documentclasses and yalafi.packages contain further
submodules that are activated by the LaTeX filter when executing
``\documentclass`` or ``\usepackage``, and on other occasions.

-  Options ``--pack mods`` (yalafi) and ``--packages mods``
   (yalafi.shell) They expect a comma-separated list of package names or
   placeholders (default: ``*``). For a name not starting with ``.``,
   the submodule is loaded from yalafi.packages (variable
   ``Parameters.package_modules`` in file ``yalafi/parameters.py``).
   Otherwise, the leading ``.`` is removed, and the module is loaded
   from the current directory or a directory in ``PYTHONPATH``. This
   allows inclusion of project-specific modules. File
   ``yalafi/packages/__init__.py`` contains lists of modules to be
   loaded for placeholders like ``*``.
-  Options ``--dcls cls`` (yalafi) and ``--documentclass cls``
   (yalafi.shell) This is similar to ``--pack`` and ``--packages``
   (default: ''). The submodule is loaded from yalafi.documentclasses
   (variable ``Parameters.class_modules``), if ``cls`` does not start
   with ``.``.
-  See also option ``--add-modules file`` in section `Example
   application <#example-application>`__.
-  Side-effect of options ``--defs file`` (yalafi) and ``--define file``
   (yalafi.shell) If the given file invokes ``\documentclass`` or
   ``\usepackage``, then the corresponding modules are loaded.
-  Side-effect of executing macro ``\LTinput{file}``\  This is similar
   to the previous case.

Each extension module has to provide a list ``require_packages`` of
strings that causes loading of other modules, and a function
``init_module()``. It is called by the parser and can modify the object
of class ``Parameters``. In order to add macros and environments, it has
to construct strings or object lists that are included in the returned
object of class ``InitModule``. Classes for definition of macros and
environments are described in the sections starting at `Definition of
macros <#definition-of-macros>`__. For an example, see file
```yalafi/packages/amsmath.py`` <yalafi/packages/amsmath.py>`__.

`Back to contents <#contents>`__

Inclusion of own macros
-----------------------

Unknown macros and environment frames are silently ignored. As all input
files are processed independently, it may be necessary to provide
project-specific definitions in advance.

For macros, which may be declared with ``\newcommand`` or ``\def`` (the
latter is only roughly approximated), you can apply
``\LTinput{file.tex}`` as a simple solution. This adds the macros
defined in the given file, skipping all other content. For the “real”
LaTeX, macro ``\LTinput`` has to be defined as
``\newcommand{\LTinput}[1]{}`` that is in turn ignored by the filter.

If LaTeX files have to stay untouched, you can use options ``--defs``
and ``--define`` for yalafi and yalafi.shell, respectively.
Alternatively, one can add the definitions to member
``Parameters.macro_defs_latex`` in file ``yalafi/parameters.py``. Here
are examples from this file and extension module
``yalafi/packages/xcolor.py``:

::

            \newcommand{\quad}{\;}
            \newcommand{\textasciicircum}{\verb?^?} % \^ is accent
    ---
            \newcommand{\textcolor}[3][]{#3}

More complicated macros as well as environments have to be registered
with Python code. This may be done with options ``--pack`` and
``--packages`` for yalafi and yalafi.shell, respectively; compare
section `Extension modules for LaTeX
packages <#extension-modules-for-latex-packages>`__. Alternatively, you
can modify the collections ``Parameters.macro_defs_python`` and
``Parameters.environment_defs`` in ``yalafi/parameters.py``.

Definition of macros
~~~~~~~~~~~~~~~~~~~~

``Macro(parms, name, args='', repl='', defaults=[], extract='')``

-  ``parms``: current object of type Parameters
-  ``name``: macro name with leading backslash ``\``
-  ``args``: string that codes the argument sequence

   -  ``A``: mandatory argument, may be a single token or a sequence
      enclosed in ``{}`` braces
   -  ``O``: optional argument in ``[]`` brackets
   -  ``*``: optional asterisk

-  ``repl``: replacement string as for ``\newcommand`` (``*`` does count
   as argument), or a function (see point `Macro handler
   functions <#macro-handler-functions>`__ below)
-  ``defaults``: an optional list of replacement strings for absent
   optional arguments
-  ``extract``: like ``repl``, but the resulting text is appended to the
   main text, separated by blank lines; for an example, see declaration
   of macro ``\footnote`` in ``Parameters.macro_defs_python`` in
   ``yalafi/parameters.py``

Definition of environments
~~~~~~~~~~~~~~~~~~~~~~~~~~

``Environ(parms, name, args='', repl='', defaults=[], remove=False, add_pars=True, items=None, end_func=None)``

Parameters ``parms`` to ``defaults`` are the same as for ``Macro()``,
where ``name`` does not start with a backslash. The arguments are those
behind the opening ``\begin{xyz}``. This means that the environment name
``xyz`` does not yet count as argument in ``args`` and ``repl``.

-  ``remove``: if True, then the complete environment body is skipped; a
   fixed replacement can be given in ``repl``
-  ``add_pars``: if True, then paragraph breaks (blank lines) are
   generated before and behind the environment body
-  ``items``: for inclusion of specific ``\item`` labels; a generator
   taking a nesting level argument has to be specified; compare
   declaration of environment enumerate in ``yalafi/parameters.py``
-  ``end_func``: optional function to be called at ``\end{...}``; for an
   example, see file ``yalafi/packages/babel.py``

Definition of equation environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``EquEnv(parms, name, args='', repl='', defaults=[], remove=False)``

This is equivalent to ``Environ()``, but maths material is replaced
according to section `Handling of displayed
equations <#handling-of-displayed-equations>`__. Replacements in
``repl`` and ``defaults`` are still interpreted in text mode.

-  ``remove``: if True, then a fixed replacement can be specified in
   ``repl``, and trailing interpunction given by
   ``Parameters.math_punctuation`` in file ``yalafi/parameters.py`` is
   appended

Macro handler functions
~~~~~~~~~~~~~~~~~~~~~~~

Parameter ``repl`` of class ``Macro`` may specify a function with the
following arguments.

``handler(parser, buf, mac, args, delim, pos)``

It has to return a possibly empty list of tokens that are used as result
of the macro expansion. The list may include tokens of class
``VoidToken`` (see argument ``args``). - ``parser``: The active parser
object. For instance, member ``parser.parms`` is the current
``Parameter`` object from file
```yalafi/parameters.py`` <yalafi/parameters.py>`__. - ``buf``: The
token buffer we are reading from. The macro token, subsequent space, and
all declared macro arguments already have been read. For instance, you
can check the next token with ``buf.cur()``; see file
```yalafi/packages/xspace.py`` <yalafi/packages/xspace.py>`__ for an
application. - ``mac``: The object created with ``Macro()``. - ``args``:
A list of token lists. For each argument declared with ``Macro()``, a
possibly empty token list is passed. - ``*``: If the asterisk was
present, the token is given. Otherwise, the list is empty. - ``A``: The
argument tokens are given, excluding possibly surrounding curly braces.
If the argument was empty (pure ``{}``, paragraph break, or end of group
or text), the list consists of a single ``VoidToken``. - ``O``: If the
optional argument has not been specified, the list is empty. Otherwise,
the tokens excluding the surrounding square brackets are given. If the
option was a pure ``[]``, the list consists of a single ``VoidToken``. -
``delim``: A list of booleans, indicating the presence of delimiters
around the arguments. - ``*``: Always False. - ``A``: True, if the
argument has been delimited by curly braces. - ``O``: True, if the
argument is present. - ``pos``: Character position of the leading
backslash of the macro invocation, counting from zero.

For examples, see file ```yalafi/handlers.py`` <yalafi/handlers.py>`__.

`Back to contents <#contents>`__

Multi-file projects
-------------------

Here, we present one of several possibilities to cope with multiple
files. The main point is that the base LaTeX filter currently cannot
directly follow file inclusions like ``\input{...}``. Assume you have
the following file ``main.tex``.

::

    % (load document class and packages)
    % possibly: load own macro definitions etc.
    \input{defs.tex}
    % the previous command is ignored by the filter, thus:
    \LTinput{defs.tex}
    \begin{document}
    Test text.
    \input{ch1/intro.tex}
    \end{document}

Please provide the definition of ``\LTinput`` as in section `Adaptation
of LaTeX and plain text <#adaptation-of-latex-and-plain-text>`__.

In order to check the “normal text” only in file ``main.tex``, you say

::

    python -m yalafi.shell [...] --packages "" main.tex

Macros like ``\input`` are ignored, in this case. With the optional
``--packages ""``, default loading of all packages known to the filter
is suppressed.

The check of file ``ch1/intro.tex`` may look like

::

    python -m yalafi.shell [...] --packages "" --define main.tex ch1/intro.tex

Option ``--define main.tex`` ensures that all settings and definitions
from file ``main.tex`` are available. “Normal text” from that file is
ignored. Alternatively, you can add ``\LTinput{main.tex}`` at the
beginning of file ``ch1/intro.tex``.

A recursive check of all files is initiated by

::

    python -m yalafi.shell [...] --packages "" --include --define main.tex main.tex

During a first phase, all file names are collected by evaluation of
``\include``, ``\input``, ``\subfile`` and ``\subfileinclude`` commands.
Then, each file is processed on its own. If you want to exclude certain
files, for instance figures given in TeX code, you can use option
``--skip`` from section `Example application <#example-application>`__.

**Remark.** An alternative version is as follows. Write all commands
that YaLafi needs in an own file, say ``yy-defs.tex``. Then use option
``--define yy-defs.tex``, or place ``\LTinput{yy-defs.tex}`` in all
sources.

`Back to contents <#contents>`__

Handling of displayed equations
-------------------------------

Displayed equations should be part of the text flow and include the
necessary interpunction. The German version of
`LanguageTool <https://www.languagetool.org>`__ (LT) will detect a
missing dot in the following snippet. For English texts, see the
comments in section `Equation replacements in English
documents <#equation-replacements-in-english-documents>`__ ahead.

::

    Wir folgern
    \begin{align}
        a   &= b \\
        c   &= d
    \end{align}
    Daher ...

Here, ``a`` to ``d`` stand for arbitrary mathematical terms (meaning:
“We conclude <maths> Therefore, ...”). In fact, LT complains about the
capital “Daher” that should start a new sentence.

Trivial version
~~~~~~~~~~~~~~~

With the entry

::

        Environ(self, 'align', remove=True, add_pars=False),

in list ``environments`` of file
```yalafi/packages/amsmath.py`` <yalafi/packages/amsmath.py>`__, the
equation environment is simply removed. We get the following filter
output that will probably cause a problem, even if the equation itself
ends with a correct interpunction sign.

::

    Wir folgern
    Daher ...

Simple version
~~~~~~~~~~~~~~

With the entry

::

        EquEnv(self, 'align', repl='  Relation', remove=True),

in ``Parameters.environment_defs``, one gets:

::

    Wir folgern
      Relation
    Daher ...

Adding a dot ``= d.`` in the equation will lead to ``Relation.`` in the
output. This will also hold true, if the interpunction sign
(``Parameters.math_punctuation``) is followed by maths space or by
macros as ``\label`` and ``\nonumber.``

Full version
~~~~~~~~~~~~

**Remark.** Our equation parsing currently assumes that aligned
operators like ``=`` and ``+`` are placed on the right side of the
alignment character ``&``. LaTeX does not enforce that, but it is the
style found in examples of the documentation for package amsmath.

**Remark.** For a simplification, see option ``--simple-equations`` in
section `Example application <#example-application>`__.

With the default entry

::

        EquEnv(self, 'align'),

we obtain (“gleich” means equal, and setting language to English will
produce “equal”):

::

    Wir folgern
      V-V-V  gleich W-W-W
      W-W-W  gleich X-X-X.
    Daher ...

The replacements like ``V-V-V`` are taken from collections
``math_repl_display*`` in file ``yalafi/parameters.py`` that depend on
language setting, too. Now, LT will additionally complain about
repetition of ``W-W-W``. Finally, writing ``= b,`` and ``= d.`` in the
equation leads to the output:

::

    Wir folgern
      V-V-V  gleich W-W-W,
      X-X-X  gleich Y-Y-Y.
    Daher ...

The rules for equation parsing are described in section `Parser for
maths material <#parser-for-maths-material>`__. They ensure that
variations like

::

        a   &= b \\
            &= c.

and

::

        a   &= b \\
            &\qquad -c.

also will work properly. In contrast, the text

::

        a   &= b \\
        -c  &= d.

will again produce an LT warning due to the missing comma after ``b``,
since the filter replaces both ``b`` and ``-c`` by ``W-W-W`` without
intermediate text.

In rare cases, manipulation with ``\LTadd{...}`` or ``\LTskip{...}`` may
be necessary to avoid false warnings from the proofreader; compare
section `Adaptation of LaTeX and plain
text <#adaptation-of-latex-and-plain-text>`__.

Inclusion of “normal” text
~~~~~~~~~~~~~~~~~~~~~~~~~~

In variant “Full version”, the argument of ``\mbox`` (macro names:
collection ``Parameters.math_text_macros``, loading of LaTeX package
amsmath adds ``\text``) is directly copied. Outside of ``\mbox`` etc.,
only maths space like ``\;`` and ``\quad`` (see
``Parameters.math_space``) is considered as space. Therefore, one will
get warnings from the proofreading program, if subsequent \\text and
maths parts are not properly separated.

Equation replacements in English documents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The replacement collections ``math_repl_display*`` in file
``yalafi/parameters.py`` do not work well, if single letters are taken
as replacements. For instance, ``V.`` cannot be safely considered as end
of a sentence. We now have chosen replacements as ``U-U-U`` for German
and English texts.

Furthermore, the English version of LanguageTool (like other
proofreading tools) rarely detects mistakenly capital words inside a
sentence; they are probably considered as proper names. Therefore, a
missing dot at the end of a displayed equation is hardly found. An
experimental hack is provided by option ``--equation-punctuation`` of
application script ```yalafi/shell/shell.py`` <yalafi/shell/shell.py>`__
described in section `Example application <#example-application>`__.

`Back to contents <#contents>`__

Multi-language documents
------------------------

**Remarks.** This feature is experimental, any comments are welcome.
Operation may be slow, unless a LanguageTool server is used, for
instance, via option ``--server my``.

As an example, assume option ``--multi-language`` for yalafi.shell and
the LaTeX text:

::

    \documentclass{article}
    \usepackage[german,english]{babel}
    \newcommand{\german}[1]{\textit{\foreignlanguage{german}{#1}}}

    \begin{document}
    This is thex German word \german{excellent}..
    \end{document}

Then, the Vim example from section `“Plain Vim” <#plain-vim>`__ with
setting ``let g:ltyc_showsuggestions = 1`` will produce this quickfix
window:

::

    t.tex|6 col 9 info|  Possible spelling mistake found. Suggestion: the; then; they; them; thee; Theo; hex; THX; TeX; Tex; The; t hex; the x; Théo
    t.tex|6 col 34 info|  Möglicher Tippfehler gefunden. Suggestion: exzellent; exzellente; exzellenten; exzellenter; Exzellenz; exzellentes; erzählend; exzellentem; erhellend; erkältend; exzelliert
    t.tex|6 col 44 info|  Two consecutive dots Suggestion: .; …

The initial language is specified by option ``--language``, it is
overwritten upon ``\usepackage[...]{babel}``. Commands like
``\selectlanguage{...}`` are also effective in files loaded via option
``--define`` or with ``\LTinput{...}``. Language names in babel commands
are mapped to xx-XX codes by dictionary ``language_map`` in file
```yalafi/packages/babel.py`` <yalafi/packages/babel.py>`__.

**Further options.** In the above example, LanguageTool is invoked for
``This is thex German word L-L-L..`` with language en-GB, and for
``excellent`` with language de-DE. The following options for
yalafi.shell can be used to adjust the behaviour.

-  ``--ml-continue-threshold num``\  If a short inclusion, for instance
   via ``\foreignlanguage``, does not comprise more than ``num``
   plain-text words (default: 2), then the main text flow is continued.
   The inclusion is represented by a placeholder from collections
   ``lang_change_repl*`` in file ``yalafi/parameters.py``. Language
   changes with ``\selectlanguage`` always break the text flow.
-  ``--ml-rule-threshold num``\  If an inserted foreign-language text
   part consists of at most ``num`` words (default: 2), then options
   ``--ml-disable`` and ``--ml-disablecategories`` become effective for
   this text part.
-  ``--ml-disable rules``\  Additionally disable these LanguageTool
   rules for text parts matching option ``--ml-rule-threshold``
   (default: ''). For example, one might disable rule
   ``UPPERCASE_SENTENCE_START``.
-  ``--ml-disablecategories cats``\  Similar to ``--ml-disable`` for
   LanguageTool’s rule categories (default: '').

Please consider also the tweaks in section `Adaptation of LaTeX and
plain text <#adaptation-of-latex-and-plain-text>`__.

`Back to contents <#contents>`__

Python package interface
------------------------

We comment the central function in file
```yalafi/tex2txt.py`` <yalafi/tex2txt.py>`__ that uses the package
interface to emulate the behaviour of script ``tex2txt.py`` in
repository `Tex2txt <https://github.com/matze-dd/Tex2txt>`__.

::

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

-  2-7: This is an auxiliary function for the parser.
-  9: The created parameter object contains all default settings and
   definitions from file ``yalafi/parameters.py``.
-  11: We read the LaTeX packages from option ``--pack`` and convert
   them to a list of handler functions called later by the parser.
-  14-17: If option ``--extr`` requests only extraction of arguments of
   certain macros, this is prepared.
-  22: If call-back ``modify_parms`` is specified, it may change the
   parameters.
-  23: We create a parser object, the passed function is called on
   ``\LTinput``.
-  24: The parsing method returns a list of tokens.
-  27: The token list is converted into a 2-tuple containing the
   plain-text string and a list of numbers. Each number in the list
   indicates the estimated position of the corresponding character in
   the text string.
-  29: If phrase replacements are requested by option ``--repl``, this
   is done. String opts.repl contains the replacement specifications
   read from the file.
-  31: On option ``--unkn``, a list of unknown macros and environments
   is generated.
-  33: This is necessary, since position numbers are zero-based in
   yalafi, but one-based in ``Tex2txt/tex2txt.py``.
-  37: For a multi-language document, ``utils.get_txt_pos_ml()`` returns
   a dictionary, containing plain-text strings and character position
   maps for each language.
-  38: Phrase replacements are performed for text parts written in the
   main language.
-  44: This corresponds to line 33.

`Back to contents <#contents>`__

Differences to Tex2txt
----------------------

Invocation of ``python -m yalafi ...`` differs as follows from
``python tex2txt.py ...`` (the script described in
`Tex2txt/README.md <https://github.com/matze-dd/Tex2txt#command-line>`__).

-  Macro definitions with ``\(re)newcommand`` in the LaTeX input are
   processed, as well as ``\documentclass`` and ``\usepackage.``
-  Macro arguments need not be delimited by {} braces or [] brackets.
-  Macros are expanded in the order they appear in the text.
-  Character position tracking for displayed equations is improved, see
   `the example below <#equation-html-report>`__.
-  Added options ``--dcls`` and ``--pack`` allow modification of
   predefined LaTeX macros and environments at Python level.
-  Added option ``--seqs``.
-  Added option ``--nosp``.
-  Added option ``--mula``.
-  Option ``--defs`` expects a file containing macro definitions as
   LaTeX code.
-  Option ``--ienc`` is also effective for file from ``--defs``.
-  Option ``--char`` (position tracking for single characters) is always
   activated.
-  Default language is English. It is also used for an unknown language.

``YaLafi/yalafi/tex2txt.py`` is faster for input texts till about 30
Kilobytes, for larger files it can be slower than
``Tex2txt/tex2txt.py --char``. Run-time increases quasi linearly with
file size. Due to token generation for each single “normal” character,
memory usage may be substantial for long input texts.

 With

::

    python -m yalafi.shell --equation-punct all --output html test.tex > test.html

and input

::

    For each $\epsilon > 0$, there is a $\delta > 0$ so that
    %
    \begin{equation}
    \norm{y-x} < \delta \text{\quad implies\quad}
        \norm{A(y) - A(x)} < \epsilon, \label{lab}
    \end{equation}
    %
    Therefore, operator $A$ is continuous at point $x$.

we get

.. figure:: _static/figs/example-equation.png
   :alt: HTML report

   HTML report

`Back to contents <#contents>`__

Remarks on implementation
-------------------------

Scanner / tokeniser
~~~~~~~~~~~~~~~~~~~

The scanner identifies token types defined in ``yalafi/defs.py``.

-  All “normal” characters yield an own token.
-  Many character combinations like ``{``, ``\[`` or ``---`` are
   recognised as “special tokens”.
-  Names of “normal” macros formed by a backslash and subsequent letters
   (method ``Parameters.macro_character()``) result in a token, macros
   ``\begin``, ``\end``, ``\item``, and ``\verb`` are treated
   separately.
-  For space, we distinguish between character sequences that do or do
   not represent a paragraph break. In both cases, a single token is
   generated.
-  Comments starting with ``%`` consume the rest of the line and leading
   space on the next line, if it is not blank. A single token is
   generated.

Parser
~~~~~~

The central method ``Parser.expand_sequence()`` does not directly read
from the scanner, but from an intermediate buffer that can take back
tokens. On macro expansion, the parser simply pushes back all tokens
generated by argument substitution. (Method
``Parser.expand_arguments()`` collects tokens forming macro arguments
and returns a list of replacement tokens that is eventually pushed back
in the main loop.) The result is close to the “real” TeX behaviour,
compare the tests in directory ``tests/``.

A method important for simple implementation is ``Parser.arg_buffer()``.
It creates a new buffer that subsequently returns tokens forming a macro
argument (only a single token or all tokens enclosed in paired ``{}``
braces or ``[]`` brackets).

Parser for maths material
~~~~~~~~~~~~~~~~~~~~~~~~~

We follow the ideas described in section `Handling of displayed
equations <#handling-of-displayed-equations>`__, compare the tests in
```tests/test_display.py`` <tests/test_display.py>`__. All unknown
macros, which are not in the blacklist ``Parameters.math_ignore``, are
assumed to generate some “visible” output. Thus, it is not necessary to
declare all the maths macros like ``\alpha`` and ``\sum``.

Displayed equations are parsed as follows.

-  Equation environments are split into “lines” separated by ``\\``.
-  Each “line” is split into “sections” delimited by ``&``.
-  Each “section” is split into “maths parts” only consisting of maths
   material separated by intermediate ``\text{...}`` or ``\mbox{...}``
   (``Parameters.math_text_macros``).
-  Arguments of ``\text`` and ``\mbox`` are directly copied.
-  A “maths part” is substituted with a placeholder from rotating
   collections ``math_repl_display*``, if it does not consist only of
   punctuation marks from ``Parameters.math_punctuation`` or of
   operators from ``Parameters.math_operators``.
-  A leading maths operator is displayed using ``math_op_text``
   (language-dependent), if the “maths part” is first in “section” and
   the “section” is not first on “line”.
-  Trailing interpunction of a “maths part” is appended to the
   placeholder.
-  If the “maths part” includes leading or trailing maths space from
   ``Parameters.math_space``, then white space is prepended or appended
   to the replacement.
-  Replacements from ``math_repl_display*`` are rotated

   -  if a non-blank ``\text`` part is detected,
   -  if a “maths part” starts with an operator and is first in
      “section”, but not on “line”,
   -  if a “maths part” only consists of an operator,
   -  if a “maths part” includes trailing interpunction.

Removal of unnecessary blank lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to avoid creation of new blank lines by macros expanding to
space or “nothing”, we include a token of type ``ActionToken`` whenever
expanding a macro. Method ``Parser.remove_pure_action_lines()`` removes
all lines only containing space and at least one such token. Initially
empty lines are retained. Together with the extraction of special text
flows, for instance from footnotes, this preserves sentences and
paragraphs, thus improving checks and reducing false positives from the
proofreading software.

`Back to contents <#contents>`__
