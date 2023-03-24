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
Collection of classes used within :mod:`yalafi`.

It includes the :class:`InitModule` used for python description of LaTeX
packages and document classes, many tokens like :class:`TextToken` used
by the parsing mechanism and :class:`Macro`, and :class:`Environ`,
:class:`EquEnv` for python representation of LaTeX commands,
environments, and math environments, respectively.
"""

from yalafi import utils


class InitModule:
    """
    Object to be returned by :func:`init_module` function of Python modules for
    LaTeX packages and document classes.
    """
    def __init__(self, macros_latex='', macros_python=None, environments=None,
                       inject_tokens=None):
        if macros_python is None:
            macros_python = []
        if environments is None:
            environments = []
        if inject_tokens is None:
            inject_tokens = []
        self.macros_latex = macros_latex
        self.macros_python = macros_python
        self.environs = environments
        self.inject_tokens = inject_tokens


class Printable:
    """
    Base class for all tokens which implements a functions to print
    tokens to the console.
    """
    def __repr__(self):
        variables = list(v for v in dir(self) if not v.startswith('_'))
        variables.sort()
        def get(v):
            return self.__getattribute__(v)
        is_not_list = list(v + '=' + repr(get(v)) for v in variables
                                    if type(get(v)) is not list)
        is_list = list(v + '=' + repr(get(v)) for v in variables
                                    if type(get(v)) is list)
        class_name = self.__class__.__name__
        return class_name + '(' + ', '.join(is_not_list + is_list) + ')'


class TextToken(Printable):
    r"""
    Base class for all non expandable tokens. Additionally used as token
    for pure text.

    Attributes:
        pos: Position of first character of :attr:`txt` in source.
        txt: String with the text of the token.
        pos_fix: A Boolean indicating, whether subsequent characters
          have the same position, or an incremented position.

    Example:
      If ``something`` is parsed, it will have
      :class:`TextToken(txt='something', pos=0, pos_fix=False)` such that
      the character ``o`` has position ``1``, ``m`` has position ``2``,
      and so on. But if ``\command{}`` expands to ``my long text``, the
      resulting token will be :func:`TextToken(txt='my long text',
      pos=0, pos_fix=True)` and all characters in ``'my long text'``
      have position ``0`` because they stem from the expanded
      ``\command{}``.
    """

    def __init__(self, pos, txt, pos_fix=False):
        self.pos = pos
        self.txt = txt
        self.pos_fix = pos_fix


class SpaceToken(TextToken):
    """
    Token for only spaces, but not paragraph breaks.

    See :class:`ParagraphToken` for paragraph breaks and :class:`TextToken` for all
    arguments.
    """

    # pylint: disable-next=useless-parent-delegation
    def __init__(self, pos, txt, pos_fix=False):
        super().__init__(pos, txt, pos_fix)


class ParagraphToken(TextToken):
    """
    Token for paragraph breaks.

    See :class:`TextToken` for all attributes.
    """

    # pylint: disable-next=useless-parent-delegation
    def __init__(self, pos, txt, pos_fix=False):
        super().__init__(pos, txt, pos_fix)


class CommentToken(TextToken):
    """
    Token for LateX comments ``% …``.

    See :class:`TextToken` for all attributes.
    """

    def __init__(self, pos, txt):
        super().__init__(pos, txt)


class SpecialToken(TextToken):
    r"""
    Token for special characters and commands like ``{``, ``}``, ``\,``.
    See :attr:`parameters.Parameters().special_tokens`.

    See :class:`TextToken` for all attributes.
    """

    def __init__(self, pos, txt):
        super().__init__(pos, txt)


class MacroToken(TextToken):
    r"""
    Token for macros, i.e. LaTeX commands like ``\someCommand``.

    Attributes:
      txt: String with the name of the macro including the preceding
        backslash ``\``.
      pos: Position of the ``\`` in LaTeX source.
    """

    def __init__(self, pos, txt):
        super().__init__(pos, txt)


class BeginToken(TextToken):
    r"""
    Token for ``\begin`` command.

    Attributes:
      txt: usually ``'\\begin'``.
      pos: Position of the ``\`` in LaTeX source.
    """

    # TODO: Fix `txt = '\\begin'`?
    def __init__(self, pos, txt):
        super().__init__(pos, txt)


class EndToken(TextToken):
    r"""
    Token for ``\end`` command.

    Attributes:
      txt: usually ``'\\end'``.
      pos: Position of the ``\`` in LaTeX source.
    """

    # TODO: Fix `txt = '\\end'`?
    def __init__(self, pos, txt):
        super().__init__(pos, txt)


class ItemToken(TextToken):
    r"""
    Token for ``\item`` command.

    Attributes:
      txt: usually ``'\\item'``.
      pos: Position of the ``\`` in LaTeX source.
    """

    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class AccentToken(TextToken):
    r"""
    Token for accent macros like ``\'`` and ``\"``.

    All used accent macros are defined in
    :attr:`yalafi.parameters.Parameters().accent_macros`.

    See :class:`TextToken` for all attributes.
    """

    def __init__(self, pos, txt):
        super().__init__(pos, txt)


class VerbatimToken(TextToken):
    r"""
    Token for verbatim parts inside ``\verb&…&`` or
    ``\begin{verbatim}…\end{verbatim}``.

    Attributes:
        pos: Position of the first character of the verbatim part,
          e.g. ``…`` above, in LaTeX source.
        txt: The verbatim part, e.g. only ``…``.
        environ: Boolean indicating whether the verbatim part was inside
          an environment.
    """

    def __init__(self, pos, txt, environ=False):
        super().__init__(pos, txt)
        self.environ = environ


class ArgumentToken(TextToken):
    r"""
    Token for argument replacement symbol like ``#2`` appearing for
    example within ``\newcommand`` statements.

    Attributes:
        pos: Position of character ``#`` in source.
        txt: String of ``#`` followed by the argument number, e.g. ``#2``.
        arg: Integer representation of the argument number, e.g. ``2``.
    """

    def __init__(self, pos, txt, arg):
        super().__init__(pos, txt)
        self.arg = arg


class ActionToken(TextToken):
    r"""
    Token that is included whenever a macro is expanded.

    In order to avoid creation of new blank lines by macros expanding to
    space or “nothing”, we include an :class:`ActionToken` whenever
    expanding a macro. Method
    :meth:`yalafi.parser.Parser.remove_pure_action_lines` removes all
    lines only containing space and at least one such token. Initially
    empty lines are retained since they do not contain an
    :class:`ActionToken`.
    """

    def __init__(self, pos):
        super().__init__(pos, '')


class VoidToken(TextToken):
    """
    Empty token which is returned after parsing empty arguments.
    """

    def __init__(self, pos):
        super().__init__(pos, '')


class LanguageToken(TextToken):
    """
    Token inserted to change the language.
    """

    def __init__(self, pos, lang='', back=False, hard=False, brk=False):
        super().__init__(pos, '')
        self.lang = lang
        """
        A string representing of the language. Should be a key of
        `Parameters.parser_language_settings`. Might be empty for
        `back=True`.
        """
        self.back = back
        """
        A Boolean indicating whether the language should be reset to the
        last active language.
        """
        self.hard = hard
        """
        A boolean indicating to replace the current language without
        keeping it in the language stack.
        """
        self.brk = brk
        """
        A boolean indicating whether a break of the text flow should be
        enforced.
        """


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
    r"""
    Python representation of a LaTeX macro (also called LaTeX command).

    Attributes:
        parms: :class:`yalafi.parameters.Parameters` object for handling
          current settings.
        name: Name of the LaTeX Macro including the leading ``\``.
        args: String encoding the arguments of the macro. It
          consists of characters ``A``, ``O`` and ``*`` representing

          * ``A``: a mandatory argument, which may be a single token or
            a sequence enclosed in ``{}`` braces
          * ``O``: an optional argument in ``[]`` brackets
          * ``*``: an optional asterisk.

          Defaults to ``''``.
        repl: Replacement string or macro handler function. Defaults
          to ``''``.
        defaults: List of replacement strings for absent optional
          arguments or ``None``. Defaults to ``None``.
        scanned: _description_. Defaults to False.
        extract: like ``repl``, but the resulting text is appended at
          the end of to the main text, separated by blank lines.
          Used for macros like ``\footnote``. Defaults to ``''``.
    """

    def __init__(self, parms, name, args='', repl='', defaults=None,
                       scanned=False, extract=''):
        if defaults is None:
            defaults = []
        super().__init__(parms, name, args, repl, defaults, scanned, extract)


class Environ(Expandable):
    def __init__(self, parms, name, args='', repl='', defaults=None,
                       add_pars=True, remove=False, items=None, end_func=None):
        if defaults is None:
            defaults = []
        super().__init__(parms, name, args, repl, defaults)
        self.add_pars=add_pars
        self.remove=remove
        self.items=items
        self.end_func=end_func


class EquEnv(Environ):
    def __init__(self, parms, name, args='', repl='', defaults=None,
                       remove=False):
        if defaults is None:
            defaults = []
        super().__init__(parms, name, args, repl, defaults,
                         add_pars=False, remove=remove)
