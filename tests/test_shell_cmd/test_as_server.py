#
#   test of yalafi.shell running as HTTP server
#

from tests.test_shell_cmd import run_shell

latex_1 = r'This is a \xxx testx.'

# LT 's JSON answer to 'This is a testx.'
json_1 = r"""
{"software":{"name":"LanguageTool","version":"4.7","buildDate":"2019-09-28 10:09","apiVersion":1,"premium":false,"premiumHint":"You might be missing errors only the Premium version can find. Contact us at support<at>languagetoolplus.com.","status":""},"warnings":{"incompleteResults":false},"language":{"name":"English (GB)","code":"en-GB","detectedLanguage":{"name":"English (GB)","code":"en-GB","confidence":1.0}},"matches":[{"message":"Possible spelling mistake found","shortMessage":"Spelling mistake","replacements":[{"value":"test"},{"value":"tests"},{"value":"testy"},{"value":"test x"}],"offset":10,"length":5,"context":{"text":"This is a testx. ","offset":10,"length":5},"sentence":"This is a testx.","type":{"typeName":"Other"},"rule":{"id":"MORFOLOGIK_RULE_EN_GB","description":"Possible spelling mistake","issueType":"misspelling","category":{"id":"TYPOS","name":"Possible Typo"}},"ignoreForIncompleteSentence":false,"contextForSureMatch":0}]}
"""

msg_1 = """1.) Line 1, column 16, Rule ID: MORFOLOGIK_RULE_EN_GB
Message: Possible spelling mistake found
Suggestion: test; tests; testy; test x
This is a testx. 
          ^^^^^

"""

def test_single_lang():
    msg = run_shell.run_as_server('', latex_1, json_1)
    assert msg == run_shell.msg_header + msg_1

def test_multi_lang():
    msg = run_shell.run_as_server('--multi-language', latex_1, json_1)
    assert msg == run_shell.msg_header + msg_1

