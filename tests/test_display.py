
#
#   test of display math
#

from yalafi import parameters, parser, utils

latex_1 = r"""
\usepackage{amsmath}
A
\begin{align}
    a &= b \\
    -c &= d.
\end{align}
B
"""
plain_1 = r"""
A
  V-V-V  equal W-W-W
  W-W-W  equal X-X-X.
B
"""
def test_1():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain

latex_2 = r"""
\usepackage{amsmath}
\begin{align}
    a &= b, \\
    -c &= d
\end{align}
"""
plain_2 = r"""
  V-V-V  equal W-W-W,
  X-X-X  equal Y-Y-Y
"""
def test_2():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_2 == plain

latex_3 = r"""
\usepackage{amsmath}
\begin{align}
    a &= b \\
    & \quad -c \\
    & {} \cdot d \\
    & \mbox{} \times e.
\end{align}
"""
plain_3 = r"""
  V-V-V  equal W-W-W
     minus X-X-X
    times Y-Y-Y
    times Z-Z-Z.
"""
def test_3():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_3)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_3 == plain

latex_4 = r"""
\usepackage{amsmath}
\begin{align}
    a &= b \text{ for all $c$.} \\
    d &\ne e.
\end{align}
"""
plain_4 = r"""
  V-V-V  equal W-W-W for all C-C-C.
  X-X-X  equal Y-Y-Y.
"""
def test_4():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_4)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_4 == plain

latex_4a = r"""
\usepackage{amsmath}
\begin{align}
    a &= b \text{ for all $c$}. \\
    d &\ne e.
\end{align}
"""
plain_4a = r"""
  V-V-V  equal W-W-W for all C-C-C.
  X-X-X  equal Y-Y-Y.
"""
def test_4a():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_4a)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_4a == plain

latex_5 = r"""
\usepackage{amsmath}
\begin{align}
    a &= b \text{ for all } c. \\
    d &\ne e.
\end{align}
"""
plain_5 = r"""
  V-V-V  equal W-W-W for all X-X-X.
  Y-Y-Y  equal Z-Z-Z.
"""
def test_5():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_5)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_5 == plain

latex_6 = r"""
\usepackage{amsmath}
\begin{alignat}
{2}
    &- b
\end{alignat}
"""
plain_6 = r"""
    minus V-V-V
"""
def test_6():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_6)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_6 == plain

latex_7 = r"""
\begin{eqnarray}
    a: &-& b
\end{eqnarray}
"""
plain_7 = r"""
  V-V-V:  minus  W-W-W
"""
def test_7():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_7)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_7 == plain

latex_8 = r"""
\[
    \beta
\]
A
$$
    \Omega
$$
"""
plain_8 = r"""
  V-V-V
A
  W-W-W
"""
def test_8():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_8)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_8 == plain

latex_9 = r"""
\usepackage{.tests.defs}
\begin{flalign}
    x
\end{flalign}
A
\begin{flalign}
    y,
\end{flalign}
"""
plain_9 = r"""
  relation
A
  relation,
"""
def test_9():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_9)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_9 == plain

