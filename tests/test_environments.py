
#
#   test  of environments
#

from yalafi import defs, parameters, parser, utils

p = parser.Parser(parameters.Parameters('de'))

latex_proof = r"""
\usepackage{amsthm}
1\begin{proof}
2\end{proof}3

A\begin{proof}B\end{proof}C

X\begin{proof}[Proof]Y\end{proof}Z
"""
plain_proof_should_be = r"""
1

Beweis.
2

3

A

Beweis.
B

C

X

Proof.
Y

Z
"""
def test_proof():
    toks = p.parse(latex_proof)
    plain_proof, pos = utils.get_txt_pos(toks)

    assert plain_proof_should_be == plain_proof

latex_table = r"""
A\begin{table}B\end{table}C
"""
plain_table_should_be = r"""
A

[Tabelle]

C
"""
def test_table():
    toks = p.parse(latex_table)
    plain_table, pos = utils.get_txt_pos(toks)

    assert plain_table_should_be == plain_table

latex_comment = r"""
\usepackage{.tests.defs}
A\begin{comment}B\end{comment}C
X
\begin{comment}
Y
\end{comment}
Z
"""
plain_comment_should_be = r"""
AC
X
Z
"""
def test_comment():
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    toks = p.parse(latex_comment)
    plain_comment, pos = utils.get_txt_pos(toks)

    assert plain_comment_should_be == plain_comment

latex_unknown = r"""
A\begin{x}B\end{x}C
X
\begin{x}
Y
\end{x}
Z
"""
plain_unknown_should_be = r"""
ABC
X
Y
Z
"""
def test_unknown():
    toks = p.parse(latex_unknown)
    plain_unknown, pos = utils.get_txt_pos(toks)

    assert plain_unknown_should_be == plain_unknown

latex_macro_in_arg = r"""
\usepackage{xcolor}
X\begin{XXX}{\textcolor}
{red}{blue}
"""
plain_macro_in_arg = r"""
Xblue
"""
def test_macro_in_arg():
    parms = parameters.Parameters()
    parms.environment_defs.append(defs.Environ(parms, 'XXX',
                        args='A', repl='#1', add_pars=False))
    p = parser.Parser(parms)
    toks = p.parse(latex_macro_in_arg)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_macro_in_arg == plain

