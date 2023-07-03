Integration into Vim
--------------------

As `Vim <https://www.vim.org>`_ is a great editor, there are several possibilities that build on existing Vim plugins or use Vim’s compiler interface.


Plugin vimtex
^^^^^^^^^^^^^


The Vim plugin `vimtex <https://github.com/lervag/vimtex>`_
provides comprehensive support for writing LaTeX documents.
It includes an interface to YaLafi, documentation is available with
``:help vimtex-grammar-vlty``.
A copy of the corresponding Vim compiler script is
`editors/vlty.vim <https://github.com/torik42/YaLafi/blob/master/editors/vlty.vim>`_.

The following snippet demonstrates a basic `vimrc` setting and some useful
values for `vlty` option field `shell_options`::

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

.. note::
   There is more in :doc:`../remaining-old-documentation`.