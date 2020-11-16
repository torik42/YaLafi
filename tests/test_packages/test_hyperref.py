

import pytest
from yalafi import parameters, parser, utils

preamble = '\\usepackage{hyperref}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_latex = [

    (r'\href XY', 'Y'),
    (r'\href[O]XY', 'Y'),
    (r'\texorpdfstring XY', 'X'),
    (r'\url XY', 'XY'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

