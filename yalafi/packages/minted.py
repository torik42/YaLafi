
#
#   YaLafi module for LaTeX package minted
#

from yalafi.defs import InitModule, Environ

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\setminted}[1]{}
        \newcommand{\mintinline}[2]{}

    """

    macros_python = []

    environments = [

        Environ(parms, 'minted', remove=True),

    ]

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

