.. note::
  This part is just copied from the old documentation. Some links may not work.

YaLafi Proofreading CLI
=======================

.. highlight:: console


Example Python script ``yalafi/shell/shell.py`` will generate a proofreading report in text or HTML format from filtering the LaTeX input and application of `LanguageTool <https://www.languagetool.org>`__ (LT).
It is best called as module as shown below, but can also be placed elsewhere and invoked as script. A simple invocation producing an HTML report could be::

  python -m yalafi.shell --lt-directory ~/lib/LT --output html t.tex > t.html

On option ``--server lt``, LT’s Web server is contacted. Otherwise,
`Java <https://java.com>`__ has to be present, and the path to LT has to
be specified with ``--lt-directory`` or ``--lt-command``. Note that from
version 4.8, LT does not fully support 32-bit systems any more. Both LT
and the script will print some progress messages to ``stderr``. They can
be suppressed with ``python ... 2>/dev/null``.

::

  python -m yalafi.shell [OPTIONS] latex_file [latex_file ...] [> text_or_html_file]

Option names may be abbreviated. If present, options are also read from
a configuration file designated by script variable ``config_file`` (one
option per line, possibly with argument), unless ``--no-config`` is
given. Default option values are set at the Python script beginning.

``--lt-directory dir``
  Directory of the “manual” local LT installation (for variant 1 in section `Installation <#installation>`__).
  May be omitted on options ``--server lt`` and ``--textgears apikey``, or if script variable ``ltdirectory`` has been set appropriately.
  See also the script comment at variable ``ltdirectory``.
``--lt-command cmd``
  Base command to call LT (for variant 2 in section `Installation <#installation>`__).
  For instance, this is ``--lt-command languagetool``.
  If an LT server has to be started, the command is invoked with option ``--http``.
  Note that option ``--server stop`` for stopping a local LT server will not work in this case.
``--as-server port``
  Emulate an LT server listening on the given port, for an example see section `Interface to Emacs <#interface-to-emacs>`__.
  The fields of received HTML requests (settings for language, rules, categories) overwrite option values given in the command line.
  The internally used proofreader is influenced by options like ``--server``.
  Other options like ``--single-letters`` remain effective.
``--output mode``
  Mode is one of ``plain``, ``html``, ``xml``, ``xml-b``, ``json`` (default: ``plain`` for text report).
  Variant ``html`` generates an HTML report, see below for further details.
  Modes ``xml``, ``xml-b`` and ``json`` are intended for Vim plugins, compare section `Interfaces to Vim <#interfaces-to-vim>`__.
``--link``
  In an HTML report, left-click on a highlighted text part opens a Web link related to the problem, if provided by LT.
``--context number``
  Number of context lines displayed around each marked text region in HTML report (default: ``2``).
  A negative number shows the whole text.
``--include``
  Track file inclusions like ``\input{...}``.
  Script variable ``inclusion_macros`` contains a list of the corresponding LaTeX macro names.
``--skip regex``
  Skip files matching the given regular expression.
  This is useful, e.g., for the exclusion of figures on option ``--include``.
``--plain-input``
  Assume plain-text input, do not evaluate LaTeX syntax.
  This cannot be used together with options ``--include`` or ``--replace``.
``--list-unknown``
  Only print a list of unknown macros and environments seen outside of maths parts.
  Compare, for instance, `Issue #183 <../../issues/183>`__.
``--language lang``
  Language code as expected by LT (default: ``en-GB``).
``--encoding ienc``
  Encoding for LaTeX input and files from options ``--define`` and ``--replace`` (default: UTF-8).
``--replace file``
  File with phrase replacements to be performed after the conversion to plain text; see section `Phrase replacement in the plain text <#phrase-replacement-in-the-plain-text>`__.
``--define file``
  Read macro definitions as LaTeX code (using ``\newcommand`` or ``\def``).
  If the code invokes ``\documentclass`` or ``\usepackage``, then the corresponding modules are loaded.
``--documentclass  class``
  Load extension module for this class.
  See section `Extension modules for LaTeX packages <#extension-modules-for-latex-packages>`__.
``--packages modules``
  Load these extension modules for LaTeX packages, given as comma-separated list (default: ``*``).
  See section `Extension modules for LaTeX packages <#extension-modules-for-latex-packages>`__.
