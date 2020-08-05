
#
#   YaLafi module for LaTeX package tikz
#

from yalafi.defs import Environ, ModParm

require_packages = []

def modify_parameters(parms):

    macros_latex = r"""

        \newcommand{\tikzset}[1]{}
        \newcommand{\usetikzlibrary}[1]{}

    """

    macros_python = []

    environments = [

        Environ(parms, 'tikzpicture', remove=True, add_pars=False),

    ]

    return ModParm(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

