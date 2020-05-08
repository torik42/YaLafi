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
#   - add fields for ALE interface
#
def output_json(tex, plain, charmap, matches, json_get, file, out):
    def f(m):
        m = utils.map_match_position(m, tex, charmap)

        beg = json_get(m, 'offset', int)
        m['fromy'] = tex.count('\n', 0, beg)
        nl = tex.rfind('\n', 0, beg) + 1
        m['fromx'] = beg - nl
        m['fromx_b'] = len(tex[nl:beg].encode())
        end = beg + json_get(m, 'length', int) - 1
        m['toy'] = tex.count('\n', 0, end)
        nl = tex.rfind('\n', 0, end) + 1
        m['tox'] = end - nl + 1
        m['tox_b'] = len(tex[nl:end+1].encode())

        cont = json_get(m, 'context', dict)
        cont_text = json_get(cont, 'text', str)
        cont_offset = json_get(cont, 'offset', int)
        cont_length = json_get(cont, 'length', int)
        m['context']['length_b'] = len(cont_text
                        [cont_offset:cont_offset+cont_length].encode())
        m['context']['offset_b'] = len(cont_text[:cont_offset].encode())
        return m
    message = {'matches': [f(m) for m in matches]}
    out.write(json.dumps(message))

def generate_json_report(cmdline, proofreader, json_get, out):
    for file in cmdline.file:
        (latex, plain, charmap, matches) = proofreader(file)
        output_json(latex, plain, charmap, matches, json_get, file, out)

