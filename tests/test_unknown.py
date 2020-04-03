
#
#   - test of option --unkn
#

from yalafi import tex2txt

options = tex2txt.Options(unkn=True)

latex_1 = r"""
A
\newcommand{\zzz}[1]{#1#1}
\xxx
\begin{\zzz Y}
B
"""
plain_1 = r"""\xxx
YY
"""
def test_1():
    plain, nums = tex2txt.tex2txt(latex_1, options)
    assert plain_1 == plain

