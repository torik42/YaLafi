#
#   tex2txt.py:
#   test of introductory example from README.md
#

from yalafi import tex2txt

latex = r"""
\usepackage{xcolor}
Only few people\footnote{We use
\textcolor{red}{redx colour.}}
is lazy.
"""

plain_t = r"""
Only few people
is lazy.



We use
redx colour.
"""

options = tex2txt.Options(lang='en', char=True)
plain, nums = tex2txt.tex2txt(latex, options)

def test_text():
    assert plain == plain_t

