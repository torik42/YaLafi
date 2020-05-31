
#
#   YaLafi module for LaTeX package xcolor
#

from yalafi.defs import Macro, ModParm

require_packages = []

def modify_parameters(parms):

    macros_latex = r"""

        \newcommand{\color}[2][]{}
        \newcommand{\colorbox}[3][]{#3}
        \newcommand{\definecolor}[4][]{}
        \newcommand{\textcolor}[3][]{#3}

    """

    macros_python = [

        Macro(parms, '\\fcolorbox', args='OAOAA', repl='#5'),

    ]

    environments = []

    return ModParm(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

