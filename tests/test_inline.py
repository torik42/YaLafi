
#
#   test of inline math
#

from yalafi import parameters, parser, utils

latex_1 = r"""
X $
\alpha;
$ Y
"""
plain_1 = r"""
X C-C-C; Y
"""
def test_1():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain

latex_2 = r"""
X$ \negmedspace\alpha\;$Y
"""
plain_2 = r"""
XC-C-C Y
"""
def test_2():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_2 == plain

latex_3 = r"""
\usepackage{amsmath}
X \( f(n)=0 \text{ for all}\medspace n \) Y
"""
plain_3 = r"""
X C-C-C for all D-D-D Y
"""
def test_3():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_3)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_3 == plain

latex_4 = r"""
$y$
для $x$
"""
plain_4 = r"""
В-В-В
для Г-Г-Г
"""
def test_4():
    p = parser.Parser(parameters.Parameters(language='ru'))
    toks = p.parse(latex_4)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_4 == plain

