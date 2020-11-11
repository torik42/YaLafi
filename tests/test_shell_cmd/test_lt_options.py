#
#   test options and input to LanguageTool that are sent by yalafi.shell
#   - here: option passing
#

import pytest
from tests.test_shell_cmd import run_shell

test_dir = 'tests/test_shell_cmd/'

latex_1 = r"""
$x$ $y$ $z$
"""

data_test_1 = [
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

@pytest.mark.parametrize('options,lt_in_expected', data_test_1)
def test_1(options, lt_in_expected):
    lt_in = run_shell.get_lt_in(options, latex_1, 'utf-8')
    assert lt_in == lt_in_expected

latex_2 = r"""
\begin{eqnarray}
    a &=& b.
\end{eqnarray}
"""
data_test_2 = [
    ('--multi-language', """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

  V-V-V  equal  W-W-W.

"""),
    ('--simple-equations', """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

  W-W-W.

"""),
]

@pytest.mark.parametrize('options,lt_in_expected', data_test_2)
def test_2(options, lt_in_expected):
    lt_in = run_shell.get_lt_in(options, latex_2, 'utf-8')
    assert lt_in == lt_in_expected


latex_3 = r"""
A
\begin{thm}
B
"""
lt_in_3 = """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

A


Theorem.
B

"""
def test_3():
    lt_in = run_shell.get_lt_in('--define ' + test_dir + 'defs.tex',
                                                latex_3, 'utf-8')
    assert lt_in == lt_in_3

latex_4 = r"""
\usepackage{babel}
\selectlanguage{german}
so dass
so

dass
"""
data_test_4 = [
    ('--language de-DE --multi-language', """
--json --encoding utf-8 --language de-DE --disable WHITESPACE_RULE -

sodass
so

dass

"""),
    # - replacement is not performed
    # - the initial line break is omitted, since it belongs to the English
    #   text that is only space
    ('--language en-GB --multi-language', """
--json --encoding utf-8 --language de-DE --disable WHITESPACE_RULE -
so dass
so

dass

"""),
]
@pytest.mark.parametrize('options,lt_in_expected', data_test_4)
def test_4(options, lt_in_expected):
    repl = test_dir + 'repls.txt'
    lt_in = run_shell.get_lt_in(options + ' --replace ' + repl,
                                            latex_4, 'utf-8')
    assert lt_in == lt_in_expected

#   test --add-modules
#
latex_5 = r"""
\KOMAoption{koma}
\selectlanguage{lang}
A
"""
lt_in_5 = """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

A

"""
def test_5():
#   this will echo 'koma' and 'lang':
#   lt_in = run_shell.get_lt_in('--packages ""', latex_5, 'utf-8')
    lt_in = run_shell.get_lt_in('--packages "" --add-modules '
                                + test_dir + 'modules.tex', latex_5, 'utf-8')
    assert lt_in == lt_in_5

