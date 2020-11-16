

import pytest
from yalafi import parameters, parser, utils

preamble = '\\usepackage{xcolor}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_latex = [

    (r'A\color{red}B', 'AB'),
    (r'A\color[rgb]{1,1,1}B', 'AB'),
    (r'A\colorbox{red}{blue}B', 'AblueB'),
    (r'A\colorbox[rgb]{1,1,1}{blue}B', 'AblueB'),
    (r'A\definecolor{xyz}{rgb}{1,1,1}B', 'AB'),
    (r'A\definecolor[named]{xyz}{rgb}{1,1,1}B', 'AB'),
    (r'A\textcolor{red}{blue}B', 'AblueB'),
    (r'A\textcolor[rgb]{1,1,1}{blue}B', 'AblueB'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected


data_test_macros_python = [

    (r'A\fcolorbox{red}{green}{blue}B', 'AblueB'),
    (r'A\fcolorbox[rgb]{1,1,1}[rgb]{5,5,5}{blue}B', 'AblueB'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_python)
def test_macros_python(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

