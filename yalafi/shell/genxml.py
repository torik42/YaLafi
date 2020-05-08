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

from . import utils
import sys
import xml.etree.ElementTree as ET

#####################################################################
#
#   XML report for vim-grammarous
#
#   XXX: only fields necessary for vim-grammarous
#
#####################################################################

#   - XXX: some code duplication with genhtml.begin_match()
#   - byte_offset: report some values in byte rather than character positions
#
def output_xml_report(tex, plain, charmap, matches, byte_offset, file, out):
    out.write('<matches>\n')
    for m in matches:
        m = utils.map_match_position(m, tex, charmap)
        beg = json_get(m, 'offset', int)
        fromy = tex.count('\n', 0, beg)
        nl = tex.rfind('\n', 0, beg) + 1
        if byte_offset:
            fromx = len(tex[nl:beg].encode())
        else:
            fromx = beg - nl
        end = beg + json_get(m, 'length', int) - 1
        toy = tex.count('\n', 0, end)
        nl = tex.rfind('\n', 0, end) + 1
        if byte_offset:
            tox = len(tex[nl:end+1].encode())
        else:
            tox = end - nl + 1

        rule = json_get(m, 'rule', dict)
        category = json_get(rule, 'category', dict)
        category = json_get(category, 'name', str)
        message = json_get(m, 'message', str)
        repls = '#'.join(json_get(r, 'value', str)
                                for r in json_get(m, 'replacements', list))
        cont = json_get(m, 'context', dict)
        cont_text = json_get(cont, 'text', str)
        cont_offset = json_get(cont, 'offset', int)
        cont_length = json_get(cont, 'length', int)
        if byte_offset:
            cont_length = len(cont_text[cont_offset:cont_offset+cont_length]
                                    .encode())
            cont_offset = len(cont_text[:cont_offset].encode())

        xml = {
            'fromy': str(fromy), 'fromx': str(fromx),
            'toy': str(toy), 'tox': str(tox),
            'category': category,
            'msg': message,
            'replacements': repls,
            'context': cont_text,
            'contextoffset': str(cont_offset),
            'errorlength': str(cont_length),
        }
        s = ET.tostring(ET.Element('error', xml), encoding='unicode') + '\n'
        out.write(s)
    out.write('</matches>\n')


def generate_xml_report(run_proofreader, out, byte_offset):
    if cmdline.server == 'lt':
        sys.stderr.write(msg_LT_server_txt)
    for file in cmdline.file:
        (tex, plain, charmap, matches) = run_proofreader(file)
        output_xml_report(tex, plain, charmap, matches, byte_offset, file, out)

#   XXX: these should be passed
#
def init(vars):
    global cmdline
    cmdline = vars.cmdline
    global json_get
    json_get = vars.json_get
    global msg_LT_server_txt
    msg_LT_server_txt = vars.msg_LT_server_txt

