
from yalafi import parameters, parser, utils

add_macros = r"""
\newcommand{\swap}[2]{#2#1}
"""

parms = parameters.Parameters()
parms.macro_defs_latex += add_macros
p = parser.Parser(parms)

latex_1 = r"""
\swap
{12}
\textbackslash
"""
plain_1 = r"""
\12
"""
def test_1():
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)

    assert plain == plain_1

    assert pos[0] == 0     # initial '\n' in plain
    assert pos[1] == 12    # \, position of \textbackslash
    assert pos[2] == 8     # 1 of 12
    assert pos[3] == 9     # 2 of 12

latex_2 = r"""
\newcommand{\xxx}[1]{\swap}
\xxx {x} 1 2
"""
plain_2 = r"""
21
"""
def test_2():
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)

    assert plain == plain_2

latex_3 = r"""
{1
}{
2}
"""
plain_3 = r"""
1
2
"""
def test_3():
    toks = p.parse(latex_3)
    plain, pos = utils.get_txt_pos(toks)

    assert plain == plain_3

latex_macro_in_arg = r"""
\usepackage{xcolor}
\newcommand{\xxx}[2]{#1#2}
A \xxx{\textcolor}{}{red}{blue} B
"""
plain_macro_in_arg = r"""
A blue B
"""
def test_macro_in_arg():
    toks = p.parse(latex_macro_in_arg)
    plain, pos = utils.get_txt_pos(toks)
    assert plain == plain_macro_in_arg

