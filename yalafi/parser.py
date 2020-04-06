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
import unicodedata


class Parser:
    def __init__(self, parms, read_macros=None):
        self.parms = parms
        self.read_macros = read_macros
        self.the_macros = dict((m.name, m) for m in parms.macro_defs_python)
        self.the_environments = dict((e.name, e)
                                            for e in parms.environment_defs)
        self.mathparser = mathparser.MathParser(self)
        self.unknowns = []
        self.latex = ''

        # used by expand_item():
        self.item_macro = defs.Macro(parms, '\\item', args='O', repl='#1')

        # for savety: \item labels outside of any environment
        def labs_default(level):
            while True:
                yield parms.item_default_label[0]
        self.item_lab_stack = [(labs_default(0), '')]

        # for expansion of verbatim environment
        self.verbatim_begin = [
                    defs.BeginToken(0, '\\begin'),
                    defs.SpecialToken(0, '{'),
                    defs.TextToken(0, 'verbatim'),
                    defs.SpecialToken(0, '}'),
        ]
        self.verbatim_end = parms.scanner.scan('\\end{verbatim}')

        # read macro definitions from LaTeX text
        self.parser_work(parms.macro_defs_latex)

    #   scan and parse (expand) LaTeX string to tokens
    #
    def parser_work(self, latex):
        # save self.latex for nested calls, e.g. \LTmacros{}
        latex_sav = self.latex
        self.latex = latex
        toks = self.parms.scanner.scan(latex)
        toks = self.expand_sequence(scanner.Buffer(toks))
        self.latex = latex_sav
        return toks

    #   main entry point
    #
    def parse(self, latex, extract=None):
        if extract:
            self.init_extractions(extract)
        self.extracted = []
        self.unknowns = []

        main = self.parser_work(latex)

        if extract:
            main = []
        for extr in self.extracted:
            if not extr:
                continue
            main.append(defs.ParagraphToken(extr[0].pos, '\n\n\n',
                                                pos_fix=True))
            main += extr
            main.append(defs.SpaceToken(extr[-1].pos, '\n', pos_fix=True))
        return main

    #   modify macro definitions for argument extraction
    #
    def init_extractions(self, extracts):
        for name in self.the_macros:
            mac = self.the_macros[name]
            if name in extracts:
                pos = next((i for i in range(len(mac.args))
                                if mac.args[i] == 'A'), len(mac.args))
                if pos < len(mac.args):
                    extr = '#' + str(pos + 1)
                else:
                    extr = ''
            else:
                extr = ''
            mac.extract = self.parms.scanner.scan(extr)
            mac.repl = []   # overwrite possible handlers
        for name in extracts:
            if name not in self.the_macros:
                self.the_macros[name] = defs.Macro(self.parms,
                            name, args='A', repl='', extract='#1')

    def get_unknowns(self):
        return self.unknowns

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
            elif type(tok) is defs.BeginToken:
                buf.back(self.begin_environment(buf, tok, False))
                continue
            elif type(tok) is defs.EndToken:
                t, stop = self.end_environment(buf, tok, env_stop)
                if stop:
                    return t
                out += t
                continue
            elif type(tok) is defs.ItemToken:
                buf.back(self.expand_item(buf, tok, out))
                continue
            elif type(tok) is defs.MacroToken:
                buf.back(self.expand_macro(buf, tok, False))
                continue
            elif tok.txt == '$' or tok.txt == '\\(':
                out += self.mathparser.expand_inline_math(buf, tok)
                continue
            elif type(tok) is defs.MathBeginToken:
                out += self.mathparser.expand_display_math(buf, tok,
                                                            tok.environ)
                continue
            elif tok.txt == '$$' or tok.txt == '\\[':
                if self.parms.math_default_env not in self.the_environments:
                    utils.fatal('no environment for \'$$\' or \'\\[\'')
                env = self.the_environments[self.parms.math_default_env]
                if type(env) is not defs.EquEnv:
                    utils.fatal(repr(env.name) + ' is not an EquEnv')
                out += self.mathparser.expand_display_math(buf, tok, env)
                continue
            elif type(tok) is defs.AccentToken:
                out += self.expand_accent(buf, tok)
                continue
            elif tok.txt == '{' or tok.txt == '}':
                out.append(defs.ActionToken(tok.pos))
            elif type(tok) is defs.SpecialToken:
                out.append(defs.ActionToken(tok.pos))
                txt = self.parms.special_tokens[tok.txt]
                out.append(defs.TextToken(tok.pos, txt))
            elif type(tok) is defs.VerbatimToken:
                if tok.environ:
                    # for Environ() entry in Parameters.environment_defs
                    t = copy.copy(tok)
                    t.environ = False
                    buf.next()
                    buf.back(self.verbatim_begin + [t] + self.verbatim_end)
                    continue
                else:
                    out.append(defs.ActionToken(tok.pos))
                    out.append(defs.TextToken(tok.pos, tok.txt))
            elif type(tok) is defs.CommentToken:
                pass
            else:
                out.append(tok)
            buf.next()
        return self.remove_pure_action_lines(out)

    #   read block (till } or ]) or single token from current buffer buf
    #   Return: new buffer for reading these tokens
    #   - buffer will contain at least one token for position tracking
    #   - this also ensures that an empty option [] will be "something"
    #
    def arg_buffer(self, buf, start, end='}'):
        tok = buf.skip_space()
        if not tok:
            return scanner.Buffer([defs.VoidToken(start)])
        if type(tok) is defs.ParagraphToken:
            return scanner.Buffer([defs.VoidToken(tok.pos)])
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
        return scanner.Buffer(utils.latex_error('cannot find closing ' + end,
                                            pos, self.latex, self.parms) + out)

    #   expand a "normal" macro
    #   Return: tokens to be inserted
    #
    def expand_macro(self, buf, tok, math):
        buf.next()
        buf.skip_space()    # for macros without arguments, even if known
        if tok.txt not in self.the_macros:
            if not (math or tok.txt in self.unknowns):
                self.unknowns.append(tok.txt)
            return [defs.ActionToken(tok.pos)]
        return self.expand_arguments(buf, self.the_macros[tok.txt], tok.pos)

    #   expand arguments for "normal" macro or \begin of environment
    #   Return: tokens to be inserted
    #
    def expand_arguments(self, buf, mac, start):
        arguments = []
        arguments_extr = []
        pos = start
        for n, code in enumerate(mac.args):
            arg_extr = arg = []
            tok = buf.skip_space()
            if tok:
                pos = tok.pos
            if code == '*':
                if tok and tok.txt == '*':
                    arg_extr = arg = [tok]
                    buf.next()
            elif code == 'O':
                if tok and tok.txt == '[':
                    arg_extr = arg = self.arg_buffer(buf, pos, end=']').all()
                else:
                    if n < len(mac.defaults):
                        # NB: do not use positions from macro definition
                        arg = [copy.copy(t) for t in mac.defaults[n]]
                        for t in arg:
                            t.pos = pos
                            t.pos_fix = True
            elif code == 'A':
                arg_extr = arg = self.arg_buffer(buf, pos).all()
            else:
                utils.fatal('illegal arg code ' + repr(code)
                                + ' of ' + repr(mac.name))
            arguments.append(arg)
            arguments_extr.append(arg_extr)

        if mac.extract:
            toks = self.generate_replacements(arguments_extr,
                                                        mac.extract, start)
            self.extracted.append(self.expand_sequence(scanner.Buffer(toks)))
        out = [defs.ActionToken(start)]
        if callable(mac.repl):
            return out + mac.repl(self, buf, mac, arguments, start)
        return out + self.generate_replacements(arguments, mac.repl, start)

    def generate_replacements(self, arguments, repls, start):
        out = []
        # preparation for position tracking
        #
        cur_pos = start
        for tok in repls:
            if type(tok) is defs.ArgumentToken and arguments[tok.arg-1]:
                # NB: may be an absent optional argument
                cur_pos = arguments[tok.arg-1][0].pos

        # macro expansion
        #
        for tok in repls:
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

    def expand_accent(self, buf, tok):
        buf.next()
        args = self.expand_sequence(self.arg_buffer(buf, tok.pos))
        if not args or not args[0].txt:
            c = ''
        elif len(args[0].txt) == 1:
            c = args[0].txt
            args.pop(0)
        else:
            args[0] = copy.copy(args[0])
            c = args[0].txt[0]
            args[0].txt = args[0].txt[1:]

        if not c.strip():
            c = ' '.join(self.parms.accent_macros[tok.txt])
        else:
            if not ('a' <= c <= 'z' or 'A' <= c <= 'Z'):
                return utils.latex_error('text-mode accent for non-letter',
                                            tok.pos, self.latex, self.parms)
            c = ('LATIN ' + ('SMALL' if c.islower() else 'CAPITAL')
                        + ' LETTER ' + c.upper() + ' WITH ' 
                        + self.parms.accent_macros[tok.txt][0])
        try:
            u = unicodedata.lookup(c)
        except:
            return utils.latex_error('could not find UTF-8 character "' + c
                                    + '"', tok.pos, self.latex, self.parms)
        return [defs.TextToken(tok.pos, u)] + args

    #   open an environment
    #
    def begin_environment(self, buf, tok, math):
        out = [defs.ActionToken(tok.pos)]
        name = self.get_environment_name(buf, tok)
        if name not in self.the_environments:
            if not (math or name in self.unknowns):
                self.unknowns.append(name)
            return out
        env = self.the_environments[name]
        if env.items:
            level = len([v for v in self.item_lab_stack if v[1] == name])
            self.item_lab_stack.append((env.items(level), name))
        if env.add_pars:
            out = [defs.ParagraphToken(tok.pos, '\n\n', pos_fix=True)]
        out += self.expand_arguments(buf, env, tok.pos)
        if type(env) is defs.EquEnv:
            out.append(defs.MathBeginToken(tok.pos, name, env))
            return out
        if env.remove:
            out += self.expand_sequence(buf, env_stop=name)
        return out

    #   close an environment
    #   - second element of returned 2-tuple: reached env_stop
    #
    def end_environment(self, buf, tok, env_stop):
        name = self.get_environment_name(buf, tok)
        out = [defs.ActionToken(tok.pos)]
        if name in self.the_environments:
            env = self.the_environments[name]
            if env.items and len(self.item_lab_stack) > 1:
                self.item_lab_stack.pop()
            if env.add_pars:
                out = [defs.ParagraphToken(tok.pos, '\n\n', pos_fix=True)]
        return out, name == env_stop

    def get_environment_name(self, buf, tok):
        buf.next()
        return self.get_text_expanded(self.arg_buffer(buf, tok.pos).all())

    #   generate string from token sequence, without macro expansion
    #
    def get_text_direct(self, toks):
        return ''.join(t.txt for t in toks
                            if type(t) is not defs.CommentToken)

    #   generate string from token sequence, with macro expansion
    #
    def get_text_expanded(self, toks):
        toks = self.expand_sequence(scanner.Buffer(toks.copy()))
        return self.get_text_direct(toks)

    #   remove all blank text lines, which contain at least one ActionToken
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

        # avoid modifications at list begin (expensive for long lists)
        tokens = list(reversed(tokens))
        out = []
        while tokens:
            tok = tokens.pop()
            if not tok.can_start:
                out.append(tok)
                continue
            buf = [tok]
            can_remove = True
            while tokens:
                tok = tokens.pop()
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
                buf = [t1]
                tokens.append(eval(t2))
                # NB: we deleted a line break
                tok = eval(defs.TextToken(t2.pos, ''))
                tok.can_start = True
                tokens.append(tok)
            elif len(buf) > 1:
                tokens.append(eval(buf.pop()))
            out += buf

        return [t for t in out if t.txt]

    #   \item: if [...] label is specified, look back in text and append
    #   a possible previous punctuation mark
    #
    def expand_item(self, buf, tok, out_so_far):
        def Space(pos):
            return defs.SpaceToken(pos, ' ', pos_fix=True)
        start = tok.pos
        buf.next()
        out = self.expand_arguments(buf, self.item_macro, start)
        if len(out) == 1:
            # only ActionToken: no [...]
            lab = next(self.item_lab_stack[-1][0])
            return out + [Space(start), defs.TextToken(start, lab,
                                            pos_fix=True), Space(start)]

        pos = next((i for i in range(len(out_so_far) - 1, -1, -1)
                                if out_so_far[i].txt.strip()), -1)
        if (pos >= 0 and out_so_far[pos].txt[-1]
                    in self.parms.item_punctuation):
            out.append(defs.TextToken(out[-1].pos,
                                out_so_far[pos].txt[-1], pos_fix=True))
        out.append(Space(out[-1].pos))
        out.insert(0, Space(start))
        return out

