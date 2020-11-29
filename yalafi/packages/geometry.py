
#
#   YaLafi module for LaTeX package geometry
#

from yalafi.defs import Macro, InitModule

require_packages = []

#
#   Please note:
#   - For all undeclared maths macros, which are not blacklisted in
#     Parameters.math_ignore (yalafi/parameters.py), we assume that
#     a part of a mathematical term or an operator is left.
#   - The spacing macros and \notag are imporant for correct parsing
#     of maths material.
#
def init_module(parser, options):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\geometry}[1]{}

    """

    return InitModule(macros_latex=macros_latex)

