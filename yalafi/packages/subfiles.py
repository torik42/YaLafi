
#
#   YaLafi module for LaTeX package subfile
#

from yalafi.defs import Environ, InitModule

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\subfile}[1]{}
        \newcommand{\subfileinclude}[1]{}

    """

    macros_python = []

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

