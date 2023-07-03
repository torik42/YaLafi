Basic Usage
-----------

There are different ways to use YaLafi depending on your needs.

#. The basic package ``yalafi`` can be used to parse a LaTeX file into plain text, it is meant to be integrated into other tools. See for example `CheckMyTex <https://pypi.org/project/CheckMyTex/>`_ and `flachtex <https://pypi.org/project/flachtex/>`_.
#. It also provides a command line interface to parse a LaTeX file into plain text, which can be used to put the text into an online proofreading tool or debugging YaLafi. (See :doc:`/yalafi-cmd`.)
#. The subpackage ``yalafi.shell`` integrates ``yalafi`` with the proofreading software `LanguageTool <https://languagetool.org/>`_. It can be used to check a LaTeX file for grammar and style errors and output them as plain text, HTML, or JSON.
#. Probably most useful are the various integrations of ``yalafi.shell`` into text editors and IDEs. These are explained in more detail in :doc:`/editor-integration`.

In the following, we explain some basic usage and internal workings for the command line interface to ``yalafi.shell``.
This will also be helpful to understand the editor integrations which build on the command line interface and the basic filter.
More details are given in the rest of the documentation.

.. _basic_usage_command_line:

Running YaLafi from the Command Line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: console

The recommended way to interact with LanguageTool is by starting a separate server process.
After installing LanguageTool you can start the server with:

.. code-block:: console

    java -cp path/to/languagetool-server.jar org.languagetool.server.HTTPServer --port 8081 --allow-origin "*"

See the `LanguageTool documentation <https://dev.languagetool.org/http-server>`_ for more details.
The server can also be started using YaLafi, see :doc:`/yalafi-shell-cmd`.

.. tip::
    Running a server will allow caching and dramatically speedup subsequent checks of the same document.

After the server is running, one can check a document using::

    python -m yalafi.shell --server my path/to/document.tex

This will print the errors to the console.
To get a more readable output, one can use the ``--output`` option::

    python -m yalafi.shell --server my --output html path/to/document.tex > path/to/document.html

and view the problems in the browser by opening ``path/to/document.html``.
Later you might want to install one of the extensions for your editor, see :doc:`/editor-integration`.


How YaLafi Processes a LaTeX Document
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To better understand the following sections, it is good to have a rough understanding of how YaLafi processes a LaTeX document.
Depending on the options, YaLafi loads itself with some predefined LaTeX commands.
It then proceeds with the following steps:

#. If present, the preamble is parsed and options to known packages are recognized.
#. Command definitions like ``\newcommand`` are parsed and YaLafi registers the commands.
#. All files included with ``\input`` or ``\include`` are also checked for command definitions. But now proofreading takes place.
#. The document is parsed into plain text removing all LaTeX markup and replacing equations by placeholders.
#. The plain text version is proofread using LanguageTool and the errors are related to their original location in the LaTeX document.


Handling Common False Positives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _special_macros:

Unknown Commands
""""""""""""""""

.. highlight:: latex

YaLafi tries to remove the LaTeX markup as good as possible, but it is not perfect.
Many common LaTeX commands are known to YaLafi and replaced properly, see the `List of Macros <https://github.com/torik42/YaLafi/blob/master/list-of-macros.md>`_.
Unknown commands are ignored if they have no arguments or replaced by their arguments if they have arguments.
This often works well within the text for commands like ``\textbf`` or ``\textit``, but can lead to problems in the preamble.
You can exclude parts not interesting to YaLafi with::

    %%% LT-SKIP-BEGIN
    \someCommand{...}
    %%% LT-SKIP-END

Just be sure not to skip command definitions which should be parsed by YaLafi for further usage.
For fine grained control there are commands ``\LTadd``, ``\LTskip``, ``\LTalter`` and ``\LTinput``.
To avoid problems when compiling the LaTeX document you have to define them as::

    \newcommand{\LTadd}[1]{}
    \newcommand{\LTalter}[2]{#1}
    \newcommand{\LTskip}[1]{#1}
    \newcommand{\LTinput}[1]{}

YaLafi has its own definition of these commands such that the argument of ``\LTadd`` is seen by YaLafi but not LaTeX, while the argument of ``\LTskip`` is ignored by YaLafi but will be included by LaTeX.

Hence, you can exclude commands also with ``\LTskip``::

    \LTskip{\someCommand{...}}

or even replace command definitions with something simpler::

    \LTadd{\newcommand{\someCommand}[1]{
        % Command definition only used by YaLafi
    }}

In case you have more commands which you need to redefine only for YaLafi, you can put them into a separate file and include it with ``\LTinput``.
It will then be parsed only by YaLafi but not LaTeX.


Unknown Words
"""""""""""""

YaLafi itself has no option to add single words to the dictionary used by LanguageTool.
Instead, you can add correct and faulty spellings to ``spelling_custom.txt`` and ``spelling_prohibit.txt`` within the LanguageTool directory ``.../LanguageTool-X.X/org/languagetool/resource/<lang-code>/hunspell/``, respectively, where ``<lang-code>`` depends on the language you are using.

.. tip::
    If these files don’t work for you, you can add the words to ``spelling.txt`` and ``prohibit.txt`` in the same directory.

However, you can ignore a set of LanguageTool rules by passing them as a comma separated list with the option ``--disable``.
The default value is ``WHITESPACE_RULE``, because LaTeX ignores multiple white spaces.


Equation Parsing
""""""""""""""""

