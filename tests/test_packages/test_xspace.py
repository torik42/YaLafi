

import pytest
from yalafi import parameters, parser, utils

preamble = '\\usepackage{xspace}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


footnote_latex = r'A\xspace\footnote{This is a footnote.} B'
footnote_plain = r"""A B


This is a footnote.
"""

data_test_macros_latex = [

    (r'A\xspace B', 'A B'),
    (r'A\xspace $x\xspace$ B', 'A C-C-C B'),
    (r'A\xspace {}$x\xspace$B', 'AC-C-CB'),
    (r'A\xspace~B', 'A\N{NO-BREAK SPACE}B'),
    (r"A\xspace's B", "A's B"),
    (r"A\xspace'' B", 'A” B'),
    (r'A\xspace-- B', 'A\N{EN DASH} B'),
    (r'A\xspace--- B', 'A\N{EM DASH} B'),
    (footnote_latex, footnote_plain),
    (r'A\xspace\footnotemark B', 'AB'),
    (r'\def\x{X\xspace}\x A', 'X A'),
    (r'\def\x{X\xspace}\x{}A', 'XA'),
    (r'\def\x{X\xspace}{\x}A', 'XA'),
    (r'\def\x{X\xspace}\x {A}', 'XA'),

]

xspace_excl = ['.', ',', "'", '/', '?', ';', ':', '!', '-', ')']

for i in xspace_excl:
    left = r'A\xspace' + i + r' B'
    right = r'A' + i + r' B'
    data_test_macros_latex.append((left, right))


@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

