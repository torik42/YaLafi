#
#   test yalafi.shell with input encoding, option --encoding
#

from tests.test_shell_cmd import run_shell

latex = 'Случайный текст на руусском.'

json = r"""
{"software":{"name":"LanguageTool","version":"4.7","buildDate":"2019-09-28 10:09","apiVersion":1,"premium":false,"premiumHint":"You might be missing errors only the Premium version can find. Contact us at support<at>languagetoolplus.com.","status":""},"warnings":{"incompleteResults":false},"language":{"name":"Russian","code":"ru-RU","detectedLanguage":{"name":"Russian","code":"ru-RU","confidence":1.0}},"matches":[{"message":"Найдена орфографическая ошибка","shortMessage":"Орфографическая ошибка","replacements":[{"value":"русском"}],"offset":19,"length":8,"context":{"text":"Случайный текст на руусском. ","offset":19,"length":8},"sentence":"Случайный текст на руусском.","type":{"typeName":"Other"},"rule":{"id":"MORFOLOGIK_RULE_RU_RU","description":"Проверка орфографии с исправлениями","issueType":"misspelling","category":{"id":"TYPOS","name":"Проверка орфографии"}},"ignoreForIncompleteSentence":false,"contextForSureMatch":0}]}
"""

msg_cyrillic = r"""1.) Line 1, column 20, Rule ID: MORFOLOGIK_RULE_RU_RU
Message: Найдена орфографическая ошибка
Suggestion: русском
Случайный текст на руусском. 
                   ^^^^^^^^

"""

def test_shell_cyrillic_utf8():
    out = run_shell.run_shell('--language ru-RU', latex, 'utf-8', json)
    assert out == run_shell.msg_header + msg_cyrillic

def test_shell_cyrillic_cp866():
    out = run_shell.run_shell('--language ru-RU --encoding cp866',
                                        latex, 'cp866', json)
    assert out == run_shell.msg_header + msg_cyrillic

