#
#   YaLafi: Yet another LaTeX filter
#   Copyright (C) 2020 Matthias Baumann
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""
   Default parameters for scanner and parser.

   Includes: standard LaTeX macros and environments, language settings,
   math material settings.
"""

from yalafi.defs import Environ, EquEnv, Macro
from yalafi import handlers as hs
from yalafi import scanner


class Parameters:
    """
    Default settings for parser.

    Attributes:
        macro_defs_latex: 
        macro_defs_python: 
        environment_defs: 
        parser_lang_settings: Dictionary with language settings.
          The keys are language codes like ``en`` or ``de``. And the
          values are :class:`ParserLanguageSetting` objects.
        parser_lang_stack: 
        lang_context: 
        heading_punct: 
        item_default_label: 
        item_punctuation: 
        mark_latex_error: 
        mark_latex_error_verbose: 
        macro_filter_add: 
        macro_filter_alter: 
        macro_filter_skip: 
        macro_load_defs: 
        newcommand_ignore: 
        comment_skip_begin: 
        comment_skip_end: 
        class_modules: 
        package_modules: 
        accent_macros: 
        special_tokens: 
        math_displayed_simple: 
        math_ignore: 
        math_space: 
        math_operators: 
        math_text_macros: 
        math_default_env: 
        math_punctuation: 
        multi_language: 
        ml_continue_thresh: 
        scanner: 
        proof_name: 
        math_repl_inline: 
        math_repl_inline_vowel: 
        math_repl_display: 
        math_repl_display_vowel: 
        math_op_text: 
        lang_change_repl: 
        lang_change_repl_vowel: 
        short_macros: 
        active_chars: 
    """

    def init_macros(self):
        """Initialize standard, default LaTeX macros."""

        # LaTeX macro definition as LaTeX code
        self.macro_defs_latex = r"""

        \newcommand{\AA}{Å}
        \newcommand{\aa}{å}
        \newcommand{\AE}{Æ}
        \newcommand{\addtocounter}[2]{}
        \newcommand{\ae}{æ}
        \newcommand{\author}[1]{#1.}
        \newcommand{\bibitem}[1]{\item}
        \newcommand{\bibliographystyle}[1]{}
        \newcommand{\footnotemark}[1][]{}
        \newcommand{\hfill}{ }
        \newcommand{\include}[1]{}
        \newcommand{\includeonly}[1]{}
        \newcommand{\index}[1]{}
        \newcommand{\input}[1]{}
        \newcommand{\L}{Ł}
        \newcommand{\l}{ł}
        \newcommand{\label}[1]{}
        \newcommand{\LaTeX}{LaTeX}
        \newcommand{\newcounter}[1]{}
        \newcommand{\newline}{ }
        \newcommand{\nobreakspace}{~}
        \newcommand{\O}{Ø}
        \newcommand{\o}{ø}
        \newcommand{\OE}{Œ}
        \newcommand{\oe}{œ}
        \newcommand{\pagenumbering}[1]{}
        \newcommand{\pageref}[1]{0}
        \newcommand{\pagestyle}[1]{}
        \newcommand{\par}{

}
        \newcommand{\qquad}{\;}
        \newcommand{\quad}{\;}
        \newcommand{\ref}[1]{0}
        \newcommand{\refstepcounter}[1]{}
        \newcommand{\S}{§}
        \newcommand{\setcounter}[2]{}
        \newcommand{\ss}{ß}
        \newcommand{\stepcounter}[1]{}
        \newcommand{\TeX}{TeX}
        \newcommand{\textasciicircum}{\verb?^?} % \^ is accent
        \newcommand{\textasciitilde}{\verb?~?}  % \~ is accent
        \newcommand{\textbackslash}{\verb?\?}   % \\ is line break
        \newcommand{\thispagestyle}[1]{}
        \newcommand{\vphantom}[1]{}

        """

        # LaTeX macro definition as Python code
        #
        self.macro_defs_python = [

        Macro(self, '\\caption', args='OA', extract='#2'),
        Macro(self, '\\chapter', args='*OA', repl=hs.h_heading),
        Macro(self, '\\cite', args='OA', repl=hs.h_cite),
        Macro(self, '\\documentclass', args='OA',
                            repl=hs.h_load_module(self.class_modules)),
        Macro(self, '\\footnote', args='OA', extract='#2'),
        Macro(self, '\\footnotetext', args='OA', extract='#2'),
        Macro(self, '\\framebox', args='OOA', repl='#3'),
        Macro(self, '\\hphantom', args='A', repl=hs.h_phantom),
        Macro(self, '\\linebreak', args='O', repl=hs.h_linebreak),
        Macro(self, '\\hspace', args='*A', repl=hs.h_hspace),
        Macro(self, '\\MakeLowercase', args='A', repl=hs.h_makeLowercase),
        Macro(self, '\\MakeUppercase', args='A', repl=hs.h_makeUppercase),
        Macro(self, '\\newcommand', args='*AOOA', repl=hs.h_newcommand),
        Macro(self, '\\newtheorem', args='AOAO', repl=hs.h_newtheorem),
        Macro(self, '\\paragraph', args='*OA', repl=hs.h_heading),
        Macro(self, '\\part', args='*OA', repl=hs.h_heading),
        Macro(self, '\\phantom', args='A', repl=hs.h_phantom),
        Macro(self, '\\providecommand', args='*AOOA', repl=hs.g_newcommand(overwrite=False)),
        Macro(self, '\\renewcommand', args='*AOOA', repl=hs.h_newcommand),
        Macro(self, '\\section', args='*OA', repl=hs.h_heading),
        Macro(self, '\\subsection', args='*OA', repl=hs.h_heading),
        Macro(self, '\\subsubsection', args='*OA', repl=hs.h_heading),
        Macro(self, '\\title', args='*OA', repl=hs.h_heading),
        Macro(self, '\\usepackage', args='OA',
                            repl=hs.h_load_module(self.package_modules)),
        Macro(self, '\\vspace', args='*A', repl=' '),

        #   \LTadd etc.
        #
        Macro(self, self.macro_filter_add, args='A', repl='#1'),
        Macro(self, self.macro_filter_alter, args='AA', repl='#2'),
        Macro(self, self.macro_filter_skip, args='A', repl=''),
        Macro(self, self.macro_load_defs, args='A', repl=hs.h_load_defs),

        ]


    def init_environments(self):
        """Initialize default LaTeX environments."""

        self.environment_defs = [

        Environ(self, 'figure', args='O', add_pars=False),
        Environ(self, 'minipage', args='A'),
        Environ(self, 'table', args='O', add_pars=False),
        Environ(self, 'tabular', args='A', add_pars=False),
        Environ(self, 'thebibliography', args='A', add_pars=True),
        Environ(self, 'verbatim', remove=False, add_pars=True),

        EquEnv(self, 'displaymath'),
        EquEnv(self, 'eqnarray'),
        EquEnv(self, 'eqnarray*'),
        EquEnv(self, 'equation'),

        ]

        #   enumerate: generate 1., 2., 3., ...
        #
        def labs_enumerate(level):
            if level == 0:
                n = 1
                while True:
                    yield str(n) + '.'
                    n += 1
            else:
                c = 'a'
                while True:
                    yield c + '.'
                    c = chr(ord(c) + 1) if c != 'z' else 'a'

        #   itemize: use default labels
        #
        def labs_itemize(level):
            while True:
                yield self.item_default_label[
                            min(level, len(self.item_default_label) - 1)]

        self.environment_defs += [

        Environ(self, 'enumerate', args='O', add_pars=False, items=labs_enumerate),
        Environ(self, 'itemize', args='O', add_pars=False, items=labs_itemize),

        ]


    def init_parser_languages(self, lang):
        """
        Initialize language-dependent parser parameters.

        Args:
            lang: Key for :attr:`parser_lang_settings` with which the
              :attr:`parser_lang_stack` is initialized.

        Settings for ``en`` are taken as fall back.
        """

        settings = self.parser_lang_settings = {}

        settings['en'] = ParserLanguageSettings(
            proof_name = 'Proof',
            math_repl_inline = ['B-B-B', 'C-C-C', 'D-D-D',
                                        'E-E-E', 'F-F-F', 'G-G-G'],
            math_repl_inline_vowel = None,
            math_repl_display = ['U-U-U', 'V-V-V', 'W-W-W',
                                        'X-X-X', 'Y-Y-Y', 'Z-Z-Z'],
            math_repl_display_vowel = None,
            math_op_text = {'+': 'plus', '-': 'minus',
                                    '\\cdot': 'times', '\\times': 'times',
                                    '/': 'over',
                                    None: 'equal'},     # default value
            lang_change_repl = ['K-K-K', 'L-L-L', 'M-M-M', 'N-N-N'],
            lang_change_repl_vowel = None,
            short_macros = {}
        )
        settings['de'] = ParserLanguageSettings(
            proof_name = 'Beweis',
            math_repl_inline = ['B-B-B', 'C-C-C', 'D-D-D',
                                        'E-E-E', 'F-F-F', 'G-G-G'],
            math_repl_inline_vowel = None,
            math_repl_display = ['U-U-U', 'V-V-V', 'W-W-W',
                                        'X-X-X', 'Y-Y-Y', 'Z-Z-Z'],
            math_repl_display_vowel = None,
            math_op_text = {'+': 'plus', '-': 'minus',
                                    '\\cdot': 'mal', '\\times': 'mal',
                                    '/': 'durch',
                                    None: 'gleich'},    # default value
            lang_change_repl = ['K-K-K', 'L-L-L', 'M-M-M', 'N-N-N'],
            lang_change_repl_vowel = None,
            short_macros = {
                '"-': '',
                '"=': '-',
                '"`': '\N{DOUBLE LOW-9 QUOTATION MARK}',    # \glqq
                '"\'': '\N{LEFT DOUBLE QUOTATION MARK}',    # \grqq
                '"A': 'Ä',
                '"a': 'ä',
                '"O': 'Ö',
                '"o': 'ö',
                '"U': 'Ü',
                '"u': 'ü',
                '"s': 'ß',
            }
        )
        settings['ru'] = ParserLanguageSettings(
            proof_name = 'Доказательство',
            math_repl_inline = ['Б-Б-Б', 'В-В-В', 'Г-Г-Г',
                                        'Д-Д-Д', 'Е-Е-Е', 'Ж-Ж-Ж'],
            math_repl_inline_vowel = None,
            math_repl_display = ['Ц-Ц-Ц', 'Ч-Ч-Ч', 'Ш-Ш-Ш',
                                        'Ы-Ы-Ы', 'Э-Э-Э', 'Ю-Ю-Ю'],
            math_repl_display_vowel = None,
            math_op_text = {'+': 'плюс', '-': 'минус',
                                    '\\cdot': 'раз', '\\times': 'раз',
                                    '/': 'на',
                                    None: 'равно'},     # default value
            lang_change_repl = ['К-К-К', 'Л-Л-Л', 'М-М-М', 'Н-Н-Н'],
            lang_change_repl_vowel = None,
            short_macros = {}
        )

        self.parser_lang_stack = [(settings[self.check_parser_lang(lang)],
                                        lang)]
        """
        List of tuples `(settings, lang)` where `settings` are the
        `ParserLanguageSettings` for the language `lang`. The last list
        item is the current language. The previous items are languages
        used before.
        """
        self.lang_context = self.parser_lang_stack[-1][0]


    def init_collections(self):
        """
        Initialize more special settings.

        This includes punctuation convention, special YaLafi commands,
        accent macros, special tokens.
        """

        #   add dot to heading unless last heading char in ...
        #   (turn off: set to [])
        #
        self.heading_punct = ['!', '?']

        #   labels for \item without [...] (may depend on nesting level)
        #
        self.item_default_label = ['']

        #   \item with [...] label: if text before ends with something
        #   from here, then append it to label
        #
        self.item_punctuation = ['.', ':', ',', ';', '!', '?']

        #   mark for parsing problem, should raise message from proofreader
        #
        self.mark_latex_error = 'LATEXXXERROR'

        #   True: include error description
        #
        self.mark_latex_error_verbose = False

        #   names of special macros
        #
        self.macro_filter_add = '\\LTadd'
        self.macro_filter_alter = '\\LTalter'
        self.macro_filter_skip = '\\LTskip'
        self.macro_load_defs = '\\LTinput'

        #   ignore re-definitions in LaTeX text for these macros:
        #
        self.newcommand_ignore = [
            self.macro_filter_add,
            self.macro_filter_alter,
            self.macro_filter_skip,
            self.macro_load_defs,
        ]

        #   special LaTeX comments to skip input text
        #
        self.comment_skip_begin = '%%% LT-SKIP-BEGIN'
        self.comment_skip_end = '%%% LT-SKIP-END'

        #   module directories
        #
        self.class_modules = 'yalafi.documentclasses'
        self.package_modules = 'yalafi.packages'

        #   accent macros
        #
        self.accent_macros = {

            "\\'": ['ACUTE', 'ACCENT'],
            '\\`': ['GRAVE', 'ACCENT'],
            '\\^': ['CIRCUMFLEX', 'ACCENT'],
            '\\v': ['CARON'],
            '\\~': ['TILDE'],
            '\\"': ['DIAERESIS'],
            '\\r': ['RING ABOVE'],
            '\\=': ['MACRON'],
            '\\b': ['LINE BELOW'],
            '\\u': ['BREVE'],
            '\\H': ['DOUBLE ACUTE', 'ACCENT'],
            '\\.': ['DOT ABOVE'],
            '\\d': ['DOT BELOW'],
            '\\c': ['CEDILLA'],
            '\\k': ['OGONEK'],

        }

        #   "special" tokens: expanded to key value
        #
        self.special_tokens = {

            '{': '{',
            '}': '}',

            '$$': '$$',
            '$': '$',
            '#': '#',
            '&': ' ',       # expand to space
            '_': '_',
            '^': '^',

            '\\(': '\\(',
            '\\)': '\\)',
            '\\[': '\\[',
            '\\]': '\\]',
            '\\\\': ' ',    # expand to space

            '~': '\N{NO-BREAK SPACE}',
            '``': '\N{LEFT DOUBLE QUOTATION MARK}',
            "''": '\N{RIGHT DOUBLE QUOTATION MARK}',
            '--': '\N{EN DASH}',
            '---': '\N{EM DASH}',

            '\\ ': ' ',
            '\\\t': ' ',
            '\\\n': ' ',
            '\\,': '\N{NARROW NO-BREAK SPACE}',
            '\\:': ' ',
            '\\;': ' ',
            '\\!': '',

            '\\{': '{',
            '\\}': '}',
            '\\$': '$',
            '\\#': '#',
            '\\&': '&',
            '\\_': '_',
            '\\%': '%',

            '\\/': '',

        }


    def init_math_collections(self):
        """
        Initialize settings for parsing math material.
        """

        self.math_displayed_simple = False
        """
        Boolean indicating whether to use simple replacement for
        displayed equations.
        """

        self.math_ignore = [
            '{',
            '}',
            '\\!',
            '\\label',
            '\\mathrlap',
            '\\nonumber',
        ]
        """
        List of things to be ignored in math mode.

        Some entries are redundant, if macros are known from text mode
        and expand to “nothing”.
        """

        self.math_space = [
            '~',
            '\\ ',
            '\\\t',
            '\\\n',
            '\\:',
            '\\,',
            '\\;',
        ]
        """List of things that generate space even in math mode."""

        self.math_operators = [
            '+', '-', '\\cdot', '\\times', '/',
            '=', '\\eq', '\\ne', '\\neq',
            '<', '>', '\\le', '\\leq', '\\ge', '\\geq',
            ':', ':=', '\\to', '\\cap', '\\cup',
            '\\Rightarrow', '\\Leftarrow', '\\Leftrightarrow',
            '\\subset', '\\subseteq', '\\supset', '\\supseteq',
            '\\stackrel',
        ]
        """
        List of math operators.

        If one of these operators appear first in a part (only math
        tokens) then one of the replacements in `self.math_op_text` is
        inserted.
        """

        self.math_text_macros = [
            '\\mbox',
        ]
        """
        List of macro names whose argument is treated as text even in
        math mode.
        """

        self.math_default_env = 'displaymath'
        r"""
        Name of math environment used for `$$` and `\[`.
        """

        self.math_punctuation = ['.', ',', ';', ':']
        """
        List of punctuation characters extracted from math parts.

        If a math part ends with a character from this list, it is
        appended to the replacement from `self_repl_xxx`.
        """

    def macro_character(self, c):
        """
        Determine whether a character may be part of a LaTeX macro name.

        Returns ``True``, if `c` is in ``[a-zA-Z@]``.
        """
        return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c == '@'


    def check_parser_lang(self, lang):
        """
        Transform `lang` into valid key for language dictionary
        :attr:`parser_lang_settings`.
        """
        lang = lang[:2].lower()
        return lang if lang in self.parser_lang_settings else 'en'


    def change_parser_lang(self, tok):
        """
        Switch current parser language settings to new language.
        """
        if tok.back:
            if len(self.parser_lang_stack) > 1:
                self.parser_lang_stack.pop()
        else:
            if tok.hard:
                self.parser_lang_stack[-1] = (
                self.parser_lang_settings[self.check_parser_lang(tok.lang)],
                        tok.lang)
            else:
                self.parser_lang_stack.append(
                (self.parser_lang_settings[self.check_parser_lang(tok.lang)],
                        tok.lang))
        # Already defined in self.init_parser_languages():
        # pylint: disable-next=attribute-defined-outside-init
        self.lang_context = self.parser_lang_stack[-1][0]


    def lang_context_lang(self):
        """
        Return the language key (e.g. ``en``) for the current language.
        """
        return self.parser_lang_stack[-1][1]


    def no_specials(self):
        """
        Deactivate special macros and magic comments.
        """
        # Already defined in self.init_collections():
        # pylint: disable-next=attribute-defined-outside-init
        self.comment_skip_begin = 'x'
        # pylint: disable-next=attribute-defined-outside-init
        self.comment_skip_end = 'x'
        self.macro_defs_python += [
            Macro(self, self.macro_filter_add, args='A', repl=''),
            Macro(self, self.macro_filter_alter, args='AA', repl='#1'),
            Macro(self, self.macro_filter_skip, args='A', repl='#1'),
        ]

    def __init__(self, language='en'):
        self.init_collections()
        self.init_math_collections()
        self.multi_language = False
        self.ml_continue_thresh = 3
        self.init_parser_languages(language)
        self.scanner = scanner.Scanner(self)
        self.init_macros()
        self.init_environments()


class ParserLanguageSettings:
    """
    Language settings for parser.
    """
    def __init__(self, proof_name,
                        math_repl_inline, math_repl_inline_vowel,
                        math_repl_display, math_repl_display_vowel,
                        math_op_text,
                        lang_change_repl, lang_change_repl_vowel,
                        short_macros):
        self.proof_name = proof_name
        self.math_repl_inline = math_repl_inline
        if math_repl_inline_vowel is None:
            self.math_repl_inline_vowel = math_repl_inline
        else:
            self.math_repl_inline_vowel = math_repl_inline_vowel
        self.math_repl_display = math_repl_display
        if math_repl_display_vowel is None:
            self.math_repl_display_vowel = math_repl_display
        else:
            self.math_repl_display_vowel = math_repl_display_vowel
        self.math_op_text = math_op_text
        self.lang_change_repl = lang_change_repl
        if lang_change_repl_vowel is None:
            self.lang_change_repl_vowel = lang_change_repl
        else:
            self.lang_change_repl_vowel = lang_change_repl_vowel
        self.short_macros = short_macros
        self.active_chars = set(k[0] for k in self.short_macros.keys())
