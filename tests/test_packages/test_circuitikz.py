

import pytest
from yalafi import parameters, parser, utils

preamble = '\\usepackage{circuitikz}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_latex = [

    (r'A\ctikzset{X}B', 'AB'),
    (r'A\usetikzlibrary XB', 'AB'),
    (
r"""
A
\begin{circuitikz}
	\ctikzset{voltage/bump b/.initial=0} % defines arrow's curvature
	\draw (0,3) to[short,o-*] (1,3) -- (1,3.5) to[R,l=$R$] (4,3.5) to[L=$L$] (7,3.5) -- (7,3) to[short,i=$I_{Last}$,*-] (9,3)
	to[R,l=$R_{Last}$] (9,0) to[short,-o] (0,0);
	\draw (1,3) -- (1,2.5) to[C,l_=$C$] (7,2.5) -- (7,3);
	\draw (0,3) to[open,v=$U_e$] (0,0);
\end{circuitikz}
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

