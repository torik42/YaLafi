
#
#   YaLafi module for LaTeX package xcolor
#

from yalafi.defs import Macro, InitModule

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

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

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

