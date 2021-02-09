
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

latex_6 = r"""
\def
"""
plain_6 = """
 LATEXXXERROR """
stderr_6 = r"""*** LaTeX error: code in 't.tex', line 2, column 1:
*** \def: missing macro name
"""
def test_6(capsys):
    capsys.readouterr()
    toks = p.parse(latex_6, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    cap = capsys.readouterr()
    assert plain == plain_6
    assert cap.err == stderr_6

latex_7 = r"""
\def \;"""
plain_7 = """
 LATEXXXERROR  """
stderr_7 = r"""*** LaTeX error: code in 't.tex', line 2, column 6:
*** \def: illegal macro name "\;"
"""
def test_7(capsys):
    capsys.readouterr()
    toks = p.parse(latex_7, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    cap = capsys.readouterr()
    assert plain == plain_7
    assert cap.err == stderr_7

latex_8 = r"""
\def\xxx
"""
plain_8 = """
 LATEXXXERROR """
stderr_8 = r"""*** LaTeX error: code in 't.tex', line 2, column 1:
*** \def: missing macro body
"""
def test_8(capsys):
    capsys.readouterr()
    toks = p.parse(latex_8, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    cap = capsys.readouterr()
    assert plain == plain_8
    assert cap.err == stderr_8

latex_9 = r"""
\def\xxx#1#3{}
"""
plain_9 = """
 LATEXXXERROR 
"""
stderr_9 = r"""*** LaTeX error: code in 't.tex', line 2, column 11:
*** \def: unexpected argument '#3'
"""
def test_9(capsys):
    capsys.readouterr()
    toks = p.parse(latex_9, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    cap = capsys.readouterr()
    assert plain == plain_9
    assert cap.err == stderr_9

latex_10 = r"""
\def\xxx#1{#3}
"""
plain_10 = """
 LATEXXXERROR 
"""
stderr_10 = r"""*** LaTeX error: code in 't.tex', line 2, column 12:
*** \def: illegal argument reference '#3'
"""
def test_10(capsys):
    capsys.readouterr()
    toks = p.parse(latex_10, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    cap = capsys.readouterr()
    assert plain == plain_10
    assert cap.err == stderr_10

