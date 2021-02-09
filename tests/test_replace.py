
#
#   test of phrase replacements
#

from yalafi import parameters, parser, utils


parms = parameters.Parameters()
p = parser.Parser(parms)

latex_1 = r"""
so
dass
1so dass
so dass1
so

dass
"""
plain_1 = r"""
sodass
1so dass
so dass1
so

dass
"""
def test_1():
    repls = ['so dass & sodass']
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    plain, pos = utils.replace_phrases(plain, pos, repls)
    assert plain_1 == plain

