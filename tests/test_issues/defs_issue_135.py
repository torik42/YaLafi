
from yalafi import defs

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_python = [

        defs.Macro(parms, '\\xyz', args='OAA', repl=h_xyz)

    ]

    return defs.InitModule(macros_python=macros_python)


def h_xyz(parser, buf, mac, args, delim, pos):
    return [
        defs.TextToken(pos, str(len(args[0]))),
        defs.TextToken(pos, str(len(args[1]))),
        defs.TextToken(pos, str(len(args[2]))),
        defs.TextToken(pos, repr(type(args[1][0]) is defs.VoidToken)),
        defs.TextToken(pos, repr(type(args[2][0]) is defs.VoidToken)),
    ]

