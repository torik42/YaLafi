
#
#   YaLafi module for LaTeX package inputenc
#

from yalafi.defs import InitModule

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\inputencoding}[1]{}

    """

    macros_python = []

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

