
#
#   test inclusion of error messages
#

from yalafi import parameters, parser, utils

parms = parameters.Parameters()
parms.mark_latex_error = 'LATEXXXERROR'

latex_1 = r"""
$
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
plain_1 = r"""
LATEXXXERROR (missing end of maths)C-C-C"""
def test_1():
    p = parser.Parser(parms)
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain

latex_2 = r"""
\verb?

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
plain_2 = r"""
LATEXXXERROR (bad \verb argument)

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
def test_2():
    p = parser.Parser(parms)
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_2 == plain

latex_3 = r"""
\begin{verbatim}
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
plain_3 = r"""
LATEXXXERROR (missing end of verbatim)verbatim
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
def test_3():
    p = parser.Parser(parms)
    toks = p.parse(latex_3)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_3 == plain

latex_4 = r"""
\textcolor{red}{
XXX
"""
plain_4 = r"""
LATEXXXERROR (cannot find closing })
XXX
"""
def test_4():
    p = parser.Parser(parms)
    toks = p.parse(latex_4)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_4 == plain

latex_5 = r"""
\' 
{1}
"""
plain_5 = r"""
LATEXXXERROR (text-mode accent for non-letter)
"""
def test_5():
    p = parser.Parser(parms)
    toks = p.parse(latex_5)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_5 == plain

latex_6 = r"""
\b y
"""
plain_6 = r"""
LATEXXXERROR (could not find UTF-8 character "LATIN SMALL LETTER Y WITH LINE BELOW")
"""
def test_6():
    p = parser.Parser(parms)
    toks = p.parse(latex_6)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_6 == plain

latex_7 = r"""
A
\newcommand{\xxx}[1]{#2}
B
"""
plain_7 = r"""
A
LATEXXXERROR (illegal argument #2 in definition of macro \xxx)
B
"""
def test_7():
    p = parser.Parser(parms)
    toks = p.parse(latex_7)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_7 == plain

latex_8 = r"""
A
\newcommand{\xxx}[0][ho]{}
B
"""
plain_8 = r"""
A
LATEXXXERROR (illegal default value in definition of macro \xxx)
B
"""
def test_8():
    p = parser.Parser(parms)
    toks = p.parse(latex_8)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_8 == plain

