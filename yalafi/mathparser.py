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
#   replacement of equations: described in README.md, section
#   "Handling of displayed equations"
#

"""
Parsing LaTeX math parts.
"""

from yalafi import defs
from yalafi import utils


class MathPartToken(defs.TextToken):
    """
    Token representing a sequence consisting only of math tokens.

    Attributes:
        toks: List of contained tokens.
    """

    def __init__(self, toks):
        super().__init__(toks[0].pos, toks[0].txt)
        self.toks = toks

    def __repr__(self):
        # XXX: why that?
        return 'MathPartToken()'

    def start_space(self):
        """
        Check if first token is a :class:`yalafi.defs.MathSpaceToken`.
        """
        return type(self.toks[0]) is defs.MathSpaceToken

    def end_space(self):
        """
        Check if last token is a :class:`yalafi.defs.MathSpaceToken`.
        """
        return type(self.toks[-1]) is defs.MathSpaceToken

    def only_space(self):
        """
        Check if all tokens are :class:`yalafi.defs.MathSpaceToken`.
        """
        return all(type(t) is defs.MathSpaceToken for t in self.toks)

    def has_elem(self, parms):
        """
        Get first math element.

        Args:
            parms: :class:`yalafi.parameters.Parameters` object for handling
              current settings.

        Returns:
            The first :class:`yalafi.defs.MathElemToken` not in
            :obj:`parms.math_punctuation` or `None`.
        """
        return next((t for t in self.toks if type(t) is defs.MathElemToken
                        and t.txt not in parms.math_punctuation), None)

    def leading_op(self):
        """
        Check if the leading token is :class:`yalafi.defs.MathOperToken`
        and return it.

        Returns:
            The leading :class:`yalafi.defs.MathOperToken` if only
            preceded by space or `None`.
        """
        tok = next((t for t in self.toks
                        if type(t) is not defs.MathSpaceToken), None)
        return tok if type(tok) is defs.MathOperToken else None

    def last_char(self, parser):
        """
        Get the last character from the math part.

        Used to check for punctuation.

        Returns:
            A possibly empty string with the last character.
        """
        txt = parser.get_text_direct(self.toks)
        txt = txt.strip()
        return txt[-1] if txt else ''


