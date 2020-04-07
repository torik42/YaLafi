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

from . import defs
from . import utils


#   object that represents a sequence consisting only of math tokens
#
class MathPartToken(defs.TextToken):

    def __init__(self, toks):
        super().__init__(toks[0].pos, toks[0].txt)
        self.toks = toks
    def __repr__(sellf):
        # XXX: why that?
        return 'MathPartToken()'
    def start_space(self):
        return type(self.toks[0]) is defs.MathSpaceToken
    def end_space(self):
        return type(self.toks[-1]) is defs.MathSpaceToken
    def only_space(self):
        return all(type(t) is defs.MathSpaceToken for t in self.toks)
    def has_elem(self, parms):
        return next((t for t in self.toks if type(t) is defs.MathElemToken
                        and t.txt not in parms.math_punctuation), None)
    def leading_op(self):
        tok = next((t for t in self.toks
                        if type(t) is not defs.MathSpaceToken), None)
        return tok if type(tok) is defs.MathOperToken else None
    def last_char(self, parser):
        txt = parser.get_text_direct(self.toks)
        txt = txt.strip()
        return txt[-1] if txt else ''


class MathParser:

    def __init__(self, parser):
        self.parser = parser

    def expand_display_math(self, buf, tok, env):
        buf.next()
        start = tok.pos
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
                                        self.parser.parms.math_repl_display)
            out += sec
            if end and end.txt == '&':
                out.append(defs.SpaceToken(out[-1].pos, ' ', pos_fix=True))
                first_section = False
            elif end and end.txt == '\\\\':
                out.append(defs.SpaceToken(out[-1].pos, '\n  ', pos_fix=True))
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
            out.append(defs.ActionToken(out[-1].pos))
        return out

    #   "expand" inline maths
    #
    def expand_inline_math(self, buf, tok):
        buf.next()
        tokens, x = self.expand_math_section(buf, tok.pos, ['$', '\\)'], None)
        tokens = self.detect_math_parts(tokens)
        out = [defs.ActionToken(tok.pos)]
        t, x = self.replace_section(True, tokens, True, True,
                                    self.parser.parms.math_repl_inline)
        out += t
        out.append(defs.ActionToken(out[-1].pos))
        return out

    #   expand a piece of math material
    #   - group tokens into types MathElem, MathOper, MathSpace
    #   - unknown macros generate a MathElem, if not on the
    #     blacklist in parms.math_ignore
    #     --> macros like \alpha need not be declared
    #   - embedded \text{...} parts are included with "normal"
    #     non-Math tokens
    #
    def expand_math_section(self, buf, start, toks_stop, env_stop):
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
                out = (utils.latex_error('missing end of maths', start,
                                self.parser.latex, self.parser.parms) + out)
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

    #   given a token sequence, find parts of math tokens
    #   not interrupted by other token types
    #   - subsequent math tokens are condensed into single token MathPartToken
    #   - other tokens are just copied
    #   
    def detect_math_parts(self, toks):
        def ismath(t):
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

    #   replace math parts in a section by text placeholders
    #   - add trailing punctuation if present in a math part
    #   - insert placeholder for leading math operator if first in part
    #     and not first in current equation
    #
    def replace_section(self, inline, tokens, first_section,
                                next_repl, repls):
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
                s = parms.math_op_text.get(op.txt, parms.math_op_text[None])
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

