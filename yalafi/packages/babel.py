
#
#   YaLafi module for LaTeX package babel
#

#   do the macros / environments always break the text flow?
#
foreignlang_break = False
selectlang_break = True
otherlang_break = False

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
    'ngerman': 'de-DE',
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

from yalafi.defs import InitModule, Macro, LanguageToken, Environ, MacroToken

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = ''

    macros_python = [

        # the following is for \end{otherlanguage}
        Macro(parms, '\\babel@skip@space', args='', repl=''),
        Macro(parms, '\\foreignlanguage', args='OAA', repl=h_foreignlanguage),
        Macro(parms, '\\selectlanguage', args='A', repl=h_selectlanguage),

    ]

    environments = [

        Environ(parms, 'otherlanguage', args='A', repl=h_begin_otherlang,
                                add_pars=False, end_func=h_end_otherlang),
        Environ(parms, 'otherlanguage*', args='A', repl=h_begin_otherlang,
                                add_pars=False, end_func=h_end_otherlang_star),

    ]

    inject_tokens = get_language_token(parser.global_latex_options + options)

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments, inject_tokens=inject_tokens)

def modify_language_map(babel, lt):
    language_map[babel] = lt

#   translate babel code to LanguageTool code
#
def translate_lang(lang):
    return language_map.get(lang, language_map['english'])

def h_foreignlanguage(parser, buf, mac, args, delim, pos):
    lang = translate_lang(parser.get_text_expanded(args[1]).strip())
    return ([LanguageToken(pos, lang=lang, brk=foreignlang_break)] + args[2]
                        + [LanguageToken(args[2][-1].pos, back=True)])

def h_selectlanguage(parser, buf, mac, args, delim, pos):
    lang = translate_lang(parser.get_text_expanded(args[0]).strip())
    return [LanguageToken(pos, lang=lang, hard=True, brk=selectlang_break)]

def h_begin_otherlang(parser, buf, mac, args, delim, pos):
    lang = translate_lang(parser.get_text_expanded(args[0]).strip())
    return [LanguageToken(pos, lang=lang, brk=otherlang_break)]

def h_end_otherlang(parser, buf, mac, args, delim, pos):
    return [LanguageToken(pos, back=True),
                MacroToken(pos, '\\babel@skip@space')]

def h_end_otherlang_star(parser, buf, mac, args, delim, pos):
    return [LanguageToken(pos, back=True)]

#   return a list
#   - with LanguageToken corresponding to given option
#   - or empty, if no language option found
#
def get_language_token(options):
    for opt in reversed(options):
        if opt[1] is None and opt[0] in language_map:
            return [LanguageToken(0, lang=translate_lang(opt[0]),
                                                hard=True, brk=True)]
    return []

