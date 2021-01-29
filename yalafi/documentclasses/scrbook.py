
#
#   YaLafi: \documentclass{scrbook}
#

from yalafi.defs import InitModule

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    parser.global_latex_options += options

    macros_latex = r"""

        \newcommand{\KOMAoption}[1]{}
        \newcommand{\KOMAoptions}[1]{}

    """

    return InitModule(macros_latex=macros_latex)