.. highlight:: latex

Inline equations ``$ ... $`` or ``\( ... \)`` are replaced by a placeholder like ``U-U-U``.
This way, they are treated like single words by LanguageTool.

Also displayed equations should be part of the text flow and include the necessary punctuation.
Consider the following LaTeX snippet:

.. literalinclude:: snippets/equation-parsing-full-1.tex
    :linenos:

YaLafi parses this into:

.. literalinclude:: snippets/equation-parsing-full-1.plain

And LanguageTool will complain about the repetition of ``W-W-W``.
The problem is a missing comma ``,`` or ``\text{and}`` at the end of the first line of the equation.
After replacing it with

.. literalinclude:: snippets/equation-parsing-full-2.tex
    :linenos:
    :lineno-match:
    :lines: 3

YaLafi parses this as

.. literalinclude:: snippets/equation-parsing-full-2.plain

and LanguageTool will not complain anymore.

.. note::
    Our equation parsing currently assumes that aligned operators like ``=`` and ``+`` are placed on the right side of the alignment character ``&``. LaTeX does not enforce that, but it is the style found in examples of the documentation for package amsmath.
    In some cases, this leads to false positives, which can often be avoided by using ``&\LTadd{+}`` or ``\LTskip{…}``.

    If you want to disable equation parsing completely, you can use the option ``--simple-equations``.

There still is a missing period at the end of the display equation in the above example.
The German version of LanguageTool has a rule for this.
But the English version rarely detects mistakenly capital words inside a sentence and a missing dot at the end of a displayed equation is hardly found.
An experimental solution is provided by option ``--equation-punctuation`` which will instruct YaLafi to add warnings for missing punctuations in display equations, see :doc:`/yalafi-shell-cmd`.


Multi-file Projects
^^^^^^^^^^^^^^^^^^^

.. highlight:: latex

Yalafi does not directly follow inclusions like ``\input`` or ``\include`` for proofreading.
In the following we describe how to handle multi file projects.

First, if you want to parse custom commands from an included file, you have to use ``\LTinput`` additionally to ``\input`` (you need to define ``\LTinput`` for LaTeX as described in :ref:`special_macros`)::

    \input{defs.tex}    % load macro definitions, ignored by YaLafi
    \LTinput{defs.tex}  % parse macro definitions with YaLafi

This will not yet proofread the content of ``defs.tex``.
It only parses the commands and registers them for later usage.
Alternatively, you can load files containing definitions with the option ``--define defs.tex``.

If you have multiple files containing text which should be checked, you might call YaLafi multiple times or use the option ``--include``.
Suppose you have the following file ``main.tex``::

    \documentclass{article}
    \input{defs.tex}
    \LTinput{defs.tex}
    \begin{document}
    \input{chapter1.tex}
    \input{chapter2.tex}
    \end{document}

In order to proofread the text (for example the title of the document) you just call YaLafi with ``main.tex``:

.. code-block:: console

    python -m yalafi.shell --packages "" main.tex

The ``--packages ""`` option is not necessary, it just suppresses the default loading of all packages known to YaLafi.
If you want to proofread the text of ``chapter1.tex`` you can call YaLafi with the option ``--define main.tex``, such that it loads the definitions from ``main.tex``:

.. code-block:: console

    python -m yalafi.shell --packages "" --define main.tex chapter1.tex

Alternatively you can add the following line to the beginning of ``chapter1.tex``:

    \LTinput{main.tex}

In both cases the text from ``main.tex`` is not checked, but the definitions are parsed by YaLafi.

A recursive check of all files is initiated by:

.. code-block:: console

    python -m yalafi.shell --packages "" --include main.tex

You still need to add ``--define main.tex`` to load the definitions from ``main.tex``, if you don’t use ``\LTinput{main.tex}`` in the included files.
If you want to exclude certain files, for instance figures given in TeX code, you can use option ``--skip``, see :doc:`/yalafi-shell-cmd`.


Multi-language Documents
^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: 
    This feature requires multiple calls of LanguageTool with different languages.
    Operation may be slow, unless a LanguageTool server is used.
    For example with ``--server my``, see :ref:`basic_usage_command_line`.

YaLafi can proofread multi-language documents properly, if they use the LaTeX package ``babel``.
Therefore, you call YaLafi with option ``--multi-language`` and ensure that it parses the ``\usepackage{babel}`` command.
Commands like ``\selectlanguage{lang}`` or ``\foreignlanguage{lang}{...}`` are then parsed and the text is checked with the correct language.

Since YaLafi will read the current language from the ``\usepackage{babel}`` command, the ``--multi-language`` option is also useful if you use different languages in different documents.
