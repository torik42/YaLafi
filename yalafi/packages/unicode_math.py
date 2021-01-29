
#
#   YaLafi module for LaTeX package unicode-math
#

from yalafi.defs import Macro, InitModule

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    math_operators = [
        '≤', '≥', '→', '∩', '∪', '⇒', '⇐',  '⇔', '⊂',
    ]

    parms.math_operators.extend(math_operators)

    macros_latex = r"""

        \newcommand{\unimathsetup}[1]{}

    """

    macros_python = [
        Macro(parms, '\\setmathfont', args='AO', repl='')
    ]

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)
