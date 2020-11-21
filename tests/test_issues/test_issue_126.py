
from tests.test_issues import issues

latex_1 = r"""
A\begin{verbatim}\xxx\end{verbatim}B
"""
plain_1 = r"""
A

\xxx

B
"""
nums_1 = [0, 1, 18, 18, 18, 19, 20, 21, 22, 22, 36, 37
]
def test_1():
    plain, nums = issues.get_plain_pos(latex_1)
    assert plain == plain_1
    assert nums == nums_1

