#
#   test yalafi.shell with different output formats, option --output
#

from tests.test_shell_cmd import run_shell
import sys

latex = 'This is ä testx.'
encoding = 'utf-8'

json = r"""
{"software":{"name":"LanguageTool","version":"4.7","buildDate":"2019-09-28 10:09","apiVersion":1,"premium":false,"premiumHint":"You might be missing errors only the Premium version can find. Contact us at support<at>languagetoolplus.com.","status":""},"warnings":{"incompleteResults":false},"language":{"name":"English (GB)","code":"en-GB","detectedLanguage":{"name":"English (GB)","code":"en-GB","confidence":1.0}},"matches":[{"message":"Possible spelling mistake found","shortMessage":"Spelling mistake","replacements":[{"value":"test"},{"value":"tests"},{"value":"testy"},{"value":"test x"}],"offset":10,"length":5,"context":{"text":"This is ä testx. ","offset":10,"length":5},"sentence":"This is ä testx.","type":{"typeName":"Other"},"rule":{"id":"MORFOLOGIK_RULE_EN_GB","description":"Possible spelling mistake","issueType":"misspelling","category":{"id":"TYPOS","name":"Possible Typo"}},"ignoreForIncompleteSentence":false,"contextForSureMatch":0}]}
"""

msg_plain = r"""1.) Line 1, column 11, Rule ID: MORFOLOGIK_RULE_EN_GB
Message: Possible spelling mistake found
Suggestion: test; tests; testy; test x
This is ä testx. 
          ^^^^^

"""

def test_shell_plain():
    out = run_shell.run_shell('', latex, encoding, json)
    assert out == run_shell.msg_header + msg_plain


if sys.version_info[:2] == (3, 6):
    msg_xml = r"""<matches>
<error category="Possible Typo" context="This is ä testx. " contextoffset="10" errorlength="5" fromx="10" fromy="0" msg="Possible spelling mistake found" replacements="test#tests#testy#test x" tox="15" toy="0" />
</matches>
"""
elif sys.version_info[:2] == (3, 8):
    msg_xml = r"""<matches>
<error fromy="0" fromx="10" toy="0" tox="15" category="Possible Typo" msg="Possible spelling mistake found" replacements="test#tests#testy#test x" context="This is ä testx. " contextoffset="10" errorlength="5" />
</matches>
"""

def test_shell_xml():
    out = run_shell.run_shell('--output xml', latex, encoding, json)
    assert out == msg_xml


#   multi-byte character 'ä' shifts column for mode xml-b
#
if sys.version_info[:2] == (3, 6):
    msg_xml_b = r"""<matches>
<error category="Possible Typo" context="This is ä testx. " contextoffset="11" errorlength="5" fromx="11" fromy="0" msg="Possible spelling mistake found" replacements="test#tests#testy#test x" tox="16" toy="0" />
</matches>
"""
elif sys.version_info[:2] == (3, 8):
    msg_xml_b = r"""<matches>
<error fromy="0" fromx="11" toy="0" tox="16" category="Possible Typo" msg="Possible spelling mistake found" replacements="test#tests#testy#test x" context="This is ä testx. " contextoffset="11" errorlength="5" />
</matches>
"""

def test_shell_xml_b():
    out = run_shell.run_shell('--output xml-b', latex, encoding, json)
    assert out == msg_xml_b


msg_json = r"""{"matches": [{"message": "Possible spelling mistake found", "shortMessage": "Spelling mistake", "replacements": [{"value": "test"}, {"value": "tests"}, {"value": "testy"}, {"value": "test x"}], "offset": 10, "length": 5, "context": {"text": "This is \u00e4 testx. ", "offset": 10, "length": 5}, "sentence": "This is \u00e4 testx.", "type": {"typeName": "Other"}, "rule": {"id": "MORFOLOGIK_RULE_EN_GB", "description": "Possible spelling mistake", "issueType": "misspelling", "category": {"id": "TYPOS", "name": "Possible Typo"}}, "ignoreForIncompleteSentence": false, "contextForSureMatch": 0, "priv": {"fromy": 0, "fromx": 10, "toy": 0, "tox": 15}}]}"""

def test_shell_json():
    out = run_shell.run_shell('--output json', latex, encoding, json)
    assert out == msg_json


msg_html = r"""<html>
<head>
<meta charset="UTF-8">
</head>
<body>
<a id="tests/test_shell_cmd/tmp/shell_in.tex"></a><H3>File&ensp;&quot;tests/test_shell_cmd/tmp/shell_in.tex&quot;&ensp;with&ensp;1&ensp;problem(s)</H3>
<table cellspacing="0">
<tr>
<td style="color: grey" align="right" valign="top">1&nbsp;&nbsp;</td>
<td>This&ensp;is&ensp;ä&ensp;<span style="background: orange; border: solid thin black" title="Possible&ensp;spelling&ensp;mistake&ensp;found
Line&ensp;1:&ensp;&gt;&gt;&gt;testx&lt;&lt;&lt;&ensp;&ensp;&ensp;&ensp;(Rule&ensp;ID:&ensp;MORFOLOGIK_RULE_EN_GB)
Suggestion: test;&ensp;tests;&ensp;testy;&ensp;test&ensp;x
Context: This&ensp;is&ensp;ä&ensp;&gt;&gt;&gt;testx&lt;&lt;&lt;.&ensp;">testx</span>.</td>
</tr>
<tr>
<td style="color: grey" align="right" valign="top">&nbsp;&nbsp;</td>
<td></td>
</tr>
</table>

</body>
</html>
"""

def test_shell_html():
    out = run_shell.run_shell('--output html', latex, encoding, json)
    assert out == msg_html

