import pytest
from yalafi import parameters, parser, utils


latex_1 = r"""
\usepackage{amsmath}
\usepackage{unicode-math}
A
\begin{align}
    a &≤ b \\
    -c &≥ d.
\end{align}
B
"""
plain_1 = r"""
A
  V-V-V  equal W-W-W
  W-W-W  equal X-X-X.
B
"""

def test_1():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain


latex_2 = r"""
\usepackage{amsmath}
\usepackage{unicode-math}
\begin{align}
    a &= b, \\
    -c &= d
\end{align}
"""
plain_2 = r"""
  V-V-V  equal W-W-W,
  X-X-X  equal Y-Y-Y
"""
def test_2():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_2 == plain


preamble = '\\usepackage{unicode-math}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_latex = [

    (r'\unimathsetup{math-style=TeX}', ''),
    (r'\setmathfont{MinionMath-Bold.otf}[range={bfup->up,bfit->it}]', '')

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected
