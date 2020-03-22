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
import re
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

def replace_phrases(txt, pos, lines):
    for lin in lines:
        i = lin.find('#')
        if i >= 0:
            lin = lin[:i]
        lin = lin.split()

        t = s = ''
        for i in range(len(lin)):
            if lin[i] == '&':
                break
            t += s + re.escape(lin[i])
                    # protect e.g. '.' and '$'
            s = r'(?:[ \t]*\n[ \t]*|[ \t]+)'
                    # at least one space character, but stay in paragraph
        if not t:
            continue
        if t[0].isalpha():
            t = r'\b' + t       # require word boundary
        if t[-1].isalpha():
            t = t + r'\b'

        r = ' '.join(lin[i+1:])
        txt, pos = substitute(txt, pos, t, r)
    return txt, pos

def substitute(i_txt, i_pos, expr, repl):
    o_txt = ''
    o_pos = []
    r_len = len(repl)
    last = 0
    for m in re.finditer(expr, i_txt):
        m_len = len(m.group(0))
        if not m_len:
            continue
        cur = m.start(0)
        o_txt += i_txt[last:cur] + repl
        o_pos += i_pos[last:cur]
        if r_len <= m_len:
            o_pos += i_pos[cur:cur+r_len]
        else:
            o_pos += (i_pos[cur:cur+m_len]
                        + [i_pos[cur+m_len-1]] * (r_len - m_len))
        last = m.end(0)
    return o_txt + i_txt[last:], o_pos + i_pos[last:]

