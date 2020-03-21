
#
#   tex2txt.py:
#   test of removal of blank lines left by macros
#

from yalafi import tex2txt

options = tex2txt.Options(lang='en', char=True)

def test_remove_blank_lines_left_by_macros():

    # a normal macro: \label
    latex = 'a\n\\label{x}\nb\n'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a\nb\n'
    assert nums == [1, 2, 13, 14]

    # macro plus comment
    latex = 'a\n\\label{x} %x\nb\n'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a\n b\n'
    assert nums == [1, 2, 12, 16, 17]

    # \begin and \end
    latex = 'a\n\\begin{x}\nb\n\\end{x}\nc\n'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a\nb\nc\n'
    assert nums == [1, 2, 13, 14, 23, 24]

    # (actually no blank lines)
    latex = 'a\n\\begin{x}b\n\\end{x}c\n'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a\nb\nc\n'
    assert nums == [1, 2, 12, 13, 21, 22]

