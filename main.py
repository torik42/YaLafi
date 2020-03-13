
#
#   YaLafi: read LaTeX text from stdin
#

from yalafi import parameters, parser, utils
import sys

# add macros to those already defined in parameters.py
#
add_macros = r"""
\newcommand{\swap}[2]{#2#1}
"""

p = parser.Parser(parameters.Parameters(), add_macros=add_macros)

latex = sys.stdin.read()
toks = p.parse(latex)
txt, pos = utils.get_txt_pos(toks)
print(txt, end='')
print(pos)

