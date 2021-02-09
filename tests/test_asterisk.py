
#
#   test of asterisk in macro definition
#

from yalafi import defs, parameters, parser, utils


parms = parameters.Parameters()
parms.macro_defs_python.append(defs.Macro(parms,
                                        '\\xxx', args='*OA', repl='#1.#2.#3'))
p = parser.Parser(parms)

latex_1 = r"""
\xxx
*
A
\xxx[B]{A}
"""
plain_1 = r"""
*..A
.B.A
"""
def test_1():
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain

