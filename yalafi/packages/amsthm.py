
#
#   YaLafi module for LaTeX package amsthm
#

from yalafi.defs import ModParm, Environ
from yalafi import handlers

require_packages = []

def modify_parameters(parms):

    macros_latex = r"""
        \newcommand{\qedhere}{}
    """

    def thm(s):
        return handlers.h_theorem(s)

    environments = [

        Environ(parms, 'proof', args='O',
                            # Parser.expand_arguments() may skip space
                            repl='#1.\n', defaults=[parms.proof_name]),

#       Environ(parms, 'corollary', args='O', repl=thm('Corollary')),
#       Environ(parms, 'definition', args='O', repl=thm('Definition')),
#       Environ(parms, 'example', args='O', repl=thm('Example')),
#       Environ(parms, 'lemma', args='O', repl=thm('Lemma')),
#       Environ(parms, 'proposition', args='O', repl=thm('Proposition')),
#       Environ(parms, 'remark', args='O', repl=thm('Remark')),
#       Environ(parms, 'theorem', args='O', repl=thm('Theorem')),

    ]

    return ModParm(macros_latex=macros_latex, environments=environments)

