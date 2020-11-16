
from tests.test_issues import issues

latex_1 = r"""
A
\usepackage{
    amsthm,,
    tikz}
\tikzset{tikz}
B
\begin{proof}[Proof of Theorem 1]
"""
plain_1 = """
A
B


Proof of Theorem 1.

"""
def test_1():
    plain = issues.get_plain(latex_1)
    assert plain == plain_1

