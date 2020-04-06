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

#
#   default parameters for scanner and parser
#

from .defs import Environ, EquEnv, Macro
from . import handlers as hs
from . import scanner


class Parameters:

    #   pre-defined macros
    #
    def init_macros(self):

        #   definition of macros, LaTeX code
        #
        self.macro_defs_latex = r"""

        \newcommand{\AA}{Å}
        \newcommand{\aa}{å}
        \newcommand{\AE}{Æ}
        \newcommand{\ae}{æ}
        \newcommand{\color}[1]{}
        \newcommand{\colorbox}[2]{#2}
        \newcommand{\documentclass}[2][]{}
        \newcommand{\eqref}[1]{(0)}
        \newcommand{\fcolorbox}[3]{#3}
        \newcommand{\footnotemark}[1][]{}
        \newcommand{\hfill}{ }
        \newcommand{\include}[1]{}
        \newcommand{\includegraphics}[2][]{}
        \newcommand{\input}[1]{}
        \newcommand{\L}{Ł}
        \newcommand{\l}{ł}
        \newcommand{\label}[1]{}
        \newcommand{\medspace}{ }
        \newcommand{\newline}{ }
        \newcommand{\O}{Ø}
        \newcommand{\o}{ø}
        \newcommand{\OE}{Œ}
        \newcommand{\oe}{œ}
        \newcommand{\pageref}[1]{0}
        \newcommand{\par}{

}
        \newcommand{\qquad}{ }
        \newcommand{\quad}{ }
        \newcommand{\ref}[1]{0}
        \newcommand{\S}{§}
        \newcommand{\ss}{ß}
        \newcommand{\texorpdfstring}[2]{#1}
        \newcommand{\textasciicircum}{\verb?^?} % \^ is accent
        \newcommand{\textasciitilde}{\verb?~?}  % \~ is accent
        \newcommand{\textbackslash}{\verb?\?}   % \\ is line break
        \newcommand{\textcolor}[2]{#2}
        \newcommand{\thickspace}{ }
        \newcommand{\thinspace}{ }
        \newcommand{\usepackage}[2][]{}

        """

        #   definition of macros, Python code
        #
        self.macro_defs_python = [

        Macro(self, '\\caption', args='OA', extract='#2'),
        Macro(self, '\\cite', args='OA', repl=hs.h_cite),
            # or simpler: \newcommand{\cite}[2][none]{[0, #1]}
        Macro(self, '\\footnote', args='OA', extract='#2'),
        Macro(self, '\\footnotetext', args='OA', extract='#2'),
        Macro(self, '\\framebox', args='OOA', repl='#3'),
        Macro(self, '\\hspace', args='*A', repl=' '),
        Macro(self, '\\vspace', args='*A', repl=' '),

        Macro(self, '\\chapter', args='*OA', repl=hs.h_heading),
            # or simpler, without added dot: \newcommand{\chapter}[1]{#1}
        Macro(self, '\\part', args='*OA', repl=hs.h_heading),
        Macro(self, '\\section', args='*OA', repl=hs.h_heading),
        Macro(self, '\\subsection', args='*OA', repl=hs.h_heading),
        Macro(self, '\\subsubsection', args='*OA', repl=hs.h_heading),
        Macro(self, '\\title', args='*OA', repl=hs.h_heading),

        #   \LTadd etc.
        #
        Macro(self, self.macro_filter_add, args='A', repl='#1'),
        Macro(self, self.macro_filter_alter, args='AA', repl='#2'),
        Macro(self, self.macro_filter_skip, args='A', repl=''),
        Macro(self, self.macro_read_macros, args='A', repl=hs.h_read_macros),

        Macro(self, '\\newcommand', args='*AOOA', repl=hs.h_newcommand),
        Macro(self, '\\renewcommand', args='*AOOA', repl=hs.h_newcommand),

        ]

    #   pre-defined environments
    #
    def init_environments(self):

        #   little helper for theorem environments
        #
        def thm(s):
            return hs.h_theorem(s)

        self.environment_defs = [

        Environ(self, 'minipage', args='A'),
        Environ(self, 'table', repl='[Tabelle]', remove=True),
        Environ(self, 'verbatim', remove=False, add_pars=True),

        Environ(self, 'proof', args='O',
                            # Parser.expand_arguments() may skip space
                            repl='#1.\n', defaults=[self.proof_name]),

        #   theorem-style environments
        #   or simpler: Environ(self, 'theorem', args='O',
        #                           repl='Theorem (#1). ', defaults=['none']),
        Environ(self, 'corollary', args='O', repl=thm('Corollary')),
        Environ(self, 'definition', args='O', repl=thm('Definition')),
        Environ(self, 'example', args='O', repl=thm('Example')),
        Environ(self, 'lemma', args='O', repl=thm('Lemma')),
        Environ(self, 'proposition', args='O', repl=thm('Proposition')),
        Environ(self, 'remark', args='O', repl=thm('Remark')),
        Environ(self, 'theorem', args='O', repl=thm('Theorem')),

        #   equation environments
        #
        EquEnv(self, 'align'),
        EquEnv(self, 'align*'),
        EquEnv(self, 'alignat', args='A'),
        EquEnv(self, 'alignat*', args='A'),
        EquEnv(self, 'displaymath'),
        EquEnv(self, 'eqnarray'),
        EquEnv(self, 'eqnarray*'),
        EquEnv(self, 'equation'),
        EquEnv(self, 'equation*'),
        EquEnv(self, 'flalign', repl='  relation', remove=True),

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

        Environ(self, 'enumerate', add_pars=False, items=labs_enumerate),
        Environ(self, 'itemize', add_pars=False, items=labs_itemize),

        ]

    #   set language-dependent parameters
    #
    def init_language(self, language):
        if language == 'de':
            self.special_tokens.update(self.special_tokens_de)
            self.proof_name = 'Beweis'
            self.math_repl_inline = ['B-B-B', 'C-C-C', 'D-D-D',
                                        'E-E-E', 'F-F-F', 'G-G-G']
            self.math_repl_display = ['U-U-U', 'V-V-V', 'W-W-W',
                                        'X-X-X', 'Y-Y-Y', 'Z-Z-Z']
            self.math_op_text = {'+': 'plus', '-': 'minus',
                                    '*': 'mal', '/': 'durch',
                                    None: 'gleich'}     # default value
        else:
            self.proof_name = 'Proof'
            self.math_repl_inline = ['B-B-B', 'C-C-C', 'D-D-D',
                                        'E-E-E', 'F-F-F', 'G-G-G']
            self.math_repl_display = ['U-U-U', 'V-V-V', 'W-W-W',
                                        'X-X-X', 'Y-Y-Y', 'Z-Z-Z']
            self.math_op_text = {'+': 'plus', '-': 'minus',
                                    '*': 'times', '/': 'over',
                                    None: 'equal'}      # default value

    #   set misc collections
    #
    def init_collections(self):

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

        self.macro_filter_add = '\\LTadd'
        self.macro_filter_alter = '\\LTalter'
        self.macro_filter_skip = '\\LTskip'
        self.macro_read_macros = '\\LTmacros'

        #   ignore re-definitions in LaTeX text for these macros:
        #
        self.newcommand_ignore = [
            self.macro_filter_add,
            self.macro_filter_alter,
            self.macro_filter_skip,
            self.macro_read_macros,
        ]

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

        }

        #   "special" tokens for German
        #
        self.special_tokens_de = {

            '"-': '',
            '"=': '-',
            '"`': '\N{DOUBLE LOW-9 QUOTATION MARK}',    # \glqq
            '"\'': '\N{LEFT DOUBLE QUOTATION MARK}',    # \grqq

        }

    #   set math collections
    #
    def init_math_collections(self):

        #   things to be ignored in math mode
        #   - some entries are redundant, if macros are known from text mode
        #     and expand to 'nothing'
        #
        self.math_ignore = [

            '{',
            '}',
            '\\!',
            '\\label',
            '\\mathrlap',
            '\\negthickspace',
            '\\negthinspace',
            '\\negmedspace',
            '\\nonumber',
            '\\notag',
            '\\qedhere',

        ]

        #   things that generate space even in math mode
        #
        self.math_space = [

            '~',
            '\\ ',
            '\\\t',
            '\\\n',
            '\\:',
            '\\,',
            '\\;',
            '\\medspace',
            '\\qquad',
            '\\quad',
            '\\thickspace',
            '\\thinspace',

        ]

        #   if these operators appear first in a part (only math tokens)
        #   then one of the replacements in self.math_op_text is inserted
        #
        self.math_operators = [

            '+', '-', '*', '/',
            '=', '\\eq', '\\ne', '\\neq',
            '<', '>', '\\le', '\\leq', '\\ge', '\\geq',
            ':', ':=', '\\to', '\\cap', '\\cup',
            '\\Leftrightarrow',
            '\\subset', '\\subseteq', '\\supset', '\\supseteq',
            '\\stackrel',

        ]

        #   macros whose argument is treated in text mode
        #
        self.math_text_macros = [
            '\\mbox',
            '\\text',
        ]

        #   math environment for $$ and \[
        #
        self.math_default_env = 'displaymath'

        #   if a math section ends with a character from here, it is
        #   appended to the replacement from self_repl_xxx
        #
        self.math_punctuation = ['.', ',', ';', ':']

    def add_latex_macros(self, latex):
        self.macro_defs_latex += latex

    #   determine whether a character may be part of macro name
    #
    def macro_character(self, c):
        return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z'

    def __init__(self, language='en'):
        self.init_collections()
        self.init_math_collections()
        self.init_language(language)
        self.scanner = scanner.Scanner(self)
        self.init_macros()
        self.init_environments()

