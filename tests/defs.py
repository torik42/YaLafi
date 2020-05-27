
from yalafi.defs import ModParm, Environ, EquEnv

require_packages = ['amsmath']  # for test_modules.py

def modify_parameters(parms):

    environments = [

        Environ(parms, 'comment', repl='', remove=True, add_pars=False),
        EquEnv(parms, 'flalign', repl='  relation', remove=True),

    ]

    return ModParm(environments=environments)

