

import pytest
from yalafi import parameters, parser, utils

preamble = '\\usepackage{tikz}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    return plain


data_test_macros_latex = [

    (r'A\tikzset{X}B', 'AB'),
    (r'A\usetikzlibrary XB', 'AB'),
    (
r"""
A
\begin{tikzpicture}

\draw (0,0) -- (2, 2);

\end{tikzpicture}
B
""",
r"""
A
B
"""
    ),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

