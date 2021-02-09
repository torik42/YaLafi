
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

#   test %%% LT-SKIP in text mode,
#
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
"""
plain_3 = r"""
A
B
C D
EF
"""
def test_3():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_3)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_3 == plain

#   %%% LT-SKIP: test on missing end
#
latex_4 = r"""
A
%%% LT-SKIP-BEGIN
B
% missing LT-SKIP-END
"""
plain_4 = r"""
A
 LATEXXXERROR B
"""
stderr_4 = r"""*** LaTeX error: code in 't.tex', line 3, column 1:
*** cannot find closing LaTeX comment '%%% LT-SKIP-END'
"""
def test_4(capsys):
    capsys.readouterr()
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_4, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    cap = capsys.readouterr()
    assert plain_4 == plain
    assert cap.err == stderr_4

#   test %%% LT-SKIP in math mode
#
latex_5 = r"""
A
\[
    \alpha, \\
%%% LT-SKIP-BEGIN
    \alpha \\
%%% LT-SKIP-END
\]
B
"""
plain_5 = r"""
A
  V-V-V,
B
"""
def test_5():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_5)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_5 == plain

#   test option --nosp
#
latex_6 = r"""
\LTadd{A}
\LTskip{B}
\LTalter CD
%%% LT-SKIP-BEGIN
X
%%% LT-SKIP-END
"""
plain_6 = """
B
C
X
"""

def test_6():
    parms =parameters.Parameters()
    parms.no_specials()
    p = parser.Parser(parms)
    toks = p.parse(latex_6)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_6 == plain


#   issue #169: catch infinite file recursion
#
latex_7 = r"""
\LTinput{t.tex}
"""
stderr_7 = r"""*** Problem while executing "\LTinput{t.tex}".
*** Is the file included recursively?
"""
def test_7(capsys):
    capsys.readouterr()
    def read(file):
        return True, '\\LTinput{t.tex}\n'
    try:
        parms = parameters.Parameters()
        p = parser.Parser(parms, read_macros=read)
        toks = p.parse(latex_7)
    except SystemExit:
        # catch exit() in the error routine utils.fatal()
        pass
    captured = capsys.readouterr()
    # remove first message line: it contains the name of Python
    err = '\n'.join(captured.err.split('\n')[1:])
    assert stderr_7 == err


latex_8 = r"""
A\LTinput{t.tex}B
"""
plain_8 = r"""
A LATEXXXERROR B
"""
stderr_8 = r"""*** LaTeX error: code in 't.tex', line 2, column 2:
*** could not read file 't.tex'
"""
def test_8(capsys):
    capsys.readouterr()
    def read(file):
        return False, ''
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_8, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    captured = capsys.readouterr()
    assert plain_8 == plain
    assert stderr_8 == captured.err


latex_9 = r"""
\LTinput{s.tex}
A\label
{B
"""
plain_9 = r"""
A LATEXXXERROR B
"""
stderr_9 = r"""*** LaTeX error: code in 's.tex', line 1, column 1:
*** missing end of maths
*** LaTeX error: code in 't.tex', line 4, column 1:
*** cannot find closing "}"
"""
def test_9(capsys):
    capsys.readouterr()
    def read(file):
        return True, r'$'
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_9, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    captured = capsys.readouterr()
    assert plain_9 == plain
    assert stderr_9 == captured.err

