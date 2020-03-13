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

from .defs import Macro
from . import handlers


class Parameters:

    def __init__(self):

        self.macro_defs_latex = r"""

        \newcommand{\newline}{ }
        \newcommand{\textbackslash}{\verb?\?}   % \\ is line break
        \newcommand{\textasciicircum}{\verb?^?} % \^ is accent
        \newcommand{\textcolor}[2]{#2}
        \newcommand{\textasciitilde}{\verb?~?}  % \~ is accent

        """

        self.macro_defs_python = [
            Macro('\\newcommand', args='*AOOA',
                                    repl=handlers.handle_newcommand),
            Macro('\\renewcommand', args='*AOOA',
                                    repl=handlers.handle_newcommand),
        ]

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

    def macro_character(self, c):
        return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z'

