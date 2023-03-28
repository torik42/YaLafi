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
Collection of macro handlers for various LaTeX commands.
"""

import re
from yalafi import defs
from yalafi import utils
from yalafi import scanner


def g_newcommand(overwrite=True):
    r"""
    Generator for ``\newcommand``, ``\renewcommand`` and ``\providecommand``.

    Args:
        overwrite: Boolean deciding, whether the returned handler
          overwrites existing commands. Defaults to True.

    Returns:
        Macro Handler for ``\newcommand``, ``\renewcommand`` and
        ``\providecommand``. Set ``overwrite=False`` for
        ``\providecommand``.
    """
    # pylint: disable-next=redefined-outer-name
    def h_newcommand(parser, buf, mac, args, delim, pos):
        r"""
        Macro handler for `\newcommand` and `\renewcommand`.
        """
        name = parser.get_text_direct(args[1])
        if name in parser.parms.newcommand_ignore:
            return []
        if not overwrite and name in parser.the_macros:
            return []
        nargs = parser.get_text_expanded(args[2])
        nargs = int(nargs) if nargs.isdecimal() else 0
        for a in [b for b in args[4] if type(b) is defs.ArgumentToken]:
            if a.arg < 1 or a.arg > nargs:
                return utils.latex_error(parser, 'illegal argument #' + str(a.arg)
                                    + ' in definition of macro ' + name, a.pos)
        if args[3]:
            if nargs < 1:
                return utils.latex_error(parser,
                        'illegal default value in definition of macro ' + name,
                        args[1][0].pos)
            parser.the_macros[name] = defs.Macro(parser.parms,
                                    name, args='O' + 'A' * (nargs - 1),
                                    repl=args[4], defaults=[args[3]], scanned=True)
        else:
            parser.the_macros[name] = defs.Macro(parser.parms,
                                    name, args='A' * nargs,
                                    repl=args[4], scanned=True)
        return []
    return h_newcommand


h_newcommand = g_newcommand(overwrite=True)


def h_theorem(name):
    r"""
    Generator for macro handler for theorem like environments.

    The returned handler will output the `name` followed by a period.
    For named theorems, the optional argument will be inserted in
    parenthesis before the period.

    Args:
        name: name of the theorem like environment.

    Returns:
        A macro handler for the theorem like environment `name`.
    """
    # TODO: Rename in next major release to g_theorem
    #   reflecting that it generates a macro handler function `handler`.
    def handler(parser, buf, mac, args, delim, pos):
        out = [defs.TextToken(pos, name, pos_fix=True)]
        if args[0]:
            # named theorem
            out.append(defs.SpaceToken(pos, ' ', pos_fix=True))
            out.append(defs.TextToken(pos, '(', pos_fix=True))
            out += args[0]
            out.append(defs.TextToken(args[0][-1].pos,
                                        ').', pos_fix=True))
            out.append(defs.SpaceToken(args[0][-1].pos,
                                        '\n', pos_fix=True))
        else:
            # unnamed theorem
            out.append(defs.TextToken(pos, '.', pos_fix=True))
            out.append(defs.SpaceToken(pos, '\n', pos_fix=True))
        return out
    return handler


def h_newtheorem(parser, buf, mac, args, delim, pos):
    r"""
    Macro handler for `\newtheorem`.
    """
    name = parser.get_text_expanded(args[0])
    title = parser.get_text_expanded(args[2])
    def f(parser, options, position):  # pylint: disable=unused-argument
        parms = parser.parms
        envs = [defs.Environ(parms, name, args='O', repl=h_theorem(title))]
        return defs.InitModule(environments=envs)
    parser.modify_parameters('<h_newtheorem>', f, [], pos)
    return []


def h_heading(parser, buf, mac, args, delim, pos):
    r"""
    Macro handler for heading commands like ``\section``. It appends a
    period to the heading unless the heading ends with a character in
    :attr:`yalafi.parameters.Parameters.heading_punct`.
    """
    arg = args[2]
    txt = parser.get_text_expanded(arg).strip()
    if (txt and parser.parms.heading_punct
                and txt[-1] not in parser.parms.heading_punct):
        arg.append(defs.TextToken(arg[-1].pos, '.'))
    return arg


def h_phantom(parser, buf, mac, args, delim, pos):
    r"""
    Macro handler for `\phantom` and `\hphantom` replacing them with
    small space, if they contain text.
    """
    if len(parser.get_text_expanded(args[0])) > 0:
        return [defs.SpecialToken(pos, '\\;')]
    return []


numbers = re.compile(r'\s*(\d+[.,]?\d*|[.,]\d+)')
r"Regex for matching numbers in `\hspace` arguments."

def h_hspace(parser, buf, mac, args, delim, pos):
    r"""
    Macro handler for `\hspace` replacing it with space, unless the
    argument is (explicitly) zero length.

    Additions and subtractions of lengths are currently not supported.
    """
    arg = parser.get_text_expanded(args[1])
    match = numbers.match(arg)
    if match and float(match.group(1).replace(',', '.')) == 0:
        return []
    return [defs.SpaceToken(pos, ' ')]


def h_linebreak(parser, buf, mac, args, delim, pos):
    r"""
    Handler for macro ``\linebreak`` taking one optional argument.

    Adds no additional space for optional argument '0','1','2','3'.
    Adds one SpaceToken for argument '4', or no argument.  Adds output
    from :func:`utils.latex_error` for other arguments, we allow
    additional white space.
    """
    if len(args[0]) == 0:
        return [defs.SpaceToken(pos, ' ')]
    else:
        arg = parser.get_text_expanded(args[0]).strip()
        if arg == '4':
            return [defs.SpaceToken(pos, ' ')]
        elif arg in ['0','1','2','3']:
            # There is no line break for arguments 0,1,2,3
            return []
    # For all other arguments, return an error
    return utils.latex_error(parser, r'`\linebreak` only takes values 0,1,2,3 or 4', pos)


def h_cite(parser, buf, mac, args, delim, pos):
    r"""
    Macro handler for the default LaTeX `\cite` command.

    See :func:`yalafi.packages.biblatex.h_cite` for the corresponding
    handler after loading BibLaTeX.
    """
    if args[0]:
        out = [defs.TextToken(pos, '[0,', pos_fix=True),
                    defs.SpaceToken(pos, ' ', pos_fix=True)]
        out += args[0]
        out += [defs.TextToken(args[0][-1].pos, ']'),
                    defs.ActionToken(args[0][-1].pos)]
    else:
        out = [defs.TextToken(pos, '[0]', pos_fix=True),
                    defs.ActionToken(pos)]
    return out


def h_load_defs(parser, buf, mac, args, delim, pos):
    r"""
    Macro handler for ``\LTinput``.

    It updates the parser by reading the provided file. Hence, it
    updates macro definitions and activates loaded packages. It only
    returns the Language Tokens from the loaded file such that switching
    languages also works.

    If the file could not be found, a LaTeX error is added to the
    output. If the file is included recursively, the error is printed to
    stderr and the program stops.
    """
    if not parser.read_macros:
        return []
    file = parser.get_text_expanded(args[0])
    ok, latex = parser.read_macros(file)
    if not ok:
        return utils.latex_error(parser, 'could not read file ' + repr(file),
                                        pos)
    try:
        toks = parser.parser_work(latex, file)
    except RecursionError:
        utils.fatal('Problem while executing "' + mac.name + '{' + file
                    + '}".\n' + '*** Is the file included recursively?')
    return utils.filter_set_toks(toks, pos, defs.LanguageToken)

#   read definitions for a LaTeX package
#
def h_load_module(prefix):
    r"""
    Generator for a macro handler function for `\documentclass` and
    `\usepackage`.

    The returned handler will try to load the package definition from
    the python module `prefix.my_package` when using
    `\usepackage{my-package}`.

    Args:
        prefix: Name of the python (sub)package which contains the
          modules corresponding to LaTeX packages.

    Returns:
        A macro handler function for `\documentclass` and `\usepackage`.

    See also `yalafi.utils.get_module_handler`.
    """
    # TODO: Rename in next major release to g_load_module
    #   reflecting that it generates a macro handler function `handler`.
    def handler(parser, buf, mac, args, delim, pos):
        options = parser.parse_keyvals_list(args[0])
        options = parser.expand_keyvals(options)
        packs = parser.get_text_expanded(args[1])
        out = []
        for p in packs.split(','):
            p = p.strip()
            if p:
                f = utils.get_module_handler(p, prefix)
                out += parser.init_package(p, f, options, pos)
        return utils.filter_set_toks(out, pos, None)
    return handler


def h_makeLowercase(parser, buf, mac, args, delim, pos):
    r"""
    Macro handler for `\MakeLowercase`.

    The argument is expanded first, then all text is replaced with a
    lower case variant.
    """
    toks = parser.expand_sequence(scanner.Buffer(args[0].copy()))
    def f(t):
        if type(t) is defs.TextToken:
            t.txt = t.txt.lower()
        return t
    return [f(t) for t in toks]


def h_makeUppercase(parser, buf, mac, args, delim, pos):
    r"""
    Macro handler for `\MakeUppercase`.

    The argument is expanded first, then all text is replaced with a
    upper case variant.
    """
    toks = parser.expand_sequence(scanner.Buffer(args[0].copy()))
    def f(t):
        if type(t) is defs.TextToken:
            t.txt = t.txt.upper()
        return t
    return [f(t) for t in toks]
