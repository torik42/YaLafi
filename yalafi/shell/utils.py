#
#   Tex2txt, a flexible LaTeX filter
#   YaLafi: Yet another LaTeX filter
#   Copyright (C) 2018-2020 Matthias Baumann
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

import re

#   for an error match from proofreader:
#   map to position to LaTeX text
#
def map_match_position(m, latex, charmap):
    beg = min(max(0, m['offset']), len(charmap) - 1)
    end = min(max(0, beg + m['length'] - 1), len(charmap) - 1)
    offset = abs(charmap[beg]) - 1
    m['offset'] = offset
    length = abs(charmap[end]) - abs(charmap[beg]) + 1
    m['length'] = correct_mark_macroname(offset, length, latex)
    return m

#   HACK:
#   correct the length of a text part marked as error by proofreader,
#   if only a single '\\' is tagged, and if it starts a macro name
#   --> mark the complete macro name
#
def correct_mark_macroname(offset, length, latex):
    if not (length == 1 and 0 <= offset < len(latex) - 1
                    and latex[offset] == '\\'):
        return length
    m = re.search(r'\A\\[A-Za-z]+', latex[offset:])
    return len(m.group(0)) if m else length

