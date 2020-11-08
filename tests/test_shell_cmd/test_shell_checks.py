
#
#   - test yalafi.shell with options --single-letters
#     and --equation-punctuation
#
#   - test option --list-unknown
#

from tests.test_shell_cmd import run_shell

latex = r"""We have x
\[
    a = b
\]
Therefore, all is OK.
"""
encoding = 'utf-8'

json = r"""
{"software":{"name":"LanguageTool","version":"4.7","buildDate":"2019-09-28 10:09","apiVersion":1,"premium":false,"premiumHint":"You might be missing errors only the Premium version can find. Contact us at support<at>languagetoolplus.com.","status":""},"warnings":{"incompleteResults":false},"language":{"name":"English (GB)","code":"en-GB","detectedLanguage":{"name":"English (GB)","code":"en-GB","confidence":1.0}},"matches":[]}
"""

def test_shell_single_1():
    out = run_shell.run_shell('', latex, encoding, json)
    assert out == ''

msg_single = r"""1.) Line 1, column 9, Rule ID: PRIVATE::SINGLE_LETTER
Message: Single letter detected.
Suggestion: —
...We have x   V-V-V Therefore, all is OK. ...
           ^

"""

def test_shell_single_2():
    out = run_shell.run_shell('--single-letter V', latex, encoding, json)
    assert out == run_shell.msg_header + msg_single

msg_equation = r"""1.) Line 3, column 5, Rule ID: PRIVATE::EQUATION_PUNCTUATION
Message: Possibly incorrect punctuation after equation.
Suggestion: —
...We have x   V-V-V Therefore, all is OK. ...
               ^^^^^^^^^^^^^^^

"""

def test_shell_equation():
    out = run_shell.run_shell('--equation-punctuation all',
                                    latex, encoding, json)
    assert out == run_shell.msg_header + msg_equation


latex_unkn = r"""
A \xxxxxx
\begin{yyyyyyyy}
B
"""
msg_unkn = r"""\xxxxxx
yyyyyyyy
"""
def test_shell_unkn():
    out = run_shell.run_shell('--list-unknown', latex_unkn, encoding, json)
    assert out == run_shell.msg_header + msg_unkn

