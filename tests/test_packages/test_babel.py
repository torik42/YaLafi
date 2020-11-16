

import pytest
from yalafi import parameters, parser, utils

preamble = '\\usepackage{babel}\n'

def get_plain(latex):
    parms = parameters.Parameters('en')
    parms.multi_language = True
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_python = [

    (r'A\foreignlanguage{russian}{T}B', 'ATB'),
    (r'A\foreignlanguage[opt]{russian}{T}B', 'ATB'),
    (r'A\foreignlanguage{german}{ T }B', 'A T B'),
    (r"""
A
\foreignlanguage{german}{ }
B
""", r"""
A
B
"""),
    (r"""
\usepackage{amsthm}
\begin{proof}
\foreignlanguage{german}{\begin{proof}}
""", r"""


Proof.

Beweis.
"""),
    (r'A\selectlanguage{russian}B', 'AB'),
    (r"""
A
\selectlanguage{english}
B
""", r"""
A
B
"""),
    (r"""
\usepackage{amsthm}
\selectlanguage{german}
\begin{proof}
""", r"""


Beweis.
"""),
    # otherlanguage: skip space behind environment
    # otherlanguage*: do not do that
    #
    (r"""
A
\begin{otherlanguage}{german}
B
\end{otherlanguage} C
""", """
A
B
C
"""),
    (r"""
A
\begin{otherlanguage}{german}
B%
\end{otherlanguage}
C
""", """
A
BC
"""),
    (r"""
A
\begin{otherlanguage*}{german}
B
\end{otherlanguage*} C
""", """
A
B
 C
"""),
    (r"""
A
\begin{otherlanguage*}{german}
B%
\end{otherlanguage*}
C
""", """
A
B
C
"""),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_python)
def test_macros_python(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

