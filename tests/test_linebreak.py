
#
#   test of \\[...] in text and math mode
#

from yalafi import parameters, parser, utils

latex_1 = r"""
A\\B
% add space, but do not remove line break
A\\
B
% do not create a blank line
A
\\
B
A\\
"""
plain_1 = r"""
A B
A 
B
A
B
A 
"""
def test_1():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain

latex_2 = r"""
A\\[5ex]B
A\\
[5ex]B
"""
plain_2 = r"""
A B
A B
"""
def test_2():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_2 == plain

latex_3 = r"""
\usepackage{amsmath}
\begin{align}
    a   &= b \\
        &= c \\[5ex]
% math mode: space before [...] not ignored
% --> [5ex] is seen as leading term on next line
        &= d \\ [5ex]
        &= e
\end{align}
"""
plain_3 = r"""
  V-V-V  equal W-W-W
    equal X-X-X
    equal Y-Y-Y
  Y-Y-Y  equal Z-Z-Z
"""
def test_3():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_3)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_3 == plain

