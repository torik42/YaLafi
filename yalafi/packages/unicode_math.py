
#
#   YaLafi module for LaTeX package unicode-math
#

from yalafi.defs import Macro, InitModule

require_packages = []

def init_module(parser, options):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\unimathsetup}[1]{}

    """

    macros_python = [
        Macro(parms, '\\setmathfont', args='AO', repl='')
    ]

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)
