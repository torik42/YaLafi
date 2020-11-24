
#
#   - test  of \newcommand with default value for optional argument
#   - test of \def
#

from yalafi import parameters, parser, utils

p = parser.Parser(parameters.Parameters())

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


latex_3 = r"""
\def\xxx#1#2{X#2Y#1Z}
\xxx AB
"""
plain_3 = """
XBYAZ
"""
def test_3():
    toks = p.parse(latex_3)
    plain, pos = utils.get_txt_pos(toks)
    assert plain == plain_3

latex_4 = r"""
\def\zB{z.\,B.\ }
X \zB Y
"""
plain_4 = """
X z.\N{NARROW NO-BREAK SPACE}B. Y
"""
def test_4():
    toks = p.parse(latex_4)
    plain, pos = utils.get_txt_pos(toks)
    assert plain == plain_4

latex_5 = r"""
\def\xxx[#1]{#1:#1}
X\xxx
[a]Y
"""
plain_5 = """
Xa:aY
"""
def test_5():
    toks = p.parse(latex_5)
    plain, pos = utils.get_txt_pos(toks)
    assert plain == plain_5

