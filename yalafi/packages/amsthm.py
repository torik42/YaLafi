
#
#   YaLafi module for LaTeX package amsthm
#

from yalafi.defs import InitModule, Environ, SpaceToken, TextToken

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\qedhere}{}
        \newcommand{\theoremstyle}[1]{}
        \newcommand{\newtheoremstyle}[9]{}

    """

    macros_python = []

    environments = [

        Environ(parms, 'proof', args='O', repl=h_proof),

    ]

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

def h_proof(parser, buf, mac, args, delim, pos):
    if args[0]:
        ret = args[0]
    else:
        ret = [TextToken(pos, parser.parms.lang_context.proof_name,
                        pos_fix=True)]
    return ret + [TextToken(ret[-1].pos, '.', pos_fix=True),
                        SpaceToken(ret[-1].pos, '\n', pos_fix=True)]

