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

from . import parameters
import sys


def latex_error(err, pos):
    sys.stderr.write('\n*** LaTeX error:\n' + err
                        + '\npos = ' + str(pos) + '\n')
    sys.exit(1)

def get_txt_pos(toks):
    txt = ''
    pos = []
    for t in toks:
        txt += t.txt
        if t.pos_fix:
            pos += [t.pos] * len(t.txt)
        else:
            pos += list(range(t.pos, t.pos + len(t.txt)))
    return txt, pos

