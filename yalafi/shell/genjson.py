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

##################################################################
#
#   JSON output
#
##################################################################

import json
from . import utils

#   - correct offset and length in each match
#   - add field priv with sub-fields fromx, fromy, tox, toy
#
def output_json(tex, plain, charmap, matches, json_get, file, out):
    def f(m):
        m = utils.map_match_position(m, tex, charmap)
        priv = m['priv'] = {}
        beg = json_get(m, 'offset', int)
        priv['fromy'] = tex.count('\n', 0, beg)
        nl = tex.rfind('\n', 0, beg) + 1
        priv['fromx'] = beg - nl
        end = beg + json_get(m, 'length', int) - 1
        priv['toy'] = tex.count('\n', 0, end)
        nl = tex.rfind('\n', 0, end) + 1
        priv['tox'] = end - nl + 1
        return m
    message = {'matches': [f(m) for m in matches]}
    out.write(json.dumps(message))

def generate_json_report(cmdline, proofreader, json_get, out):
    for file in cmdline.file:
        (latex, plain, charmap, matches) = proofreader(file)
        output_json(latex, plain, charmap, matches, json_get, file, out)

