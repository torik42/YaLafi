
#
#   test of extraction for macro arguments
#

from yalafi import defs, parameters, parser, utils


latex_1 = r"""
X
\xxx[y]{file_in.tex}
Y
"""
plain_1_1 = r"""
X
file_in.tex
Y
"""
plain_1_2 = r"""


file_in.tex
"""
def test_1():
    parms = parameters.Parameters()
    parms.macro_defs_python.append(defs.Macro(parms,
                                    '\\xxx', args='*OA', repl='#3'))
    p = parser.Parser(parms)

    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1_1 == plain

    toks = p.parse(latex_1, extract=['\\xxx'])
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1_2 == plain


# test for issue #1
#
latex_2 = r"""
\xxx A
"""
plain_2 = r"""
aXb



abA
"""
def test_2():
    parms = parameters.Parameters()
    parms.macro_defs_python.append(defs.Macro(parms,
                                    '\\xxx', args='OA', repl='a#1b',
                                    defaults=['X'], extract='a#1b#2'))
    p = parser.Parser(parms)
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_2 == plain

