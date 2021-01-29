
from yalafi.defs import InitModule, Environ, EquEnv, Macro, TextToken

require_packages = ['amsmath']  # for test_modules.py

def init_module(parser, options, position):
    parms = parser.parms

    macros_python = [
        # test_macros.py
        Macro(parms, '\\delim', args='*OA', repl=h_delim),

    ]

    environments = [

        # test_environments.py
        Environ(parms, 'comment', repl='', remove=True, add_pars=False),
        # test_display.py
        EquEnv(parms, 'flalign', repl='  relation', remove=True),

    ]

    return InitModule(macros_python=macros_python, environments=environments)

def h_delim(parser, buf, mac, args, delim, pos):
    return [
        TextToken(pos, repr(delim[0])),
        TextToken(pos, repr(delim[1])),
        TextToken(pos, repr(delim[2]))
    ]

