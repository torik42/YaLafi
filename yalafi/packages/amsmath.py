
#
#   YaLafi module for LaTeX package amsmath
#

from yalafi.defs import Macro, ModParm, EquEnv

require_packages = []

#
#   Please note:
#   - For all undeclared maths macros, which are not blacklisted in
#     Parameters.math_ignore (yalafi/parameters.py), we assume that
#     a part of a mathematical term or an operator is left.
#   - The spacing macros and \notag are imporant for correct parsing
#     of maths material.
#
def modify_parameters(parms):

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

    return ModParm(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

