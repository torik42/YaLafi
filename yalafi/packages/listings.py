
#
#   YaLafi module for LaTeX package listings
#

from yalafi.defs import InitModule, Environ

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\lstinputlisting}[2][]{\par}
        \newcommand{\lstset}[1]{}

    """

    macros_python = []

    environments = [

        Environ(parms, 'lstlisting', remove=True),

    ]

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

