
#
#   YaLafi module for LaTeX package babel
#

#   map between language codes for babel and LanguageTool
#   - sorted according to xx-XX code
#
language_map = {
#   'ar'
#   'ast-ES'
    'belarusian': 'be-BY',
    'breton': 'br-FR',
    'catalan': 'ca-ES',
#   'ca-ES-valencia'
    'danish': 'da-DK',
    'german': 'de-DE',
    'german-at': 'de-AT',
    'german-ch': 'de-CH',
    'greek': 'el-GR',
    'english': 'en-GB',
    'english-au': 'en-AU',
    'english-ca': 'en-CA',
    'british': 'en-GB',
    'english-gb': 'en-GB',
    'english-nz': 'en-NZ',
    'american': 'en-US',
    'english-us': 'en-US',
#   'en-ZA',
    'esperanto': 'eo',
    'spanish': 'es',
#   'fa',
    'french': 'fr',
#   'ga-IE'
    'galician': 'gl-ES',
    'italian': 'it',
    'japanese': 'ja-JP',
#   'km-KH'
    'dutch': 'nl',
#   'nl-BE'
    'polish': 'pl-PL',
    'portuguese': 'pt-PT',
#   'pt-AO'
    'portuguese-br': 'pt-BR',
#   'pt-MZ'
    'romanian': 'ro-RO',
    'russian': 'ru-RU',
    'slovak': 'sk-SK',
    'slovenian': 'sl-SI',
    'swedish': 'sv',
    'tamil': 'ta-IN',
#   'tl-PH'
    'ukrainian': 'uk-UA',
    'chinese': 'zh-CN',
}

from yalafi.defs import InitModule, Macro, LanguageToken

require_packages = []

def init_module(parser, options):
    parms = parser.parms

    macros_latex = ''

    macros_python = [

        Macro(parms, '\\foreignlanguage', args='OAA', repl=h_foreignlanguage),
        Macro(parms, '\\selectlanguage', args='A', repl=h_selectlanguage),

    ]

    environments = []

    inject_tokens = []
    if options:
        # set current language to the last in option list
        inject_tokens = [LanguageToken(0, lang=translate_lang(options[-1][0]),
                                                hard=True)]

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments, inject_tokens=inject_tokens)

def modify_language_map(babel, lt):
    language_map[babel] = lt

#   translate babel code to LanguageTool code
#
def translate_lang(lang):
    return language_map.get(lang, language_map['english'])

def h_foreignlanguage(parser, buf, mac, args, pos):
    lang = translate_lang(parser.get_text_expanded(args[1]).strip())
    return ([LanguageToken(pos, lang=lang)] + args[2]
                        + [LanguageToken(args[2][-1].pos, back=True)])

def h_selectlanguage(parser, buf, mac, args, pos):
    lang = translate_lang(parser.get_text_expanded(args[0]).strip())
    return [LanguageToken(pos, lang=lang, hard=True)]

