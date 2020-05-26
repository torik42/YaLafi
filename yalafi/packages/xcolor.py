
#
#   YaLafi module for LaTeX package xcolor
#

from yalafi.defs import ModParm

require_packages = []

def modify_parameters(parms):

    macros_latex = r"""
        \newcommand{\color}[1]{}
        \newcommand{\colorbox}[2]{#2}
        \newcommand{\fcolorbox}[3]{#3}
        \newcommand{\textcolor}[2]{#2}
    """

    return ModParm(macros_latex=macros_latex)

