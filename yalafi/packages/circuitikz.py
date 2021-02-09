
#
#   YaLafi module for LaTeX package circuitikz
#

from yalafi.defs import Environ, InitModule

require_packages = ['tikz']

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\ctikzset}[1]{}

    """

    macros_python = []

    environments = [

        Environ(parms, 'circuitikz', remove=True, add_pars=False),

    ]

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

