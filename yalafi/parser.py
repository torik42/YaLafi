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

from . import defs
from . import mathparser
from . import scanner
from . import utils
import copy


class Parser:
    def __init__(self, parms, add_macros=None):
        self.parms = parms
        self.the_macros = dict((m.name, m) for m in parms.macro_defs_python)
        self.the_environments = dict((e.name, e)
                                            for e in parms.environment_defs)
        self.mathparser = mathparser.MathParser(parms)

        # read macro definitions from LaTeX text
        macs = scanner.Scanner(parms, parms.macro_defs_latex).all()
        self.expand_sequence(scanner.Buffer(macs))
        if add_macros:
            macs = scanner.Scanner(parms, add_macros).all()
            self.expand_sequence(scanner.Buffer(macs))

    #   scann and parse (expand) LaTeX string to tokens
    #
    def parse(self, latex):
        sc = scanner.Scanner(self.parms, latex)
        buf = scanner.Buffer(sc.all())
        return self.expand_sequence(buf)

    #   expand token sequence in text mode from current buffer
    #   - env_stop: stop reading on \end for this environment
    #   Return: expanded token sequence
    #
    def expand_sequence(self, buf, env_stop=None):
        out = []
        while True:
            tok = buf.cur()
            if not tok:
                break
            if type(tok) is defs.MacroToken:
                if tok.txt == '\\begin':
                    out += self.begin_environment(buf, tok)
                elif tok.txt == '\\end':
                    t, stop = self.end_environment(buf, tok, env_stop)
                    if stop:
                        return t
                    out += t
                else:
                    buf.back(self.expand_macro(buf, tok))
            elif tok.txt == '{':
                out.append(defs.ActionToken(tok.pos))
                out += self.expand_sequence(self.arg_buffer(buf))
                if buf.cur():
                    out.append(defs.ActionToken(buf.cur().pos))
            elif tok.txt == '}':
                utils.latex_error('unexpected }', tok.pos)
            elif tok.txt == '$' or tok.txt == '\\(':
                out += self.mathparser.expand_inline_math(buf, tok)
            elif tok.txt == '$$' or tok.txt == '\\[':
                out += self.mathparser.expand_display_math(buf, tok.txt)
            elif type(tok) is defs.SpecialToken:
                out.append(defs.ActionToken(tok.pos))
                txt = self.parms.special_tokens[tok.txt]
                out.append(defs.TextToken(tok.pos, txt))
                buf.next()
            elif type(tok) is defs.VerbatimToken:
                out.append(defs.ActionToken(tok.pos))
                out.append(defs.TextToken(tok.pos, tok.txt))
                buf.next()
            elif type(tok) is defs.CommentToken:
                buf.next()
            else:
                out.append(tok)
                buf.next()
        return self.remove_pure_action_lines(out)

    #   read block (till } or ]) or single token from current buffer buf
    #   Return: new buffer for reading these tokens
    #   - buffer will contain at least one token for position tracking
    #
    def arg_buffer(self, buf, end='}'):
        tok = buf.skip_space()
        if not tok:
            # XXX: improve position estimation?
            return scanner.Buffer([defs.VoidToken(0)])
        if end == '}' and tok.txt != '{':
            # consume single token
            buf.next()
            return scanner.Buffer([tok])
        pos = tok.pos
        lev = 1 if tok.txt == '{' else 0
        tok = buf.next()    # skip opening { or [
        out = []
        while tok:
            if tok.txt == '{':
                lev += 1
            if tok.txt == '}':
                lev -= 1
            if tok.txt == end and lev == 0:
                buf.next()  # consume closing } or ]
                if not out:
                    out = [defs.VoidToken(pos)]
                return scanner.Buffer(out)
            out.append(tok)
            tok = buf.next()
        utils.latex_error('cannot find closing ' + end, pos)

    #   expand a "normal" macro
    #   Return: tokens to be inserted
    #
    def expand_macro(self, buf, tok):
        buf.next()
        buf.skip_space()    # for macros without arguments, even if known
        if tok.txt not in self.the_macros:
            return [defs.ActionToken(tok.pos)]
        return self.expand_arguments(buf, self.the_macros[tok.txt], tok.pos)

    #   expand arguments for "normal" macro or \begin of environment
    #   Return: tokens to be inserted
    #
    def expand_arguments(self, buf, mac, start):
        arguments = []
        opt = 0
        for code in mac.args:
            tok = buf.skip_space()
            if code == '*':
                if tok and tok.txt == '*':
                    buf.next()
                continue
            if code == 'O':
                if tok and tok.txt == '[':
                    arg = self.arg_buffer(buf, end=']').all()
                else:
                    if opt < len(mac.opts):
                        arg = mac.opts[opt]
                    else:
                        arg = []
            elif code == 'A':
                arg = self.arg_buffer(buf).all()
            else:
                assert code in '*AO'
            arguments.append(arg)
            opt += 1

        out = [defs.ActionToken(start)]
        if callable(mac.repl):
            return out + mac.repl(self, buf, mac, arguments)

        # preparation for position tracking
        #
        cur_pos = start
        for tok in mac.repl:
            if type(tok) is defs.ArgumentToken and arguments[tok.arg-1]:
                # NB: may be an absent optional argument
                cur_pos = arguments[tok.arg-1][0].pos

        # macro expansion
        #
        for tok in mac.repl:
            if type(tok) is defs.ArgumentToken:
                arg = arguments[tok.arg - 1]
                if arg:
                    out.append(defs.ActionToken(arg[0].pos))
                    out += arg
                    out.append(defs.ActionToken(arg[-1].pos))
                    cur_pos = arg[-1].pos
            else:
                tok = copy.copy(tok)
                tok.pos = cur_pos
                tok.pos_fix = True
                out.append(tok)
        return out

    #   open an environment
    #
    def begin_environment(self, buf, tok):
        out = [defs.ActionToken(tok.pos)]
        name = self.get_environment_name(buf)
        if name not in self.the_environments:
            return out
        env = self.the_environments[name]
        out += self.expand_arguments(buf, env, tok.pos)
        if type(env) is defs.EquEnvironment:
            return out + self.mathparser.expand_display_math(buf, name)
        if env.remove:
            out += self.expand_sequence(buf, env_stop=name)
        return out

    #   close an environment
    #
    def end_environment(self, buf, tok, env_stop):
        name = self.get_environment_name(buf)
        if (name not in self.the_environments
                or not self.the_environments[name].end_par):
            out = [defs.ActionToken(tok.pos)]
        else:
            out = [defs.ParagraphToken(tok.pos, '\n\n', pos_fix=True)]
        return out, name == env_stop

    def get_environment_name(self, buf):
        buf.next()
        return self.get_text_expanded(self.arg_buffer(buf).all())

    #   generate string from token sequence, without macro expansion
    #
    def get_text_direct(self, toks):
        return ''.join(t.txt for t in toks
                            if type(t) is not defs.CommentToken)

    #   generate string from token sequence, with macro expansion
    #
    def get_text_expanded(self, toks):
        toks = self.expand_sequence(scanner.Buffer(toks))
        return self.get_text_direct(toks)

    #   remove all blank text lines that contain at least one ActionToken
    #
    def remove_pure_action_lines(self, tokens):
        def eval(t):
            if type(t) is defs.ActionToken:
                t.is_blank = True
                t.can_start = False
                t.can_end = False
            else:
                txt = t.txt
                t.is_blank = '\n' not in txt and not txt.strip()
                t.can_start = '\n' in txt and not txt[txt.rfind('\n'):].strip()
                t.can_end = '\n' in txt and not txt[:txt.find('\n')].strip()
            return t

        tokens = [t for t in tokens if t.txt or type(t) is defs.ActionToken]
        tokens = [eval(t) for t in tokens]
        tok = eval(defs.TextToken(0, ''))
        tok.can_start = True
        tokens.insert(0, tok)
        tok = eval(defs.TextToken(tokens[-1].pos, ''))
        tok.can_end = True
        tokens.append(tok)

        out = []
        while tokens:
            tok = tokens.pop(0)
            if not tok.can_start:
                out.append(tok)
                continue
            buf = [tok]
            can_remove = True
            while tokens:
                tok = tokens.pop(0)
                buf.append(tok)
                if tok.can_end:
                    break
                if not tok.is_blank:
                    can_remove = False
                    break
            if (can_remove and len(buf) > 1
                    and any(type(t) is defs.ActionToken for t in buf)):
                t1 = copy.copy(buf[0])
                t2 = copy.copy(buf[-1])
                # in t1, we remove all behind the last newline
                txt = t1.txt
                if '\n' in txt:
                    t1.txt = txt[:txt.rfind('\n')+1]
                else:
                    t1.txt = ''
                # in t2, we remove all till including the first newline
                txt = t2.txt
                if '\n' in txt:
                    pos = txt.find('\n') + 1
                    t2.txt = txt[pos:]
                    t2.pos += pos
                else:
                    t2.txt = ''
                    t2.pos += len(txt)
                buf = [t1, t2]
            if len(buf) > 1:
                tokens.insert(0, eval(buf.pop()))
            out += buf

        return [t for t in out if t.txt]

