
#
#   test  of \newcommand with default value for optional argument
#

from yalafi import parser, utils

parms = utils.get_default_parameters()
p = parser.Parser(parms)

latex1 = r"""
\newcommand{\xxx}[1][X]{#1Z}
\xxx
\xxx
[A]
"""
plain1_should_be = r"""
XZAZ
"""
def test_1():
    toks = p.parse(latex1)
    plain1, pos1 = utils.get_txt_pos(toks)

    assert plain1_should_be == plain1

latex2 = r"""
\newcommand{\xxx}[2][X]{#2#1}
\xxx{ A }
\xxx[B]C
"""
plain2_should_be = r"""
 A X
CB
"""
def test_2():
    toks = p.parse(latex2)
    plain2, pos2 = utils.get_txt_pos(toks)

    assert plain2_should_be == plain2

