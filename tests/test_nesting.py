
#
#   tex2txt.py:
#   - test of nesting for macros
#   - test of nesting for environments with replacement
#

from yalafi import tex2txt

options = tex2txt.Options(lang='en', char=True)

def test_nested_macro():

    latex = '\\textcolor{x}{\\textcolor{y}{z}}'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'z'


def test_nested_table():

    latex = '\\begin{table}A\\begin{table}B\\end{table}C\\end{table}'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == '\n\n[Tabelle]\n\n'

    latex = '\\begin{table}A\\begin{tablx}B\\end{table}C\\end{table}'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == '\n\n[Tabelle]\n\nC\n\n'

