
#
#   tests for extension modules
#

from yalafi import parameters, parser, tex2txt, utils

latex_1 = r"""
\begin{align}x\end{align}
"""
plain_1 = r"""
x
"""
def test_1():
    plain, nums = tex2txt.tex2txt(latex_1, tex2txt.Options())
    assert plain == plain_1

latex_2 = r"""
\usepackage{amsmath}
\begin{align}x\end{align}
"""
plain_2 = r"""
  V-V-V
"""
def test_2():
    plain, nums = tex2txt.tex2txt(latex_2, tex2txt.Options())
    assert plain == plain_2

latex_3 = r"""
\begin{align}x\end{align}
"""
plain_3 = r"""
  V-V-V
"""
def test_3():
    plain, nums = tex2txt.tex2txt(latex_3, tex2txt.Options(pack='*'))
    assert plain == plain_3

latex_4 = r"""
\begin{align}x\end{align}
"""
plain_4 = r"""
  V-V-V
"""
def test_4():
    plain, nums = tex2txt.tex2txt(latex_4,
                                    tex2txt.Options(pack='.tests.defs'))
    assert plain == plain_4

latex_5 = r"""
\LTinput {z.tex}
\begin{align}x\end{align}
"""
plain_5 = r"""
  V-V-V
"""
def test_5():
    def read(file):
        return True, r'\usepackage{amsmath}'
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_5)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_5 == plain

