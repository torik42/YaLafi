
#
#   tex2txt.py:
#   test of LaTeX comments
#

import tex2txt

options = tex2txt.Options(lang='en', char=True)

#   compare LAB:COMMENTS in tex2txt.py
#
def test_latex_comments():

    # "normal" comment
    latex = 'a %x\nb\n'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a b\n'
    assert nums == [1, 2, 6, 7]

    # join lines
    latex = 'a%x\n  b\n'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'ab\n'
    assert nums == [1, 7, 8]

    # join lines: protect macro name
    latex = 'a\\aa%x\nb\n'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'aåb\n'
    assert nums == [1, 2, 8, 9]

    # do not join lines, if next line empty
    latex = 'a%x\n\nb\n'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a\n\nb\n'
    assert nums == [1, 4, 5, 6, 7]

    # remove pure comment lines
    latex = 'a %x\n %x\nb\n'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'a b\n'
    assert nums == [1, 2, 10, 11]

