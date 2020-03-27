
#
#   test of punctuation marks at \item
#

from yalafi import defs, parameters, parser, utils

latex_1 = r"""
A
\item
B.
\item[1)]C
\item[2)]D.
\item[$\alpha$)] E
"""
plain_1 = r"""
A
  B.
 1). C
 2) D.
 C-C-C).  E
"""
def test_1():
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain

latex_2 = r"""
\item
X.
\item[1)]
Y
"""
plain_2 = r"""
 * X.
 1) 
Y
"""
def test_2():
    parms = parameters.Parameters()
    parms.item_default_label = '*'
    parms.item_punctuation = []
    p = parser.Parser(parms)
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_2 == plain

