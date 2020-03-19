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

    def init_macros_environments(self):

        # XXX: caption, cite, footnote, footnotetext, framebox
        # XXX: hspace, vspace

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
        \newcommand{\item}[1][]{ #1 }
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

        self.macro_defs_python = [

        # or simpler: \newcommand{\cite}[2][none]{[0, #1]}
        Macro(self, '\\cite', args='OA', repl=hs.h_cite),

        # or simpler, without added dot: \newcommand{\chapter}[1]{#1}
        Macro(self, '\\chapter', args='*OA', repl=hs.h_heading),
        Macro(self, '\\part', args='*OA', repl=hs.h_heading),
        Macro(self, '\\section', args='*OA', repl=hs.h_heading),
        Macro(self, '\\subsection', args='*OA', repl=hs.h_heading),
        Macro(self, '\\subsubsection', args='*OA', repl=hs.h_heading),
        Macro(self, '\\title', args='*OA', repl=hs.h_heading),

        Macro(self, '\\newcommand', args='*AOOA',
                                repl=hs.h_newcommand),
        Macro(self, '\\renewcommand', args='*AOOA',
                                repl=hs.h_newcommand),

        ]

        self.environment_defs = [

        Environ(self, 'comment', repl='', remove=True, add_pars=False),
        Environ(self, 'minipage', args='A'),
        Environ(self, 'table', repl='[Tabelle]', remove=True),

        Environ(self, 'proof', args='O',
                            # Parser.expand_arguments() may skip space
                            repl='#1.\n', opts=[self.proof_name]),

        # theorem-style environments
        # or simpler: Environ(self, 'theorem', args='O',
        #                           repl='Theorem (#1). ', opts=['none']),
        Environ(self, 'corollary', args='O', repl=hs.h_theorem('Corollary')),
        Environ(self, 'definition', args='O', repl=hs.h_theorem('Definition')),
        Environ(self, 'example', args='O', repl=hs.h_theorem('Example')),
        Environ(self, 'lemma', args='O', repl=hs.h_theorem('Lemma')),
        Environ(self, 'proposition', args='O',
                                        repl=hs.h_theorem('Proposition')),
        Environ(self, 'remark', args='O', repl=hs.h_theorem('Remark')),
        Environ(self, 'theorem', args='O', repl=hs.h_theorem('Theorem')),

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
                                    None: 'gleich'}
        else:
            self.proof_name = 'Proof'
            self.math_repl_inline = ['B-B-B', 'C-C-C', 'D-D-D',
                                        'E-E-E', 'F-F-F', 'G-G-G']
            self.math_repl_display = ['U-U-U', 'V-V-V', 'W-W-W',
                                        'X-X-X', 'Y-Y-Y', 'Z-Z-Z']
            self.math_op_text = {'+': 'plus', '-': 'minus',
                                    '*': 'times', '/': 'over',
                                    None: 'equal'}

    def init_collections(self):

        # add dot to heading unless last heading char in ...
        # (turn off: set to '')
        self.heading_punct = '!?'

        self.accent_macros = {

            "\\'": 'ACUTE',
            '\\`': 'GRAVE',
            '\\^': 'CIRCUMFLEX',
            '\\v': 'CARON',
            '\\~': 'TILDE',
            '\\"': 'DIAERESIS',
            '\\r': 'RING ABOVE',
            '\\=': 'MACRON',
            '\\b': 'LINE BELOW',
            '\\u': 'BREVE',
            '\\H': 'DOUBLE ACUTE',
            '\\.': 'DOT ABOVE',
            '\\d': 'DOT BELOW',
            '\\c': 'CEDILLA',
            '\\k': 'OGONEK',

        }

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
            '\\,': ' ',
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

        self.special_tokens_de = {

            '"-': '',
            '"=': '-',
            '"`': '\N{DOUBLE LOW-9 QUOTATION MARK}',    # \glqq
            '"\'': '\N{LEFT DOUBLE QUOTATION MARK}',    # \grqq

        }

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

        self.math_operators = [

            '+', '-', '*', '/',
            '=', '\\eq', '\\ne', '\\neq',
            '<', '>', '\\le', '\\leq', '\\ge', '\\geq',
            ':', ':=', '\\to', '\\cap', '\\cup',
            '\\Leftrightarrow',
            '\\subset', '\\subseteq', '\\supset', '\\supseteq',
            '\\stackrel',

        ]

        self.math_text_macros = [
            '\\mbox',
            '\\text',
        ]

        # math environment for $$ and \[
        self.math_default_env = 'displaymath'

        self.math_punctuation = '.,;:'

    def macro_character(self, c):
        return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z'

    def __init__(self, language='en'):
        self.init_collections()
        self.init_language(language)
        self.scanner = scanner.Scanner(self)
        self.init_macros_environments()

