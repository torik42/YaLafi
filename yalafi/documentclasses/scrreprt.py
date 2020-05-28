
#
#   YaLafi: \documentclass{scrreprt}
#

from yalafi.defs import ModParm

require_packages = []

def modify_parameters(parms):

    macros_latex = r"""
        \newcommand{\KOMAoptions}[1]{}
    """

    return ModParm(macros_latex=macros_latex)

