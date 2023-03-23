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
Simple LaTeX scanner mapping LaTeX source to token lists.
"""

from yalafi import defs
from yalafi import utils


class Scanner:
    """
    Simple LaTeX scanner mapping LaTeX source to token lists.

    Each “normal” character becomes a single token. Space is divided
    into paragraph-breaking and non-breaking space.
    """
    def __init__(self, parms):
        self.parms = parms

        # sort list of special tokens: long tokens first
        self.special_tokens_sorted = list(parms.special_tokens.keys())
        self.special_tokens_sorted.sort(key=(lambda s: -len(s)))

    def scan(self, latex, source='<unknown>'):
        """
        Scan a LaTeX string into tokens.

        This also changes attributes of the scanner.

        Args:
            latex: LaTeX string.
            source: Name of the source, usually the file name from where
              the LaTeX strings comes. Defaults to '<unknown>'.

        Returns:
            List of tokens representing the LaTeX string.
        """
        self.latex = latex
        self.source = source
        self.max_pos = len(latex)
        self.pos = 0
        tokens = []
        while self.pos < self.max_pos:
            tokens.append(self.next_token())
        return tokens


    def next_token(self):
        """
        Return next token based on position :attr:`pos`.

        Identify which token to insert for the next characters, i.e. for
        the first characters in ``self.latex[self.pos:]``.  Advance
        ``self.pos`` and return the correct token.

        Returns:
            The next token.
        """
        latex = self.latex
        start = self.pos
        c = latex[start]

        # depending on character dispatch to subroutines:
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
        # otherwise, only return one character:
        self.pos += 1
        return defs.TextToken(start, c)


    def scan_comment(self, latex, start):
        """Scan a % comment."""
        self.pos = next((i for i in range(start + 1, self.max_pos)
                                if latex[i] == '\n'), self.max_pos)
        next_non_space = next((i for i in range(self.pos + 1, self.max_pos)
                                if not latex[i].isspace()), self.max_pos)
        if latex.count('\n', self.pos + 1, next_non_space) == 0:
            # next line not empty: progress further
            self.pos = next_non_space
        return defs.CommentToken(start, latex[start:self.pos])


    def scan_space(self, latex, start):
        """Scan space."""
        self.pos = next((i for i in range(start + 1, self.max_pos)
                                if not latex[i].isspace()), self.max_pos)
        space = latex[start:self.pos]
        if space.count('\n') < 2:
            return defs.SpaceToken(start, space)
        return defs.ParagraphToken(start, space)


    def scan_macro(self, latex, start):
        r"""Scan a LaTeX macro beginning with ``\``"""
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


    def scan_arg_token(self, latex, start):
        r"""Scan argument number like ``#1`` used in ``\newcommand``."""
        self.pos += 1
        if self.pos >= self.max_pos or not latex[self.pos].isdecimal():
            return defs.SpecialToken(start, latex[start])
        arg = int(latex[self.pos])
        self.pos += 1
        return defs.ArgumentToken(start, latex[start:self.pos], arg)


    def scan_verb(self, latex, start):
        r"""Scan ``\verb``"""
        def verb_err():
            return self.latex_error('bad \\verb argument', start)[0]
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


    def scan_verbatim(self, latex, start, mac):
        r"""
        Scan environment begin.

        If the environment name is not ``verbatim``, a
        :class:`yalafi.defs.BeginToken` is returned and :attr:`pos` is
        left unchanged.
        If the environment name is ``verbatim``, the scanner is advanced
        and a :class:`yalafi.defs.VerbatimToken` with the content of the
        ``verbatim`` environment is returned.
        """
        # XXX: we do not account for % comments
        pos = next((i for i in range(start + len('\\begin'), self.max_pos)
                        if not latex[i].isspace()), self.max_pos)
        if (pos >= self.max_pos or latex.count('\n', start, pos) > 1
                or not latex.startswith('{verbatim}', pos)):
            return defs.BeginToken(start, mac)

        pos += len('{verbatim}')
        end = latex.find('\\end{verbatim}', pos)
        if end < 0:
            return self.latex_error('missing end of verbatim', start)[0]
        self.pos = end + len('\\end{verbatim}')
        return defs.VerbatimToken(pos, latex[pos:end], environ=True)


    #   HACK: we us a "fake parser"
    def latex_error(self, msg, pos):
        """Wrapper for :func:`yalafi.utils.latex_error`"""
        class FP:
            """Fake parser for using :func:`yalafi.utils.latex_error`."""
            def __init__(self, sc):
                self.latex = sc.latex
                self.source = sc.source
                self.parms = sc.parms
        return utils.latex_error(FP(self), msg, pos)


class Buffer:
    """
    A buffer for tokens.

    It is basically a list of tokens, where all operations happen at the
    beginning. In the implementation, it is a reversed list. This is
    faster and more convenient than changing a list at the beginning.
    """

    def __init__(self, tokens):
        self.tokens = list(reversed(tokens))
        """List of tokens. The last item is the first token."""


    def all(self):
        """Return list of all remaining tokens."""
        return list(reversed(self.tokens))


    def cur(self):
        """Return the current (first) token in the buffer."""
        if self.tokens:
            return self.tokens[-1]
        return None


    def next(self):
        "Remove the current (first) token from the buffer and return the next."
        if self.tokens:
            self.tokens.pop()
        return self.cur()


    def back(self, toks):
        """
        Push back a list of tokens, i.e. place them in front of all
        other tokens in the buffer.
        """
        self.tokens.extend(reversed(toks))


    def skip_space(self):
        """
        Skip space and comment tokens, remove them from the buffer, and
        return the next other token. Paragraph tokens are not skipped.

        See :meth:`Buffer.is_space` for details on which tokens are
        skipped.
        """
        tok = self.cur()
        while self.is_space(tok):
            tok = self.next()
        return tok


    def look_ahead(self):
        """
        Skip space and comment tokens, but keep them in the buffer, and
        return the next other token.

        Paragraph tokens are not skipped, but they might be returned.

        See `Buffer.is_space` for details on which tokens are skipped.
        """
        buf = []
        tok = self.cur()
        while self.is_space(tok):
            buf.append(tok)
            tok = self.next()
        self.back(buf)
        return tok


    def is_space(self, tok):
        """
        Test whether token is space or comment (but not paragraph).

        Args:
            tok: TextToken

        Returns:
            `True`, if tok is :class:`yalafi.defs.SpaceToken`,
            :class:`yalafi.defs.CommentToken`,
            :class:`yalafi.defs.ActionToken`,
            :class:`yalafi.defs.VoidToken`, or
            :class:`yalafi.defs.LanguageToken`.
        """
        return type(tok) in (defs.SpaceToken, defs.CommentToken,
                        defs.ActionToken, defs.VoidToken, defs.LanguageToken)

