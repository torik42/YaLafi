
#
#   YaLafi module for LaTeX package hyperref
#

from yalafi.defs import InitModule, Macro

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\href}[3][]{#3}
        \newcommand{\texorpdfstring}[2]{#1}
        \newcommand{\url}[1]{#1}

    """

    macros_python = [

        Macro(parms, '\\ref', args='*A', repl='0'),
        
    ]

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

