#
#   Tex2txt, a flexible LaTeX filter
#   YaLafi: Yet another LaTeX filter
#   Copyright (C) 2018-2020 Matthias Baumann
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

import re

#   create error messages for single letters
#
def create_single_letter_matches(plain, cmdline):
    if cmdline.single_letters is None:
        # option not given: do not check
        return []

    #   some processing of the accepted patterns given in the option
    #
    accept = cmdline.single_letters.split('|')
    def f(s):
        # - replace '~' and '\\,' with UTF-8 (narrow) non-breaking space
        # - escape the rest, for instance dots '.'
        # - add word boundaries if appropriate
        #
        s = s.replace('~', '\N{NO-BREAK SPACE}')
        s = s.replace('\\,', '\N{NARROW NO-BREAK SPACE}')
        s = re.escape(s)
        if s[0].isalpha():
            s = r'\b' + s
        if s[-1].isalpha():
            s = s + r'\b'
        return r'(' + s + r')'
    accept = r'|'.join(f(s) for s in accept if s)

    #   a list of all occurences of accepted patterns
    #
    if accept:
        hits = list((m.start(0), m.end(0))
                        for m in re.finditer(accept, plain))
    else:
        hits = []

    def msg(m):
        return create_message(m, rule='PRIVATE::SINGLE_LETTER',
                    msg='Single letter detected.', repl='—')
    def f(m):
        #   return True if match of single letter occurs inside of
        #   a place in list 'hits'
        #
        for (beg, end) in hits:
            if beg <= m.start(0) < end:
                return True
        return False
    single = r'\b[^\W0-9_]\b'
    return list(msg(m) for m in re.finditer(single, plain) if not f(m))

#   create error messages for problem with equation punctuation
#
def create_equation_punct_messages(plain, cmdline,
                                    equation_replacements_display,
                                    equation_replacements_inline,
                                    equation_replacements):
    if cmdline.equation_punctuation is None:
        return []

    mode = {
        'displayed': equation_replacements_display,
        'inline': equation_replacements_inline,
        'all': equation_replacements,
    }
    k = list(k for k in mode.keys()
                        if k.startswith(cmdline.equation_punctuation))
    if len(k) != 1:
        tex2txt.fatal('mode for --equation-punctuation has to determine'
                        + ' one of ' + ', '.join(mode.keys()))
    repls = mode[k[0]]

    def msg(m):
        return create_message(m, rule='PRIVATE::EQUATION_PUNCTUATION',
                    msg='Possibly incorrect punctuation after equation.',
                    repl='—')
    def f(m):
        #   return True if equation is followed by
        #   - another equation (possibly after punctuation in punct)
        #   - a dot
        #   - a lower-case word (possibly after punctuation in punct)
        #
        groups = m.groups()
        equ = groups[0]     # another equation follows: not consumed!
        dot = groups[-2]    # a dot follows
        word = groups[-1]   # a word follows
        return equ or dot or word and word[0].islower()
    punct = ',;:'
    equ = r'\b(?:' + repls + r')\b'
    expr = (r'(' + equ + r'(?=\s*[' + punct + r']?\s*' + equ + r'))|'
                + equ + r'\s*(?:(\.)|[' + punct + r']?\s*([^\W0-9_]+))?')
    return list(msg(m) for m in re.finditer(expr, plain) if not f(m))

def create_context(txt, offset, length):
    context_size = 45
    beg = max(offset - context_size, 0)
    end = min(offset + context_size, len(txt))
    s = txt[beg:end].replace('\t', ' ').replace('\n', ' ')
    return  {
        'text': '...' + s + '...',
        'offset': offset - beg + 3,
        'length': length,
    }

#   construct message element for a match from re.finditer()
#
def create_message(m, rule, msg, repl):
    offset = m.start(0)
    length = len(m.group(0))
    return {
        'offset': offset,
        'length': length,
        'context': create_context(m.string, offset, length),
        'rule': {'id': rule, 'category': {'name': 'Problem'}},
        'message': msg,
        'replacements': [{'value': repl}],
    }

