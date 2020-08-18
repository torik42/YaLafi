
#
#   YaLafi module for LaTeX package pgfplots
#

from yalafi.defs import ModParm

require_packages = ['graphicx', 'tikz']

def modify_parameters(parms):

    macros_latex = r"""

        \newcommand{\pgfplotsset}[1]{}

    """

    macros_python = []

    environments = []

    return ModParm(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

