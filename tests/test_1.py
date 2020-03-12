
from yalafi import parser, utils

add_macros = r"""
\newcommand{\swap}[2]{#2#1}
"""

parms = utils.get_default_parameters()
p = parser.Parser(parms, add_macros=add_macros)

latex1 = r"""
\swap
{12}
\textbackslash
"""
plain1_should_be = r"""
\12
"""
def test_1():
    toks = p.parse(latex1)
    plain1, pos1 = utils.get_txt_pos(toks)

    assert plain1_should_be == plain1

    assert pos1[0] == 0     # initial '\n' in plain
    assert pos1[1] == 12    # \, position of \textbackslash
    assert pos1[2] == 8     # 1 of 12
    assert pos1[3] == 9     # 2 of 12

latex2 = r"""
\newcommand{\xxx}[1]{\swap}
\xxx {x} 1 2
"""
plain2_should_be = r"""
21
"""
def test_2():
    toks = p.parse(latex2)
    plain2, pos2 = utils.get_txt_pos(toks)

    assert plain2_should_be == plain2

latex3 = r"""
{1
}{
2}
"""
plain3_should_be = r"""
1
2
"""
def test_3():
    toks = p.parse(latex3)
    plain3, pos3 = utils.get_txt_pos(toks)

    assert plain3_should_be == plain3

