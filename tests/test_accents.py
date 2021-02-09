
#
#   test of text-mode accents
#

from yalafi import parameters, parser, utils

p = parser.Parser(parameters.Parameters())

latex_1 = r"""
\'e
\'{e}
\'{ee}
\'{}e
"""
plain_1 = r"""
é
é
ée
´e
"""
def test_1():
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain

