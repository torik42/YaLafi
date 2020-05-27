
#
#   YaLafi module for LaTeX package amsthm
#

from yalafi.defs import ModParm, Environ

require_packages = []

def modify_parameters(parms):

    macros_latex = r"""
        \newcommand{\qedhere}{}
    """

    environments = [

        Environ(parms, 'proof', args='O',
                            # Parser.expand_arguments() may skip space
                            repl='#1.\n', defaults=[parms.proof_name]),

    ]

    return ModParm(macros_latex=macros_latex, environments=environments)

