

import pytest
from yalafi import parameters, parser, utils

preamble = '\\usepackage{amsmath}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_latex = [

    (r'\eqref{e}', '(0)'),
    (r'A\medspace B', 'A B'),
    (r'A\[\negmedspace\]B', 'A  B'),
            # the space is due to leading '  ' in displayed equations
    (r'A\[\negthickspace\]B', 'A  B'),
    (r'A\[\negthinspace\]B', 'A  B'),
    (r'A\[\notag\]B', 'A  B'),
    (r'A\numberwithin{x}{y}B', 'AB'),
    (r'A\thickspace B', 'A B'),
    (r'A\thinspace B', 'A\N{NARROW NO-BREAK SPACE}B'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected


data_test_macros_python = [

    (r'A\DeclareMathOperator*xy B', 'A B'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_python)
def test_macros_python(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

