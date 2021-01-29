
#
#   YaLafi module for LaTeX package xspace
#

from yalafi import defs
from yalafi.defs import Macro, InitModule

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = ""

    macros_python = [

        Macro(parms, '\\xspace', args='', repl=h_xspace),

    ]

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)


#   see http://mirrors.ctan.org/macros/latex/required/tools/xspace.dtx
#   line 243: \def\@xspace@exceptions@tlp{%
#
xspace_excl = ['.', ',', "'", "''", '/', '?', ';', ':', '!', '~',
                '-', '--', '---', ')', '{', '}',
                '\\footnote', '\\footnotemark']


def h_xspace(parser, buf, mac, args, delim, pos):
    tok = buf.cur()
    if tok and tok.txt not in xspace_excl:
        return [defs.SpaceToken(pos, ' ')]
    return []
