

import pytest
from yalafi import parameters, parser, utils

preamble = '\\usepackage{amsthm}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_latex = [

    (r'A\[\qedhere\]B', 'A  B'),
            # the space is due to leading '  ' in displayed equations
    (r'A\theoremstyle{plain}B', 'AB'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected


data_test_environments = [

    ('A\\begin{proof}[Proof to X]\nB', 'A\n\nProof to X.\n\nB'),
    ('A\\begin{proof}\nB', 'A\n\nProof.\nB'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_environments)
def test_environments(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

