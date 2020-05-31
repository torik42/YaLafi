
#
#   YaLafi: \documentclass{scrbook}
#

from yalafi.defs import ModParm

require_packages = []

def modify_parameters(parms):

    macros_latex = r"""

        \newcommand{\KOMAoption}[1]{}
        \newcommand{\KOMAoptions}[1]{}

    """

    return ModParm(macros_latex=macros_latex)

