
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


latex_11 = r"""
\usepackage{amsmath}
A
\begin{multline}
    a = b \\
    - c.
\end{multline}
B
"""
plain_11 = r"""
A
  V-V-V
   minus W-W-W.
B
"""
def test_11():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_11)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_11 == plain


latex_12 = r"""
\usepackage{amsmath}
A
\begin{multline}
    a = b \\
    c.
\end{multline}
B
"""
plain_12 = r"""
A
  V-V-V
  V-V-V.
B
"""
def test_12():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_12)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_12 == plain


latex_13 = r"""
\usepackage{amsmath}
A
\begin{align}
    a &=
    \begin{multlined}[t]
    b \\
    + c.
    \end{multlined}
\end{align}
B
"""
plain_13 = r"""
A
  V-V-V  equal   W-W-W
   plus X-X-X.
B
"""
def test_13():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_13)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_13 == plain


latex_14 = r"""
\usepackage{amsmath}
A
\begin{align}
    a &=
    \begin{aligned}[t]
    \end{aligned}
\end{align}
B
"""
plain_14 = r"""
A
  V-V-V  equal   
B
"""
def test_14():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_14)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_14 == plain


latex_15 = r"""
\usepackage{amsmath}
A
\begin{align}
    a &=
    \begin{aligned}[t]
    & c \\
    &+ d.
    \end{aligned}
\end{align}
B
"""
plain_15 = r"""
A
  V-V-V  equal    W-W-W
    plus X-X-X.
B
"""
def test_15():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_15)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_15 == plain


latex_16 = r"""
\usepackage{amsmath}
A
\begin{equation}
    a
    = \begin{aligned}[t]
    & c \\
    &+ d.
    \end{aligned}
\end{equation}
B
"""
plain_16 = r"""
A
  X-X-X   V-V-V
    plus W-W-W.
B
"""
def test_16():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_16)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_16 == plain


latex_17 = r"""
\usepackage{amsmath}
A
\begin{equation}
    a=\begin{cases}
    0&  \text{if something},\\
    1&  \text{else}.
\end{cases}
\end{equation}
B
"""
plain_17 = r"""
A
  V-V-V if something,
  W-W-W else.
B
"""
def test_17():
    p = parser.Parser(parameters.Parameters())
    toks = p.parse(latex_17)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_17 == plain


#   simplified equation parsing
#
latex_10 = r"""
\usepackage{amsmath}
\begin{align}
    a &= b.
\end{align}
"""
plain_10 = r"""
  W-W-W.
"""
def test_10():
    parms = parameters.Parameters()
    parms.math_displayed_simple = True
    p = parser.Parser(parms)
    toks = p.parse(latex_10)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_10 == plain

