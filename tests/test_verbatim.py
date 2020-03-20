
#
#   tex2txt.py:
#   - test of \verb and \begin{verbatim}
#

import tex2txt

options = tex2txt.Options(lang='en', char=True)

def test_verb():

    latex = '\\verb?%x\\y?\\label{z}?'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == '%x\\y?'


def test_verbatim():

    # extra blank lines: see LAB:VERBATIM in tex2txt.py
    latex = 'A\\begin{verbatim}\\verb?%\\x?\n\\end{verbatim}B'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'A\n\n\\verb?%\\x?\n\n\nB'

