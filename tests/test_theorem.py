
#
#   test  of environments
#

from yalafi import parameters, parser, utils

p = parser.Parser(parameters.Parameters())

latex_theorem = r"""
A\begin{theorem}B\end{theorem}C

X\begin{theorem}[T]Y\end{theorem}Z
"""
plain_theorem = r"""
A

Theorem.
B

C

X

Theorem (T).
Y

Z
"""
def test_theorem():
    toks = p.parse(latex_theorem)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_theorem == plain


latex_option = r"""
X\begin{theorem}[\textcolor{red}{blue}]Y
"""
plain_option = r"""
X

Theorem (blue).
Y
"""
def test_option():
    toks = p.parse(latex_option)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_option == plain