class MathParser:
    """
    Parser for math material.
    """

    def __init__(self, parser):
        self.parser = parser

    def expand_display_math(self, buf, tok, env):
        r"""
        Expand display math material

        Args:
            buf: Current buffer to read math from.  The math material
              will be removed from the buffer.
            tok: Token marking the beginning of the math material. Typically
              :class:`yalafi.defs.MathBeginToken` or
              :class:`yalafi.defs.SpecialToken`.
            env: :class:`yalafi.defs.EquEnv` of the math environment to parse.
              Can be `displaymath`, if the environment starts with ``\[``.

        Returns:
            List of tokens replacing the parsed math material.
        """
        buf.next()
        start_simple = start = tok.pos
        first_section = True
        next_repl = True
        out = [defs.ActionToken(start),
                        defs.SpaceToken(start, '  ', pos_fix=True)]
        while True:
            tokens, end = self.expand_math_section(buf, start,
                                        ['&', '\\\\', '$$', '\\]'], env.name)
            tokens = self.detect_math_parts(tokens)
            sec, next_repl = self.replace_section(False, tokens,
                        first_section, next_repl,
                        self.parser.parms.lang_context.math_repl_display)
            out += sec
            if end and end.txt == '&':
                out.append(defs.SpaceToken(out[-1].pos, ' ', pos_fix=True))
                first_section = False
            elif end and end.txt == '\\\\':
                out.append(defs.SpaceToken(out[-1].pos, '\n  ', pos_fix=True))
                self.parser.parse_newline_option(buf, False)
                first_section = True
            else:
                break
            if buf.cur():
                start = buf.cur().pos

        if env.remove:
            txt = self.parser.get_text_direct(out).strip()
            if txt and txt[-1] in self.parser.parms.math_punctuation:
                out = [defs.TextToken(out[-1].pos, txt[-1], pos_fix=True)]
            else:
                out = [defs.ActionToken(out[-1].pos)]
        else:
            if self.parser.parms.math_displayed_simple:
                txt = self.parser.get_text_direct(out).strip()
                out = [defs.ActionToken(start_simple),
                        defs.SpaceToken(start_simple, '  ', pos_fix=True),
                        defs.TextToken(start_simple, self.parser.parms.
                                        lang_context.math_repl_display[0],
                                        pos_fix=True)]
                if txt and txt[-1] in self.parser.parms.math_punctuation:
                    out.append(defs.TextToken(out[-1].pos, txt[-1],
                                                        pos_fix=True))
            out.append(defs.ActionToken(out[-1].pos))
        return out


    def expand_inline_math(self, buf, tok):
        r"""
        Expand inline math material.

        Args:
            buf: Current buffer to read math from.  The math material
              will be removed from the buffer.
            tok: :class:`yalafi.defs.TextToken` marking the beginning of
              the math material, i.e. ``tok.txt`` is either ``$`` or
              ``\(``.

        Returns:
            List of tokens replacing the parsed math material.
        """
        buf.next()
        # pylint: disable-next=unused-variable
        tokens, x = self.expand_math_section(buf, tok.pos, ['$', '\\)'], None)
        tokens = self.detect_math_parts(tokens)
        out = [defs.ActionToken(tok.pos)]
        t, x = self.replace_section(True, tokens, True, True,
                            self.parser.parms.lang_context.math_repl_inline)
        out += t
        out.append(defs.ActionToken(out[-1].pos))
        return out


    def expand_math_section(self, buf, start, toks_stop, env_stop):
        r"""
        Expand a piece of math material.

        Group tokens into types :class:`yalafi.defs.MathElemToken`,
        :class:`yalafi.defs.MathOperToken` and
        :class:`yalafi.defs.MathSpaceToken`.  Unknown macros generate a
        :class:`yalafi.defs.MathElemToken`, unless listed in
        :attr:`parser.parms.math_ignore`.  Thus macros like `\alpha`
        need not be declared.  Embedded ``\text{…}`` parts are included
        with normal :class:`yalafi.defs.TextToken`.

        Args:
            buf: Current buffer to read math from.  The math material
              will be removed from the buffer.
            start: Original starting position of the math material in
              the LaTeX source.  Used only for error generation.
            toks_stop: List of strings, which end current math section,
              or None.  Can be used to break sections of math material
              at ``&`` and ``\\``.
            env_stop: Name of the LaTeX math environment at which end
              the expansion should stop, or None.

        Returns:
            A tuple containing a list of groped tokens and the token
            stopping the expansion.
        """
        def special(t):
            if type(t) is defs.SpecialToken:
                txt = parms.special_tokens[t.txt]
            else:
                txt = t.txt
            return t.pos, txt

        parser = self.parser
        parms = parser.parms
        out = []
        while True:
            tok = buf.skip_space()
            if not tok or type(tok) is defs.ParagraphToken:
                buf.next()
                out = (utils.latex_error(parser, 'missing end of maths', start)
                                                    + out)
                break
            elif tok.txt in toks_stop:
                buf.next()
                break
            elif type(tok) is defs.BeginToken:
                buf.back(parser.begin_environment(buf, tok, True))
                continue
            elif type(tok) is defs.EndToken:
                t, stop = parser.end_environment(buf, tok, env_stop)
                out += t
                if stop:
                    break
                continue
            elif type(tok) is defs.MacroToken:
                if tok.txt in parms.math_text_macros:
                    buf.next()
                    out += parser.expand_sequence(
                                        parser.arg_buffer(buf, tok.pos))
                    continue
                t = parser.expand_macro(buf, tok, True)
                if tok.txt in parms.math_space:
                    t.insert(0, defs.MathSpaceToken(tok.pos, ' '))
                elif tok.txt in parms.math_operators:
                    t.insert(0, defs.MathOperToken(tok.pos, tok.txt))
                elif not (tok.txt in parser.the_macros
                            or tok.txt in parms.math_ignore):
                    t.insert(0, defs.MathElemToken(tok.pos, tok.txt))
                buf.back(t)
                continue
            elif type(tok) in (defs.MathElemToken, defs.MathOperToken,
                                            defs.MathSpaceToken):
                out.append(tok)
            elif tok.txt in parms.math_ignore:
                pass
            elif type(tok) is defs.LanguageToken:
                pass
            elif tok.txt in parms.math_space:
                out.append(defs.MathSpaceToken(tok.pos, ' '))
            elif tok.txt in parms.math_operators:
                out.append(defs.MathOperToken(*special(tok)))
            else:
                out.append(defs.MathElemToken(*special(tok)))
            buf.next()

        out = [t for t in out
                    if type(t) not in (defs.VoidToken, defs.ActionToken)]
        return out, tok


    def detect_math_parts(self, toks):
        """
        Detect uninterrupted math parts.

        Given a token sequence, find parts of math tokens not
        interrupted by other tokens and condense them into a single
        :class:`MathPartToken` token.  Other tokens are just copied.

        Args:
            toks: List of :class:`yalafi.defs.TextToken`.

        Returns:
            List of tokens.
        """


        def ismath(t):
            """
            Check whether the token is a math token.

            Args:
                t: A token

            Returns:
                True, if ``t`` is a :class:`yalafi.defs.MathElemToken`,
                :class:`yalafi.defs.MathOperatorToken` or
                :class:`yalafi.defs.MathSpaceToken`.  False otherwise.
            """
            return type(t) in (defs.MathElemToken, defs.MathOperToken,
                                    defs.MathSpaceToken)
        out = []
        while toks:
            pos = next((i for i in range(len(toks))
                                if ismath(toks[i])), len(toks))
            out += toks[:pos]
            toks = toks[pos:]
            if not toks:
                break
            pos = next((i for i in range(len(toks))
                                if not ismath(toks[i])), len(toks))
            out.append(MathPartToken(toks[:pos]))
            toks = toks[pos:]
        return out


    def replace_section(self, inline, tokens, first_section,
                                next_repl, repls):
        """
        Replace math parts in a section by placeholders.

        Add trailing punctuation if present in a math part. And insert
        a placeholder for leading math operators if first in part, but
        not first in current section.

        For more details see the implementation details in ???.

        Args:
            inline: Boolean indicating whether the tokens are from
              inline math.
            tokens: List of tokens describing one math section.  The
              only reasonable math token is :class:`MathPartToken`.
            first_section: Boolean indicating whether the section is the
              first in a line.
            next_repl: Boolean indicating, whether the next replacement
              shall be used for the first token.
            repls: A list of replacement strings.  It will be cycled
              in place.

        Returns:
            A tuple consisting of a list of replacement tokens and the
            Boolean ``next_repl`` for the next section.
        """
        first_part = not first_section
        parms = self.parser.parms
        out = []
        for tok in tokens:
            if type(tok) is not MathPartToken:
                out.append(tok)
                if tok.txt.strip():
                    first_part = False
                    next_repl = True
                continue
            if tok.only_space():
                out.append(defs.SpaceToken(tok.pos, ' ', pos_fix=True))
                continue

            if tok.start_space():
                out.append(defs.SpaceToken(tok.pos, ' ', pos_fix=True))
            op = tok.leading_op()
            elem = tok.has_elem(parms)
            if not inline and first_part and op:
                s = parms.lang_context.math_op_text.get(
                            op.txt, parms.lang_context.math_op_text[None])
                out.append(defs.SpaceToken(tok.pos, ' ', pos_fix=True))
                out.append(defs.TextToken(op.pos, s, pos_fix=True))
                out.append(defs.SpaceToken(op.pos, ' ', pos_fix=True))
            if inline or (next_repl or op and first_part) and elem:
                repls[:] = repls[1:] + repls[:1]
            if inline or elem:
                out.append(defs.TextToken(tok.pos if inline else elem.pos,
                                                repls[0], pos_fix=True))

            next_repl = False
            c = tok.last_char(self.parser)
            if c in parms.math_punctuation:
                out.append(defs.TextToken(tok.pos, c, pos_fix=True))
                next_repl = True
            if op and not elem:
                next_repl = True
            if tok.end_space():
                out.append(defs.SpaceToken(tok.pos, ' ', pos_fix=True))
        return out, next_repl
