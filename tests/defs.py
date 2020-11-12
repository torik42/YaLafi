
from yalafi.defs import InitModule, Environ, EquEnv

require_packages = ['amsmath']  # for test_modules.py

def init_module(parser, options):
    parms = parser.parms

    environments = [

        Environ(parms, 'comment', repl='', remove=True, add_pars=False),
        EquEnv(parms, 'flalign', repl='  relation', remove=True),

    ]

    return InitModule(environments=environments)

