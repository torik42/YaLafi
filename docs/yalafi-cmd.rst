.. note::

    This part is just copied from the old documentation. Some links may not work.

YaLafi Plain Parsing CLI
========================

The LaTeX filter can be integrated in shell scripts, compare the
examples in
`Tex2txt/README.md <https://github.com/matze-dd/Tex2txt#tool-integration>`__.

::

    python -m yalafi [--nums file] [--repl file] [--defs file] [--dcls class]
                     [--pack modules] [--extr macros] [--lang xy] [--ienc enc]
                     [--seqs] [--unkn] [--nosp] [--mula base] [latexfile]

Without positional argument ``latexfile``, standard input is read.

``--nums file``
  File for storing estimated original position numbers for each character of plain text. This can be used later to correct position figures in proofreader messages.
``--repl file``
  As option ``--replace`` in :doc:`yalafi-shell-cmd`.
``--defs file``
  As option ``--define`` in
  :doc:`yalafi-shell-cmd`.
``--dcls class`` and ``--pack modules``
  As options ``--documentclass`` and ``--packages`` in :doc:`yalafi-shell-cmd`.
``--extr ma[,mb,...]``
  As option ``--extract`` in :doc:`yalafi-shell-cmd`.
``--lang xy``
  Language ``de``, ``en`` or ``ru`` (default: ``en``,
  also taken in case of unknown language). Is used for adaptation of
  equation replacements, maths operator names, proof titles, and for
  handling of macros like ``"=``.
``--ienc enc``
  As option ``--encoding`` in :doc:`yalafi-shell-cmd`.
``--seqs``
  As option ``--simple-equations`` in :doc:`yalafi-shell-cmd`.
``--unkn``
  As option ``--list-unknown`` in :doc:`yalafi-shell-cmd`.
``--nosp``
  As option ``--no-specials`` in :doc:`yalafi-shell-cmd`.
``--mula base``
  Turn on multi-language processing. The different text parts are stored in files ``<base>.<part>.<language>``.
  If ``--nums`` has been specified, the position maps are written to files with similar naming scheme.
