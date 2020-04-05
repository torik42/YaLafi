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

from . import utils


class Printable:
    def __repr__(self):
        vars = list(v for v in dir(self) if not v.startswith('_'))
        vars.sort()
        def get(v):
            return self.__getattribute__(v)
        is_not_list = list(v + '=' + repr(get(v)) for v in vars
                                    if type(get(v)) is not list)
        is_list = list(v + '=' + repr(get(v)) for v in vars
                                    if type(get(v)) is list)
        cls = self.__class__.__name__
        return cls + '(' + ', '.join(is_not_list + is_list) + ')'

class TextToken(Printable):
    def __init__(self, pos, txt, pos_fix=False):
        self.pos = pos
        self.txt = txt
        self.pos_fix = pos_fix

class SpaceToken(TextToken):
    def __init__(self, pos, txt, pos_fix=False):
        super().__init__(pos, txt, pos_fix)

class ParagraphToken(TextToken):
    def __init__(self, pos, txt, pos_fix=False):
        super().__init__(pos, txt, pos_fix)

class CommentToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class SpecialToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class MacroToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class BeginToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class EndToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class ItemToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class AccentToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class VerbatimToken(TextToken):
    def __init__(self, pos, txt, environ=False):
        super().__init__(pos, txt)
        self.environ = environ

class ArgumentToken(TextToken):
    def __init__(self, pos, txt, arg):
        super().__init__(pos, txt)
        self.arg = arg

class ActionToken(TextToken):
    def __init__(self, pos):
        super().__init__(pos, '')

class VoidToken(TextToken):
    def __init__(self, pos):
        super().__init__(pos, '')

class MathBeginToken(TextToken):
    def __init__(self, pos, text, env):
        super().__init__(pos, text)
        self.environ = env

class MathElemToken(TextToken):
    def __init__(self, pos, text):
        super().__init__(pos, text)

class MathOperToken(TextToken):
    def __init__(self, pos, text):
        super().__init__(pos, text)

class MathSpaceToken(TextToken):
    def __init__(self, pos, text):
        super().__init__(pos, text)

class Expandable(Printable):
    def __init__(self, parms, name, args, repl, defaults,
                                    scanned=False, extract=''):
        def check(toks, args):
            for t in toks:
                if type(t) is ArgumentToken and not 1 <= t.arg <= len(args):
                    utils.fatal('illegal argument reference ' + repr(t.txt)
                                    + ' for ' + repr(name))
            return toks
        if not all(c in '*AO' for c in args):
            utils.fatal('illegal argument code ' + repr(args)
                            + ' for ' + repr(name))
        self.name = name
        self.args = args
        self.extract = check(parms.scanner.scan(extract), args)
        if scanned:
            self.repl = repl
            self.defaults = defaults
            return
        if callable(repl):
            self.repl = repl
        else:
            self.repl = check(parms.scanner.scan(repl), args)
        self.defaults = [parms.scanner.scan(op) for op in defaults]

class Macro(Expandable):
    def __init__(self, parms, name, args='', repl='', defaults=[],
                                    scanned=False, extract=''):
        super().__init__(parms, name, args, repl, defaults, scanned, extract)

class Environ(Expandable):
    def __init__(self, parms, name, args='', repl='', defaults=[],
                                    add_pars=True, remove=False, items=None):
        super().__init__(parms, name, args, repl, defaults)
        self.add_pars=add_pars
        self.remove=remove
        self.items=items

class EquEnv(Environ):
    def __init__(self, parms, name, args='', repl='', defaults=[],
                                    remove=False):
        super().__init__(parms, name, args, repl, defaults,
                                    add_pars=False, remove=remove)

