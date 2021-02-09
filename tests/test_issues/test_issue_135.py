
import pytest
from tests.test_issues import issues

preamble = '\\usepackage{.tests.test_issues.defs_issue_135}\n'

data_test_macros_latex = [

    (r'\xyz AB', '011FalseFalse'),
    (r'\xyz []AB', '111FalseFalse'),
    (r'\xyz [o]AB', '111FalseFalse'),
    (r'\xyz A', '011FalseTrue'),
    (r'\xyz {}A', '011TrueFalse'),
    (r'\xyz A{}', '011FalseTrue'),
    (r'\xyz {}{AB}', '012TrueFalse'),
    (r'\xyz A', '011FalseTrue'),
    (r'{\xyz A}', '011FalseTrue'),
    (r'{\xyz}', '011TrueTrue'),
    (r'{\xyz[]}', '111TrueTrue'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = issues.get_plain(preamble + latex)
    assert plain == plain_expected
