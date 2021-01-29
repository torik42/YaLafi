
#
#   YaLafi module for LaTeX package tikz
#

from yalafi.defs import Environ, InitModule

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\tikzset}[1]{}
        \newcommand{\usetikzlibrary}[1]{}

    """

    macros_python = []

    environments = [

        Environ(parms, 'tikzpicture', remove=True, add_pars=False),

    ]

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

