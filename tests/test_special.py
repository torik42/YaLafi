
#
#   test of macros like \LTadd
#

from yalafi import parameters, parser, utils


latex_1 = r"""
% these definitions should be ignored
\newcommand{\LTadd}[1]{}
\newcommand{\LTalter}[2]{#1}
\newcommand{\LTskip}[1]{#1}
A
\LTskip{X}
B\LTadd
YC
\LTalter
0
1
"""
plain_1 = r"""
A
BYC
1
"""
def test_1():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain

latex_2 = r"""
% this definition should be ignored
\newcommand{\LTinput}[1]{}
\LTinput {z.tex}
\xxx
Y
A\color XB
"""
plain_2 = r"""
 Y Y
AB
"""
def test_2():
    def read(file):
        return True, r'\usepackage{xcolor}\newcommand{\xxx}[1]{ #1 #1}'
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_2 == plain

latex_3 = r"""
A
%%% LT-SKIP-BEGIN
$$
%%% LT-SKIP-END
    B
C %%% LT-SKIP-BEGIN
$$
%%% LT-SKIP-END
D
E%%% LT-SKIP-BEGIN
$$
%%% LT-SKIP-END
F
G
%%% LT-SKIP-BEGIN
H
% missing LT-SKIP-END
"""
plain_3 = r"""
A
B
C D
EF
G
 LATEXXXERROR H
"""

def test_3():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_3)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_3 == plain

