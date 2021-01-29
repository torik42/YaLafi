
#
#   YaLafi module for LaTeX package amsmath
#

from yalafi.defs import Macro, InitModule, EquEnv, SpecialToken

require_packages = []

#
#   Please note:
#   - For all undeclared maths macros, which are not blacklisted in
#     Parameters.math_ignore (yalafi/parameters.py), we assume that
#     a part of a mathematical term or an operator is left.
#   - The spacing macros and \notag are imporant for correct parsing
#     of maths material.
#
def init_module(parser, options, position):
    parms = parser.parms

    parms.math_text_macros.append('\\text')

    macros_latex = r"""

        \newcommand{\eqref}[1]{(0)}
        \newcommand{\medspace}{\:}
        \newcommand{\negmedspace}{}
        \newcommand{\negthickspace}{}
        \newcommand{\negthinspace}{}
        \newcommand{\notag}{}
        \newcommand{\numberwithin}[2]{}
        \newcommand{\thickspace}{\;}
        \newcommand{\thinspace}{\,}

    """

    macros_python = [

        Macro(parms, '\\DeclareMathOperator', args='*AA'),
        Macro(parms, '\\substack', args='A', repl=h_substack),

    ]

    environments = [

        EquEnv(parms, 'align'),
        EquEnv(parms, 'align*'),
        EquEnv(parms, 'alignat', args='A'),
        EquEnv(parms, 'alignat*', args='A'),
        EquEnv(parms, 'equation'),
        EquEnv(parms, 'equation*'),
        EquEnv(parms, 'flalign'),
        EquEnv(parms, 'flalign*'),
        EquEnv(parms, 'gather'),
        EquEnv(parms, 'gather*'),
        EquEnv(parms, 'multiline'),
        EquEnv(parms, 'multiline*'),

    ]

    inject_tokens = []      # this list of tokens is used as replacement
                            # for '\documentclass...' or '\usepackage...'

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                    environments=environments, inject_tokens=inject_tokens)


#   macro \substack: replace \\ tokens with space
#
def h_substack(parser, buf, mac, args, delim, pos):
    def f(tok, lev):
        if tok.txt == r'\\' and lev == 0:
            return SpecialToken(tok.pos, r'\;')
        return tok
    return [f(tok, lev) for tok, lev in parser.iter_token_levels(args[0])]

