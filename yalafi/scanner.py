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
#   a simple LaTeX scanner
#   - each "normal" character is an own token
#   - space is divided into "normal" space and paragraph-breaking space
#

from . import defs
from . import utils


class Scanner:
    def __init__(self, parms):
        self.parms = parms

        # sort list of special tokens: long tokens first
        self.special_tokens_sorted = list(parms.special_tokens.keys())
        self.special_tokens_sorted.sort(key=(lambda s: -len(s)))

    #   scan the given LaTeX string, return token list
    #
    def scan(self, latex):
        self.latex = latex
        self.max_pos = len(latex)
        self.pos = 0
        tokens = []
        while self.pos < self.max_pos:
            tokens.append(self.next_token())
        return tokens

    #   determine next token
    #
    def next_token(self):
        latex = self.latex
        start = self.pos
        c = latex[start]

        if c.isspace():
            return self.scan_space(latex, start)
        if c == '%':
            return self.scan_comment(latex, start)
        if c == '#':
            return self.scan_arg_token(latex, start)
        # - better with re.match()?
        #   (but would need to create latex[start:] for each token)
        # --> re.match() with one precompiled large RE a bit faster
        #     for short texts, but much slower for large texts!
        for t in self.special_tokens_sorted:
            if latex.startswith(t, start):
                self.pos += len(t)
                return defs.SpecialToken(start, t)
        if c == '\\':
            return self.scan_macro(latex, start)
        # single character
        self.pos += 1
        return defs.TextToken(start, c)

    #   scan a % comment
    #
    def scan_comment(self, latex, start):
        self.pos = next((i for i in range(start + 1, self.max_pos)
                                if latex[i] == '\n'), self.max_pos)
        next_non_space = next((i for i in range(self.pos + 1, self.max_pos)
                                if not latex[i].isspace()), self.max_pos)
        if latex.count('\n', self.pos + 1, next_non_space) == 0:
            # next line not empty: progress further
            self.pos = next_non_space
        return defs.CommentToken(start, latex[start:self.pos])

    #   scan a space or paragraph token
    #
    def scan_space(self, latex, start):
        self.pos = next((i for i in range(start + 1, self.max_pos)
                                if not latex[i].isspace()), self.max_pos)
        space = latex[start:self.pos]
        if space.count('\n') < 2:
            return defs.SpaceToken(start, space)
        return defs.ParagraphToken(start, space)

    #   scan a macro
    #
    def scan_macro(self, latex, start):
        self.pos = next((i for i in range(start + 1, self.max_pos)
                            if not self.parms.macro_character(latex[i])),
                            self.max_pos)
        if self.pos == start + 1 and self.pos < self.max_pos:
            # an accent macro like \'
            self.pos += 1
        mac = latex[start:self.pos]
        if mac == '\\begin':
            return self.scan_verbatim(latex, start, mac)
        if mac == '\\end':
            return defs.EndToken(start, mac)
        if mac == '\\item':
            return defs.ItemToken(start, mac)
        if mac == '\\verb':
            return self.scan_verb(latex, start)
        if mac in self.parms.accent_macros:
            return defs.AccentToken(start, mac)
        return defs.MacroToken(start, mac)

    #   scan argument number #1 etc.
    #
    def scan_arg_token(self, latex, start):
        self.pos += 1
        if self.pos >= self.max_pos or not latex[self.pos].isdecimal():
            return defs.SpecialToken(start, latex[start])
        arg = int(latex[self.pos])
        self.pos += 1
        return defs.ArgumentToken(start, latex[start:self.pos], arg)

    #   scan \verb
    #
    def scan_verb(self, latex, start):
        def verb_err():
            return utils.latex_error('bad \\verb argument',
                                        start, latex, self.parms)[0]
        start_arg = start + len('\\verb')
        if start_arg >= self.max_pos:
            return verb_err()
        end_arg = latex[start_arg] + '\n'
        start_arg += 1
        self.pos = next((i for i in range(start_arg, self.max_pos)
                                if latex[i] in end_arg), self.max_pos)
        if self.pos == self.max_pos or latex[self.pos] == '\n':
            return verb_err()
        self.pos += 1
        return defs.VerbatimToken(start_arg, latex[start_arg:self.pos-1])

    #   scan \begin{verbatim} ... \end{verbatim}
    #
    def scan_verbatim(self, latex, start, mac):
        # XXX: we do not account for % comments
        pos = next((i for i in range(start + len('\\begin'), self.max_pos)
                        if not latex[i].isspace()), self.max_pos)
        if (pos >= self.max_pos or latex.count('\n', start, pos) > 1
                or not latex.startswith('{verbatim}', pos)):
            return defs.BeginToken(start, mac)

        pos += len('{verbatim}')
        end = latex.find('\\end{verbatim}', pos)
        if end < 0:
            return utils.latex_error('missing end of verbatim',
                                            start, latex, self.parms)[0]
        self.pos = end + len('\\end{verbatim}')
        return defs.VerbatimToken(start, latex[pos:end], environ=True)


#   token buffer that can push back tokens
#   - use reversed token list to avoid pop / insert at list start
#
class Buffer:
    def __init__(self, tokens):
        self.tokens = list(reversed(tokens))

    #   return list of all remaining tokens
    #
    def all(self):
        return list(reversed(self.tokens))

    #   return current token or None
    #
    def cur(self):
        if self.tokens:
            return self.tokens[-1]
        return None

    #   advance to next token, return it or None
    #
    def next(self):
        if self.tokens:
            self.tokens.pop()
        return self.cur()

    #   push back a list of tokens
    #
    def back(self, toks):
        self.tokens.extend(reversed(toks))

    #   skip space and comments (but not paragraphs)
    #
    def skip_space(self):
        tok = self.cur()
        while type(tok) in (defs.SpaceToken, defs.CommentToken,
                                defs.ActionToken, defs.VoidToken):
            tok = self.next()
        return tok

