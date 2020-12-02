
#
#   YaLafi module for LaTeX package xspace
#

from yalafi import defs
from yalafi.defs import Macro, InitModule

require_packages = []

def init_module(parser, options):
    parms = parser.parms

    macros_latex = ""

    macros_python = [

        Macro(parms, '\\xspace', args='A', repl=h_xspace),

    ]

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)


#   see http://mirrors.ctan.org/macros/latex/required/tools/xspace.dtx
#   line 243: \def\@xspace@exceptions@tlp{%
#
xspace_excl = ['.', ',', "'", "''", '/', '?', ';', ':', '!', '~',
                    '-', '--', '---', ')', '\\footnote', '\\footnotemark']


def h_xspace(parser, buf, mac, args, delim, pos):
    arg = args[0]
    if len(arg) == 1 and type(arg[0]) is defs.VoidToken:
        return []
    if not arg[0].txt in xspace_excl:
        arg.insert(0, defs.SpaceToken(arg[0].pos, ' '))
    return arg

