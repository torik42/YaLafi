
#
#   YaLafi module for LaTeX package geometry
#

from yalafi.defs import Macro, InitModule

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\geometry}[1]{}

    """

    return InitModule(macros_latex=macros_latex)

