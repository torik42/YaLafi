
from yalafi.defs import ModParm, Environ, EquEnv
from yalafi import handlers

require_packages = []

def modify_parameters(parms):

    def thm(s):
        return handlers.h_theorem(s)

    environments = [

        Environ(parms, 'comment', repl='', remove=True, add_pars=False),
        Environ(parms, 'theorem', args='O', repl=thm('Theorem')),
        EquEnv(parms, 'flalign', repl='  relation', remove=True),

    ]

    return ModParm(environments=environments)

