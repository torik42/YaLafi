
#
#   tex2txt.py:
#   - test of some macros from parms.system_macros
#

from yalafi import tex2txt

options = tex2txt.Options(lang='en', char=True)

def test_system_macros():

    latex = 'a\\footnote[2]{x}b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'ab\n\n\nx\n'


def test_renewcommand():

    latex = 'a\\newcommand\n{\\x}\n{y}b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'ab'

    latex = 'a\\newcommand{\\x}[1][z]{y}b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'ab'

    latex = 'a\\newcommand*{\\x}[1][z]{y}b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'ab'

    latex = 'a\\renewcommand{\\x}[1][z]{y}b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'ab'

    latex = 'a\\newcommand\n\n{\\x}[1]{y}b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a\n\n[1]yb'

    latex = 'a\\newcommand{\\x}\n\n[1]{y}b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a\n\n[1]yb'

    latex = 'a\\newcommand{\\x}[1]\n\n{y}b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a\n\nyb'

