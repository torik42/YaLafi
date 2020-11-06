#
#   test options and input to LanguageTool that are sent by yalafi.shell
#   - here: for multi-language support
#

from tests.test_shell_cmd import run_shell

#   without multi-lang
#
latex_1 = r"""
A \foreignlanguage{german}{B} C
"""
lt_in_1 = """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

A B C

"""
def test_1():
    lt_in = run_shell.get_lt_in('', latex_1, 'utf-8')
    assert lt_in == lt_in_1

#   with multi-lang
#
latex_2 = r"""
A \foreignlanguage{german}{B} C
"""
lt_in_2 = """
--json --encoding utf-8 --language de-DE --disable WHITESPACE_RULE -
B

--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

A L-L-L C

"""
def test_2():
    lt_in = run_shell.get_lt_in('--multi-language', latex_2, 'utf-8')
    assert lt_in == lt_in_2

#   with multi-lang, but --ml-continue-threshold 0
#
latex_3 = r"""
A \foreignlanguage{german}{B} C
"""
lt_in_3 = """
--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

A 

--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -
 C


--json --encoding utf-8 --language de-DE --disable WHITESPACE_RULE -
B
"""
def test_3():
    lt_in = run_shell.get_lt_in('--multi-language --ml-continue-threshold 0',
                                                latex_3, 'utf-8')
    assert lt_in == lt_in_3

#   with multi-lang and --ml-disable
#
latex_4 = r"""
A \foreignlanguage{german}{B} C
"""
lt_in_4 = """
--json --encoding utf-8 --language de-DE --disable WHITESPACE_RULE,x,y -
B

--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

A L-L-L C

"""
def test_4():
    lt_in = run_shell.get_lt_in('--multi-language --ml-disable x,y',
                                                latex_4, 'utf-8')
    assert lt_in == lt_in_4

#   with multi-lang and --ml-disable, but --ml-rule-thresh 0
#
latex_5 = r"""
A \foreignlanguage{german}{B} C
"""
lt_in_5 = """
--json --encoding utf-8 --language de-DE --disable WHITESPACE_RULE -
B

--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

A L-L-L C

"""
def test_5():
    lt_in = run_shell.get_lt_in('--multi-language --ml-disable x,y'
                                + ' --ml-rule-threshold 0', latex_5, 'utf-8')
    assert lt_in == lt_in_5

#   with multi-lang and --ml-disablecategories
#
latex_6 = r"""
A \foreignlanguage{german}{B} C
"""
lt_in_6 = """
--json --encoding utf-8 --language de-DE --disable WHITESPACE_RULE --disablecategories x,y -
B

--json --encoding utf-8 --language en-GB --disable WHITESPACE_RULE -

A L-L-L C

"""
def test_6():
    lt_in = run_shell.get_lt_in('--multi-language --ml-disablecategories x,y',
                                                latex_6, 'utf-8')
    assert lt_in == lt_in_6

