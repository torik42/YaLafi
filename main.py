
#
#   YaLafi: read LaTeX text from stdin
#

from yalafi import parser, utils
import sys

# add macros to those already defined in parameters.py
#
add_macros = r"""
\newcommand{\swap}[2]{#2#1}
"""

parms = utils.get_default_parameters()
p = parser.Parser(parms, add_macros=add_macros)

latex = sys.stdin.read()
toks = p.parse(latex)
txt, pos = utils.get_txt_pos(toks)
print(txt, end='')
print(pos)

