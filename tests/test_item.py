
#
#   test of punctuation marks at \item
#   test of enumerate
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
    parms.item_default_label = ['*']
    parms.item_punctuation = []
    p = parser.Parser(parms)
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_2 == plain

latex_3 = r"""
\item A
\begin{enumerate}
\item B.
\item[x)] C
\item D
\begin{enumerate}
\item E
\item F
\end{enumerate}
\item G
\end{enumerate}
"""
plain_3 = r"""
 * A
 1. B.
 x).  C
 2. D
 a. E
 b. F
 3. G
"""
def test_3():
    parms = parameters.Parameters()
    parms.item_default_label = ['*']
    p = parser.Parser(parms)
    toks = p.parse(latex_3)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_3 == plain

latex_4 = r"""
\item A
\begin{itemize}
\item B
\begin{itemize}
\item C
\end{itemize}
\item D
\end{itemize}
E
"""
plain_4 = r"""
 * A
 * B
 - C
 * D
E
"""
def test_4():
    parms = parameters.Parameters()
    parms.item_default_label = ['*', '-']
    p = parser.Parser(parms)
    toks = p.parse(latex_4)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_4 == plain

