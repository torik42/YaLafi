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

def handle_newcommand(parser, buf, mac, args):
    name = parser.get_text_direct(args[0])
    nargs = parser.get_text_expanded(args[1])
    nargs = int(nargs) if nargs.isdecimal() else 0
    for a in [b for b in args[3] if type(b) is defs.ArgumentToken]:
        if a.arg < 1 or a.arg > nargs:
            utils.latex_error('illegal argument #' + str(a.arg)
                                + ' in definition of macro ' + name, a.pos)
    if args[2]:
        if nargs < 1:
            utils.latex_error('illegal default value in definition of macro '
                                    + name, args[0][0].pos)
        parser.the_macros[name] = defs.Macro(name, args='O' + 'A' * (nargs-1),
                                repl=args[3], opts=[args[2]], scanned=True)
    else:
        parser.the_macros[name] = defs.Macro(name, args='A' * nargs,
                                        repl=args[3], scanned=True)
    return []

