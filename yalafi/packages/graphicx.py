
#
#   YaLafi module for LaTeX package graphicx
#

from yalafi.defs import InitModule

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\includegraphics}[2][]{}

    """

    macros_python = []

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

