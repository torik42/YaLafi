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

r"""
Parsing LaTeX source with advanced macro expansion.
"""

import copy
import unicodedata

from yalafi import defs
from yalafi import mathparser
from yalafi import scanner
from yalafi import utils


class Parser:
    """
    LaTeX parser with advanced macro expansion.
    """

    def __init__(self, parms, packages=None, read_macros=None):
        if packages is None:
            packages = []
        self.parms = parms
        """:class:`yalafi.parameters.Parameters` object with Parser settings."""
        self.read_macros = read_macros
        self.packages = {}
        self.global_latex_options = []
        """Global options passed to document class."""
        self.the_macros = {}
        r"""Dictionary of all registered LaTeX macros.

        The keys are the macro names with preceding ``\``.
        The values are of type :class:`yalafi.defs.Macro`.
        """
        self.the_environments = {}
        """Dictionary of all registered LaTeX environment.

        The keys are the environment names.
        The values are of type :class:`yalafi.defs.Environ`.
        """
        self.mathparser = mathparser.MathParser(self)
        self.extracted = []
        self.unknowns = []
        self.latex = ''
        self.source = self.source_main = '<none>'

        # used by expand_item():
        self.item_macro = defs.Macro(parms, '\\item', args='O', repl='#1')

        # for safety: \item labels outside of any environment
        def labs_default(_):
            while True:
                yield parms.item_default_label[0]
        self.item_lab_stack = [(labs_default(0), '')]

        # initialise and modify parameters, macros, etc.
        builtin = [], lambda p, o, n: defs.InitModule(
                                macros_latex=parms.macro_defs_latex,
                                macros_python=parms.macro_defs_python,
                                environments=parms.environment_defs)
        for name, actions in [('<builtins>', builtin)] + packages:
            self.init_package(name, actions, [], 0)


    def init_package(self, name, actions, options, position):
        """
        Load a *package* module `name` into parser.

        If the package `name` is not already loaded to the parser or the
        `options` have changed, load all required packages by recursive
        calls. Then load the package itself and update parameter object
        `self.parms`.

        Args:
            name: LaTeX package name.
            actions: Tuple of :obj:`require_packages` and :func:`init_module`) as defined
              in Python modules for LaTeX packages.
            options: LaTeX package options.
            position: Position in source, where the package is loaded.

        Returns:
            List of tokens to be inserted.
        """
        out = []
        if (name in self.packages and
                self.packages[name] == self.global_latex_options + options):
            return out
        try:
            for requ in actions[0]:
                if requ not in self.packages or self.packages[requ] == options:
                    out += self.init_package(requ, utils.get_module_handler(
                                        requ, self.parms.package_modules),
                                        options, position)
            self.packages[name] = self.global_latex_options + options
            out += self.modify_parameters(name, actions[1], options, position)
        except:
            utils.fatal('error loading module ' + repr(name))
        return out


    def modify_parameters(self, name, f, options, position):
        r"""
        Modify :attr:`parms` and add new macros and
        environments to :attr:`the_macros` and :attr:`the_environments`,
        respectively.

        Used by package extension mechanism and handlers of LaTeX macro
        and environment definitions.

        Args:
            name: ???
            f: An :func:`init_module` function to initialize a module
              corresponding to a LaTeX package. It should have the following style

              .. function:: init_module(parser, options, position)

                 :param parser.Parser parser: Current parser
                 :param position: Position of the function call, usually
                                  the ``\usepackage[option]{package}``
                                  statement.
                 :return: A :class:`yalafi.defs.InitModule` object.

            options: LaTeX options for module ``name``.
            position: Position in source, where the package is loaded.

        Returns:
            List of tokens to be inserted.
        """
        mods = f(self, options, position)
        for m in mods.macros_python:
            self.the_macros[m.name] = m
        for e in mods.environs:
            self.the_environments[e.name] = e
        if mods.macros_latex:
            self.parser_work(mods.macros_latex, name)
        return mods.inject_tokens


    def parser_work(self, latex, source):
        """
        Scan and parse (expand) LateX string to tokens.

        Skip text enclosed in special comments
        :attr:`yalafi.parameters.Parameters.comment_skip_begin` and
        :attr:`yalafi.parameters.Parameters.comment_skip_end` of
        :attr:`parms`.

        Args:
            latex: String with LaTeX source code to be parsed.
            source: Name of the source for debug messages.

        Returns:
            Expanded sequence of tokens generated from the LaTeX source.
        """
        # save self.latex for nested calls, e.g. \LTinput{}
        latex_sav = self.latex
        self.latex = latex
        source_sav = self.source
        self.source = source

        toks = self.parms.scanner.scan(latex, source)

        # treat special comments for skipping LaTeX text
        out = []
        last = 0
        while True:
            beg = next((i for i in range(last, len(toks))
                    if type(toks[i]) is defs.CommentToken and
                    toks[i].txt.startswith(self.parms.comment_skip_begin)),
                                    len(toks))
            out += toks[last:beg]
            if beg == len(toks):
                break
            end = next((i for i in range(beg + 1, len(toks))
                    if type(toks[i]) is defs.CommentToken and
                    toks[i].txt.startswith(self.parms.comment_skip_end)),
                                    len(toks))
            if end == len(toks):
                out += utils.latex_error(self,
                                    'cannot find closing LaTeX comment '
                                    + repr(self.parms.comment_skip_end),
                                    toks[beg].pos)
                out += toks[beg+1:]
                break
            last = end + 1
        toks = out

        toks = self.expand_sequence(scanner.Buffer(toks))
        self.latex = latex_sav
        self.source = source_sav
        return toks


    def parse(self, latex, source='<unknown>',
                    define='', source_defs='<unknown>', extract=None):
        r"""
        Parse LaTeX source.

        Args:
            latex: String with LaTeX source code to be parsed.
            source: Name of the source for debug messages. Defaults to
              '<unknown>'.
            define: _description_. Defaults to ''.
            source_defs: _description_. Defaults to '<unknown>'.
            extract: List of macro names whose first argument should be
              extracted. If provided, only these macros are handled by
              YaLafi. No other parsing is happening. Defaults to None.

        Returns:
            List of parsed tokens. First part contains expansion
            following the `repl` of each Macro, followed by all
            extracted parts using the `extract` of each Macro separated
            by paragraph breaks. If `extract` is given, the first part
            is removed from the output.
        """
        if extract:
            # Redefine all macros, if only extracted parts are requested.
            self.init_extractions(extract)
        self.extracted = []
        self.unknowns = []
        self.source = self.source_main = source

        main = []
        if define:
            toks = self.parser_work(define, source_defs)
            main = utils.filter_set_toks(toks, 0, defs.LanguageToken)
        main += self.parser_work(latex, source)

        if extract:
            # Clear `main` again, if only extracted parts are requested.
            main = []
        for extr in self.extracted:
            if not extr:
                continue
            main.append(defs.ParagraphToken(extr[0].pos, '\n\n\n',
                                                pos_fix=True))
            main += extr
            main.append(defs.SpaceToken(extr[-1].pos, '\n', pos_fix=True))
        return main


    def init_extractions(self, extracts):
        """
        Modify macro definitions such that only the first argument of
        all given macros will be extracted. All other macro definitions
        are discarded.

        Args:
            extracts: List of macro names whose arguments shall be extracted.
        """
        for name, mac in self.the_macros.items():
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
        """Return unknown macro names."""
        return self.unknowns


    def expand_sequence(self, buf, env_stop=None):
        """
        Expand token sequence in text mode from buffer `buf` until end
        of environment `env_stop`.

        Args:
            buf: Buffer with tokens to be expanded.
            env_stop: Name of the environment at which end the expansion
              stops. Can be `None`, then the expansion will not end.

        Returns:
            Expanded token sequence.
        """
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
                buf.back(t)
                continue
            elif type(tok) is defs.ItemToken:
                buf.back(self.expand_item(buf, tok, out))
                continue
            elif type(tok) is defs.MacroToken:
                if tok.txt == '\\def':
                    out += self.parse_def_macro(buf, tok.pos)
                else:
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
            elif tok.txt == '\\\\':
                out.append(defs.ActionToken(tok.pos))
                out.append(defs.SpaceToken(tok.pos, ' '))
                buf.next()
                self.parse_newline_option(buf, True)
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
                    buf.next()
                    buf.back(self.expand_verb_env_token(tok))
                    continue
                else:
                    out.append(defs.ActionToken(tok.pos))
                    out.append(defs.TextToken(tok.pos, tok.txt))
            elif type(tok) is defs.LanguageToken:
                if self.parms.multi_language:
                    self.parms.change_parser_lang(tok)
                    out.append(tok)
            elif tok.txt in self.parms.lang_context.active_chars:
                out.append(self.expand_short_macro(buf, tok))
                continue
            elif type(tok) is defs.CommentToken:
                pass
            else:
                out.append(tok)
            buf.next()
        return self.remove_pure_action_lines(out)


    def arg_buffer(self, buf, start, end='}'):
        """
        Read block (till ``end``) or single token from current buffer
        ``buf``.

        Args:
            buf: A :class:`yalafi.scanner.Buffer` instance.
        Return:
            New :class:`yalafi.scanner.Buffer` for reading these tokens,
            it will contain at least one token for position tracking.
            This ensures that also an empty option ``[]`` will be
            tracked.
        """
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
        opening_tok = tok
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

        # HACK: see Issue 23
        # We have read till end of text, and the collected tokens might
        # be skipped by the caller. Thus, we push back the tokens to the
        # input, together with an error message. To the caller, we
        # return a buffer only yielding an error mark.
        buf.back([opening_tok]
                + utils.latex_error(self, 'cannot find closing "' + end + '"',
                                                pos) + out)
        return scanner.Buffer([defs.TextToken(opening_tok.pos,
                                    ' ' + self.parms.mark_latex_error + ' ',
                                    pos_fix=True)])


    def expand_macro(self, buf, tok, math):
        """
        Expand a normal macro.

        Return:
            List of tokens to be inserted.
        """
        buf.next()
        buf.skip_space()  # for macros without arguments, even if known
        if tok.txt not in self.the_macros:
            if not (math or tok.txt in self.unknowns):
                self.unknowns.append(tok.txt)
            return [defs.ActionToken(tok.pos)]
        return self.expand_arguments(buf, self.the_macros[tok.txt], tok.pos)


    def expand_arguments(self, buf, mac, start):
        """
        Expand arguments of a normal macro or environment.

        Returns:
            List of tokens to be inserted.
        """
        arguments = []
        arguments_extr = []
        delimiters = []
        pos = start
        for n, code in enumerate(mac.args):
            arg_extr = arg = []
            delim = False
            tok = buf.skip_space()
            if tok:
                pos = tok.pos
            if code == '*':
                if tok and tok.txt == '*':
                    arg_extr = arg = [tok]
                    buf.next()
            elif code == 'O':
                if tok and tok.txt == '[':
                    delim = True
                    arg_extr = arg = self.arg_buffer(buf, pos, end=']').all()
                else:
                    if n < len(mac.defaults):
                        # NB: do not use positions from macro definition
                        arg = [copy.copy(t) for t in mac.defaults[n]]
                        for t in arg:
                            t.pos = pos
                            t.pos_fix = True
            elif code == 'A':
                if tok and tok.txt == '}':
                    # issue #135
                    arg_extr = arg = [defs.VoidToken(pos)]
                else:
                    if tok and tok.txt == '{':
                        delim = True
                    arg_extr = arg = self.arg_buffer(buf, pos).all()
            else:
                utils.fatal('illegal arg code ' + repr(code)
                                + ' of ' + repr(mac.name))
            arguments.append(arg)
            arguments_extr.append(arg_extr)
            delimiters.append(delim)

        if mac.extract:
            toks = ([defs.LanguageToken(start,
                                    lang=self.parms.lang_context_lang(),
                                    hard=True, brk=True)]
                        + self.generate_replacements(arguments_extr,
                                                        mac.extract, start))
            self.extracted.append(self.expand_sequence(scanner.Buffer(toks)))
        out = [defs.ActionToken(start)]
        if callable(mac.repl):
            return out + mac.repl(self, buf, mac, arguments, delimiters, start)
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
                return utils.latex_error(self,
                                'text-mode accent for non-letter', tok.pos)
            size = 'SMALL' if c.islower() else 'CAPITAL'
            accent = self.parms.accent_macros[tok.txt][0]
            c = f"LATIN {size} LETTER {c.upper()} WITH {accent}"
        try:
            u = unicodedata.lookup(c)
        except:
            return utils.latex_error(self,
                f'could not find UTF-8 character "{c}"',
                tok.pos)
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
            if env.end_func:
                out += env.end_func(self, buf, env, [], [], tok.pos)
        return out, name == env_stop

    def get_environment_name(self, buf, tok):
        buf.next()
        return self.get_text_expanded(self.arg_buffer(buf, tok.pos).all())


    def expand_verb_env_token(self, tok):
        r"""
        Expand a single verbatim token delivered by the scanner to a
        valid token sequence for an environment which can be treated
        like any other environment afterwards.

        The scanner :class:`yalafi.scanner.Scanner` returns the whole content of a
        verbatim environment as a single :class:yalafi.defs.VerbatimToken` ``tok`` with
        ``tok.environ=True``. This function replaces this single token by
        a sequence of tokens which will later be replaced using
        :class:`Environ('verbatim', …)<yalafi.defs.Environ>` from :attr:`self.parms.environment_defs`.

        Args:
            tok: A single VerbatimToken.

        Returns:
            A list of tokens representing `tok` with `tok.environ` set
            to `False` within a `verbatim` environment.
        """
        tok = copy.copy(tok)
        tok.environ = False
        return [
                    defs.BeginToken(tok.pos, '\\begin'),
                    defs.SpecialToken(tok.pos, '{'),
                    defs.TextToken(tok.pos, 'verbatim'),
                    defs.SpecialToken(tok.pos, '}'),
                    tok,
                    defs.EndToken(tok.pos + len(tok.txt), '\\end'),
                    defs.SpecialToken(tok.pos + len(tok.txt), '{'),
                    defs.TextToken(tok.pos + len(tok.txt), 'verbatim'),
                    defs.SpecialToken(tok.pos + len(tok.txt), '}'),
        ]

    #   parse (skip) optional [...] after \\
    #
    def parse_newline_option(self, buf, skip_space):
        if skip_space:
            # we do not want to remove a line break for \\ without [...]
            tok = buf.look_ahead()
            if tok and tok.txt == '[':
                buf.skip_space()
        tok = buf.cur()
        if tok and tok.txt == '[':
            self.arg_buffer(buf, tok.pos, end=']')


    def get_text_direct(self, toks):
        """Generate string from token sequence, without macro expansion."""
        return ''.join(t.txt for t in toks
                            if type(t) is not defs.CommentToken)


    def get_text_expanded(self, toks):
        """
        Generate string from token sequence, with macro expansion.

        Expand all macros in `toks` and return the resulting text.
        """
        toks = self.expand_sequence(scanner.Buffer(toks.copy()))
        return self.get_text_direct(toks)


    def _classify_token(self, tok):
        r"""
        Classify token according to its ability to start or end a blank
        section which can be removed. Three boolean attributes are added
        to the token:
          is_blank: Set `True`, when the token contains only space, but
            no `\n`.
          can_start: Set `True` if `tok` contains `\n` and only space
            afterwards.
          can_end: Set `True` if `tok` contains `\n` and only space
            before.
        """
        if isinstance(tok, defs.ActionToken):
            tok.is_blank = True
            tok.can_start = False
            tok.can_end = False
        else:
            txt = tok.txt
            tok.is_blank = '\n' not in txt and not txt.strip()
            tok.can_start = '\n' in txt and not txt[txt.rfind('\n'):].strip()
            tok.can_end = '\n' in txt and not txt[:txt.find('\n')].strip()
        return tok


    def remove_pure_action_lines(self, tokens):
        """
        Remove all blank text lines in :obj:`tokens`, which contain at least
        one :class:`yalafi.defs.ActionToken`.

        Args:
            tokens: list of :class:`yalafi.defs.TextToken`.

        Returns:
            List of tokens with removed line breaks.
        """
        # Only keep tokens which have text, or are of type ActionToken
        # or LanguageToken. Classify them (see self._classify_token),
        # and put tokens which can start or end a blank section at the
        # start and end of the list (so that all tokens could be
        # removed).
        tokens = [t for t in tokens if t.txt or
                        type(t) in (defs.ActionToken, defs.LanguageToken)]
        tokens = [self._classify_token(t) for t in tokens]
        tok = self._classify_token(defs.TextToken(0, ''))
        tok.can_start = True
        tokens.insert(0, tok)
        tok = self._classify_token(defs.TextToken(tokens[-1].pos, ''))
        tok.can_end = True
        tokens.append(tok)

        # avoid modifications at list begin (expensive for long lists)
        # TODO: use `scanner.Buffer` instead.
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
                lang_toks = [t for t in buf if type(t) is defs.LanguageToken]
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
                buf = [t1] + lang_toks
                tokens.append(self._classify_token(t2))
                # NB: we deleted a line break
                tok = self._classify_token(defs.TextToken(t2.pos, ''))
                tok.can_start = True
                tokens.append(tok)
            elif len(buf) > 1:
                tokens.append(self._classify_token(buf.pop()))
            out += buf

        return [t for t in out if t.txt or type(t) is defs.LanguageToken]

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


    def expand_short_macro(self, buf, tok):
        """
        Expand a short macro as introduced by babel for language German,
         e.g. ``"A`` → ``Ä``.
        """
        cur = buf.next()
        if (not cur or tok.txt + cur.txt
                    not in self.parms.lang_context.short_macros):
            return tok
        buf.next()
        return defs.TextToken(tok.pos,
                    self.parms.lang_context.short_macros[tok.txt + cur.txt],
                    pos_fix=True)


    def parse_keyvals_dict(self, tokens):
        """
        Parse LaTeX key-value list as dictionary.

        Args:
            List of tokens representing a LaTeX key-value list often
            used for options, e.g. `a=b,a4paper,x={ hoho }`.

        Returns:
            Python dictionary representing the LaTeX key-value list. The
            keys are strings, but the values are lists of tokens for the
            LaTeX values. For entries without `=` in the LaTeX list, the
            value is `None`.
        """
        as_list = self.parse_keyvals_list(tokens)
        return {k: v for (k, v) in as_list}


    def parse_keyvals_list(self, tokens):
        """
        Parse LaTeX key-value list as list of tuples.
        
        Args:
            List of tokens representing a LaTeX key-value list often
            used for options, e.g. `a=b,a4paper,x={ hoho }`.
        
        Returns:
            Python list of tuples representing the LaTeX key-value list.
            The first entries of the tuples are the keys as strings. The
            second entries of the tuples are the values as lists of
            tokens. For entries without `=` in the LaTeX list, the
            second entry is `None`.
        
        See also `Parser.parse_keyvals_dict`.
        """
        # FIXME: Parsing of the key name is not really robust.
        buf = scanner.Buffer(tokens)
        values = []
        while True:
            tok = buf.skip_space()
            if not tok:
                break
            key = []
            while type(tok) is defs.TextToken and tok.txt not in ('=', ','):
                key.append(tok)
                tok = buf.next()
            key = self.get_text_expanded(key)
            tok = buf.skip_space()
            if not tok or tok.txt == ',':
                # no value given with `key=value`
                tok = buf.next()
                values.append((key, None))
                continue
            buf.next()                  # skip `=`
            tok = buf.skip_space()      # skip leading space of value
            val = []
            while tok and tok.txt != ',':
                if tok.txt == '{':
                    # `{...}` protects space and `,`
                    seq = self.arg_buffer(buf, 0).all()
                    if len(seq) == 1 and type(seq[0]) is defs.VoidToken:
                        # this was an empty `{}`
                        seq = []
                    else:
                        # braces `{}` have been removed by arg_buffer()
                        seq = ([defs.SpecialToken(tok.pos, '{')] + seq
                                    + [defs.SpecialToken(seq[-1].pos, '}')])
                    val += seq
                    tok = buf.cur()
                else:
                    val.append(tok)
                    tok = buf.next()
            if val and type(val[-1]) is defs.SpaceToken:
                # skip trailing space of value
                val.pop()
            values.append((key, val))
            buf.next()  # skip ','
        return values


    def expand_keyvals(self, keyvals):
        """
        Expand key-value list to text form.

        Args:
            keyvals: List of tuples `(key, value)` as returned by
              `Parser.parse_keyvals_list` where `value` is a list of
              tokens or None.

        Returns:
            The same list, but with the list of tokens expanded to
            strings.
        """
        def f(kv):
            if kv[1] is None:
                return kv
            return (kv[0], self.get_text_expanded(kv[1]))
        return [f(kv) for kv in keyvals]

    #   roughly approximated version of \def
    #   - macro name must have form \xyz
    #   - XXX:
    #       - on expansion, absence of literal parameter tokens like '[' will
    #         consume other tokens,
    #       - these parameter tokens may mistakenly be enclosed in {} braces
    #       - space in parameter text is not correctly treated
    #
    def parse_def_macro(self, buf, start):
        buf.next()
        tok = buf.skip_space()
        if not tok:
            return utils.latex_error(self, '\\def: missing macro name', start)
        if type(tok) is not defs.MacroToken:
            return utils.latex_error(self, '\\def: illegal macro name "'
                                        + tok.txt + '"', tok.pos)
        name = tok.txt
        args = []
        while True:
            buf.next()
            tok = buf.skip_space()
            if not tok:
                return utils.latex_error(self, '\\def: missing macro body',
                                        start)
            if tok.txt == '{':
                break
            args.append(tok)
        repl = self.arg_buffer(buf, tok.pos).all()

        n = 1
        arg_pos_map = []
        for k, t in enumerate(args, start=1):
            if type(t) is defs.ArgumentToken:
                if t.arg != n:
                    return utils.latex_error(self,
                                                '\\def: unexpected argument '
                                                + repr(t.txt), t.pos)
                n += 1
                arg_pos_map.append(k)

        repl_mapped = []
        for t in repl:
            if type(t) is defs.ArgumentToken:
                if t.arg < 1 or t.arg > len(arg_pos_map):
                    return utils.latex_error(self,
                            '\\def: illegal argument reference ' + repr(t.txt),
                            t.pos)
                t = copy.copy(t)
                t.arg = arg_pos_map[t.arg - 1]
            repl_mapped.append(t)

        self.the_macros[name] = defs.Macro(self.parms, name,
                                        args='A'*len(args), repl=repl_mapped,
                                        scanned=True)
        return [defs.ActionToken(start)]


    def iter_token_levels(self, tokens):
        """
        Generate an iterator that walks over tokens and appends the
        nesting levels of brackets `{}`.
        """
        lev = 0
        for tok in tokens:
            if not tok:
                continue
            if tok.txt == '{':
                lev += 1
            elif tok.txt == '}':
                lev -= 1
            yield tok, lev
