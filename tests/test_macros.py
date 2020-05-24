
#
#   tex2txt.py:
#   - test of detection of macro arguments
#   - test of optional parameters for \cite, \begin{proof}
#   - test of optional parameter for \footnotemark
#   - treatment of unknown macros
#

from yalafi import tex2txt

options = tex2txt.Options(lang='en', char=True)

def test_macro_arguments():

    # normal expansion
    latex = '\\usepackage{xcolor}\n\\textcolor\n{red}\n{blue}'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'blue'
    assert nums == [39, 40, 41, 42]

    # no expansion: argument in next paragraph
    latex = '\\usepackage{xcolor}\\textcolor\n{red}\n \n{blue}'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == ' \nblue'

    # no expansion: argument in next paragraph
    latex = '\\usepackage{xcolor}\\textcolor\n\n{red}\n{blue}'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == '\nred\nblue'

    # expansion: comment line
    latex = '\\usepackage{xcolor}\\textcolor\n %x\n{red}\n{blue}'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'blue'


def test_cite():

    latex = '\\cite{x}'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == '[0]'

    latex = '\\cite[y]{x}'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == '[0, y]'


def test_proof():

    latex = '\\usepackage{amsthm}\n\\begin{proof}'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == '\n\nProof.\n'

    latex = '\\usepackage{amsthm}\nA \\begin{proof}[Test] B'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'A \n\nTest.\n B'
    assert nums == [21, 22, 23, 23, 37, 38, 39, 40, 40, 40, 42, 43]


def test_footnotemark():

    latex = 'a\\footnotemark b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'ab'

    latex = 'a\\footnotemark[1] b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a b'

    latex = 'a\\footnotemark\n[1]b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'ab'

    # do not cross paragraph border
    latex = '\\footnotemark\n\n[1]'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == '\n[1]'


def test_unknown_macro():

    latex = 'a\\xxx b'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'ab'

    latex = 'a\\xxx \n{b} c'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'ab c'


    latex = 'a\\xxx\n\n{b} c'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a\n\nb c'

