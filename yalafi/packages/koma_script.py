
#
#   YaLafi: \documentclass{scrartcl}
#

from yalafi.defs import InitModule, Macro
from yalafi import handlers as hs

require_packages = []


def init_module(parser, options, position):
    parms = parser.parms

    parser.global_latex_options += options

    macros_latex = r"""

        \newcommand{\KOMAoption}[1]{}
        \newcommand{\KOMAoptions}[1]{}

    """

    macros_python = [

        Macro(parms, '\\subtitle', args='*OA', repl=hs.h_heading),
        Macro(parms, '\\extratitle', args='*OA', repl=hs.h_heading),
        Macro(parms, '\\subject', args='*OA', repl=hs.h_heading),

    ]

    return InitModule(macros_latex=macros_latex, macros_python=macros_python)
