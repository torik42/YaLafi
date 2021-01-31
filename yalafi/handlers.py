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
from . import utils

#   macros \newcommand, \renewcommand
#
def h_newcommand(parser, buf, mac, args, delim, pos):
    name = parser.get_text_direct(args[1])
    if name in parser.parms.newcommand_ignore:
        return []
    nargs = parser.get_text_expanded(args[2])
    nargs = int(nargs) if nargs.isdecimal() else 0
    for a in [b for b in args[4] if type(b) is defs.ArgumentToken]:
        if a.arg < 1 or a.arg > nargs:
            return utils.latex_error('illegal argument #' + str(a.arg)
                                + ' in definition of macro ' + name,
                                        a.pos, parser.latex, parser.parms)
    if args[3]:
        if nargs < 1:
            return utils.latex_error(
                    'illegal default value in definition of macro ' + name,
                            args[1][0].pos, parser.latex, parser.parms)
        parser.the_macros[name] = defs.Macro(parser.parms,
                                name, args='O' + 'A' * (nargs - 1),
                                repl=args[4], defaults=[args[3]], scanned=True)
    else:
        parser.the_macros[name] = defs.Macro(parser.parms,
                                name, args='A' * nargs,
                                repl=args[4], scanned=True)
    return []

#   \begin{theorem}[opt]
#   - if present, add content of option opt in () parantheses
#   - add '.'
#   --> now only used by h_newtheorem()
#
def h_theorem(name):
    def handler (parser, buf, mac, args, delim, pos):
        out = [defs.TextToken(pos, name, pos_fix=True)]
        if args[0]:
            # there is a [.] option
            out.append(defs.SpaceToken(pos, ' ', pos_fix=True))
            out.append(defs.TextToken(pos, '(', pos_fix=True))
            out += args[0]
            out.append(defs.TextToken(args[0][-1].pos,
                                        ').', pos_fix=True))
            out.append(defs.SpaceToken(args[0][-1].pos,
                                        '\n', pos_fix=True))
        else:
            out.append(defs.TextToken(pos, '.', pos_fix=True))
            out.append(defs.SpaceToken(pos, '\n', pos_fix=True))
        return out
            
    # this creates a closure
    return handler

#   \newtheorem
#
def h_newtheorem(parser, buf, mac, args, delim, pos):
    name = parser.get_text_expanded(args[0])
    title = parser.get_text_expanded(args[2])
    def f(parser, options, position):
        parms = parser.parms
        envs = [defs.Environ(parms, name, args='O', repl=h_theorem(title))]
        return defs.InitModule(environments=envs)
    parser.modify_parameters(f, [], pos)
    return []

#   heading macros: append '.', unless last char in parms.heading_punct
#
def h_heading(parser, buf, mac, args, delim, pos):
    arg = args[2]
    txt = parser.get_text_expanded(arg).strip()
    if (txt and parser.parms.heading_punct
                and txt[-1] not in parser.parms.heading_punct):
        arg.append(defs.TextToken(arg[-1].pos, '.'))
    return arg

#   \phantom, \hphantom
#
def h_phantom(parser, buf, mac, args, delim, pos):
    if len(parser.get_text_expanded(args[0])) > 0:
        return [defs.SpecialToken(pos, '\\;')]
    return []

#   macro \cite[opt]
#
def h_cite(parser, buf, mac, args, delim, pos):
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

#   macro \LTinput: read macro definitions from file
#   - this also activates packages and switches languages
#   - check for recursive inclusion of a file
#
def h_load_defs(parser, buf, mac, args, delim, pos):
    if not parser.read_macros:
        return []
    file = parser.get_text_expanded(args[0])
    ok, latex = parser.read_macros(file)
    if not ok:
        return utils.latex_error('could not read file ' + repr(file),
                                        pos, parser.latex, parser.parms)
    try:
        toks = parser.parser_work(latex)
    except RecursionError:
        utils.fatal('Problem while executing "' + mac.name + '{' + file
                    + '}".\n' + '*** Is the file included recursively?')
    return utils.filter_set_toks(toks, pos, defs.LanguageToken)

#   read definitions for a LaTeX package
#
def h_load_module(prefix):
    def f(parser, buf, mac, args, delim, pos):
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
    return f

