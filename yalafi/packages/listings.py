
#
#   YaLafi module for LaTeX package listings
#

from yalafi.defs import ModParm, Environ

require_packages = []

def modify_parameters(parms):

    macros_latex = r"""

        \newcommand{\lstinputlisting}[2][]{\par}
        \newcommand{\lstset}[1]{}

    """

    macros_python = []

    environments = [

        Environ(parms, 'lstlisting', remove=True),

    ]

    return ModParm(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