``--add-modules file``
  Parse the given LaTeX file and prepend all modules included by macro ``\usepackage`` to the list provided in option ``--packages``.
  Value of option ``--documentclass`` is overridden by macro ``\documentclass.``
``--extract macros``
  Only check first mandatory argument of the LaTeX macros whose names are given as comma-separated list.
  The option only works properly for predefined macros, including those imported by options ``--documentclass``, ``--define``, and ``--packages``.
  This is useful for check of foreign-language text, if marked accordingly.
  Internally used for detection of file inclusions on ``--include``.
``--simple-equations``
  Replace a displayed equation only with a single placeholder from collections ``math_repl_display*`` in file ``yalafi/parameters.py``; append trailing interpunction, if present.
``--no-specials``
  Revert changes from special macros and magic comments described in section `Modification of LaTeX text <#Modification-of-latex-text>`__.
``--disable rules``
  Comma-separated list of ignored LT rules, is passed as ``--disable`` to LT (default: ``WHITESPACE_RULE``).
``--enable rules``
  Comma-separated list of added LT rules, is passed as ``--enable`` to LT (default: '').
``--disablecategories cats`` ``--enablecategories cats``
  Disable / enable LT rule categories, directly passed to LT (default for both: '').
``--lt-options opts``
  Pass additional options to LT, given as single string in argument ``opts``.
  The first character of ``opts`` will be skipped and must not be ``-``.
  Example: ``--lt-options '~--languagemodel ../Ngrams --disablecategories PUNCTUATION'``.
  Some options are included into HTML requests to an LT server, see script variable ``lt_option_map``.
``--single-letters accept``
  Check for single letters, accepting those in the patterns given as list separated by ``|``.
  Example: ``--single-letters 'A|a|I|e.g.|i.e.||'`` for an English text, where the trailing ``||`` causes the addition of equation and language-change replacements from collections ``math_repl_*`` and ``lang_change_repl*`` in file ``yalafi/parameters.py``.
  All characters except ``|`` are taken verbatim, but ``~`` and ``\,`` are interpreted as UTF-8 non-breaking space and narrow non-breaking space.
``--equation-punctuation mode``
  This is an experimental hack for the check of punctuation after equations in English texts, compare section `Equation replacements in English documents <#equation-replacements-in-english-documents>`__.
  An example is given in section `Differences to Tex2txt <#differences-to-tex2txt>`__.
  The abbreviatable mode values indicate the checked equation type: ``displayed``, ``inline``, ``all``.
  The check generates a message, if an element of an equation is not terminated by a dot ``.``, and at the same time is not followed by a lower-case word or another equation element, both possibly separated by a punctuation mark from ``,;:``.
  Patterns for equation elements are given by collections ``math_repl_display*`` and ``math_repl_inline*`` in file ``yalafi/parameters.py``.
``--server mode``
  Use LT’s Web server (mode is ``lt``) or a local LT server (mode is ``my``) instead of LT’s command-line tool.
  Stop the local server (mode is ``stop``, currently only works under Linux and Cygwin).
  
  LT’s server
    Server address is set in script variable ``ltserver``.
    For conditions and restrictions, please refer to https://dev.languagetool.org/public-http-api.
  Local server
    If not yet running, then start it according to script variable ``ltserver_local_cmd``.
    On option ``--lt-command``, the specified command is invoked with option ``--http``.
    Additional server options can be passed with ``--lt-server-options``.
    See also https://dev.languagetool.org/http-server.
    This may be faster than the command-line tool used otherwise, especially when checking many LaTeX files or together with an editor plugin.
    The server will not be stopped at the end (use ``--server stop``).
``--lt-server-options opts``
  Pass additional options when starting a local LT server.
  Syntax is as for ``--lt-options``.
``--textgears apikey``
  Use the TextGears server, see https://textgears.com.
  Language is fixed to American English.
  The access key ``apikey`` can be obtained on page https://textgears.com/signup.php?givemethatgoddamnkey=please, but the key ``DEMO_KEY`` seems to work for short input.
  The server address is given by script variable ``textgears_server``.
``--multi-language``
  Activate support of multi-language documents; compare section `Multi-language documents <#multi-language-documents>`__ for further related options.
``--no-config``
  Do not read config file, whose name is set in script variable ``config_file``.
