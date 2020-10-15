
#
#   YaLafi module for LaTeX package inputenc
#

from yalafi.defs import ModParm

require_packages = []

def modify_parameters(parms):

    macros_latex = r"""

        \newcommand{\inputencoding}[1]{}

    """

    macros_python = []

    environments = []

    return ModParm(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

