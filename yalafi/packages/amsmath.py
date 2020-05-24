
#
#   YaLafi module for LaTeX package amsmath
#

from yalafi.defs import ModParm, EquEnv

require_packages = []

def modify_parameters(parms):

    parms.math_text_macros.append('\\text')

    macros_latex = r"""
        \newcommand{\eqref}[1]{(0)}
        \newcommand{\medspace}{\:}
        \newcommand{\negmedspace}{}
        \newcommand{\negthickspace}{}
        \newcommand{\negthinspace}{}
        \newcommand{\notag}{}
        \newcommand{\thickspace}{\;}
        \newcommand{\thinspace}{\,}
    """

    environments = [

        EquEnv(parms, 'align'),
        EquEnv(parms, 'align*'),
        EquEnv(parms, 'alignat', args='A'),
        EquEnv(parms, 'alignat*', args='A'),
        EquEnv(parms, 'equation*'),

    ]

    return ModParm(macros_latex=macros_latex, environments=environments)

