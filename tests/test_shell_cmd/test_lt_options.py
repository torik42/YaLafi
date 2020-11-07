#
#   test options and input to LanguageTool that are sent by yalafi.shell
#   - here: option passing
#

import pytest
from tests.test_shell_cmd import run_shell

latex_in = r"""
$x$ $y$ $z$
"""

data_test_options = [
    ('', """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

C-C-C D-D-D E-E-E

"""),
    ('--disable ""', """
--json --encoding utf-8 --language en-GB -

C-C-C D-D-D E-E-E

"""),
    ('--disable x,y', """
--json --encoding utf-8 --language en-GB --disable x,y -

C-C-C D-D-D E-E-E

"""),
    ('--enable x,y --disable ""', """
--json --encoding utf-8 --language en-GB --enable x,y -

C-C-C D-D-D E-E-E

"""),
    ('--disablecategories x,y', """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE --disablecategories x,y -

C-C-C D-D-D E-E-E

"""),
    ('--enablecategories x,y', """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE --enablecategories x,y -

C-C-C D-D-D E-E-E

"""),
    ('--language ru-RU', """
--json --encoding utf-8 --language ru-RU --disable WHITESPACE_RULE -

В-В-В Г-Г-Г Д-Д-Д

"""),
    ('--lt-options "~--xx 1 --yy 2"', """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE --xx 1 --yy 2 -

C-C-C D-D-D E-E-E

"""),
    ('--plain-input', """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

$x$ $y$ $z$

"""),
]

@pytest.mark.parametrize('options,lt_in_expected', data_test_options)
def test_macros_latex(options, lt_in_expected):
    lt_in = run_shell.get_lt_in(options, latex_in, 'utf-8')
    assert lt_in == lt_in_expected
