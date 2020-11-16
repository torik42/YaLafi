

import pytest
from yalafi import parameters, parser, utils

preamble = '\\usepackage{listings}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_latex = [

    (r'A\lstinputlisting[opts]{file}B', 'A\n\nB'),
    (r'A\lstset{opts}B', 'AB'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected


data_test_environments = [

    (r'A\begin{lstlisting}[opts]xxx\end{lstlisting}B', 'A\n\n\nB'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_environments)
def test_environments(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

