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

from yalafi import tex2txt
import sys

#####################################################################
#
#   text report
#
#####################################################################

#   generate text report from element 'matches' of JSON output
#
#   - compare printMatches() in file CommandLineTools.java in directory
#     languagetool-commandline/src/main/java/org/languagetool/commandline/
#   - XXX: some code duplication with genhtml.begin_match()
#
def output_text_report(tex, plain, charmap, matches, file, out):
    starts = tex2txt.get_line_starts(plain)

    for (nr, m) in enumerate(matches, 1):
        offset = json_get(m, 'offset', int)
        lin = plain.count('\n', 0, offset) + 1
        nl = plain.rfind('\n', 0, offset) + 1
        col = offset - nl + 1
        lc = tex2txt.translate_numbers(tex, plain, charmap, starts, lin, col)

        rule = json_get(m, 'rule', dict)
        out.write('=== ' + file + ' ===\n')

        s = (str(nr) + '.) Line ' + str(lc.lin) + ', column ' + str(lc.col)
                + ', Rule ID: ' + json_get(rule, 'id', str))
        if 'subId' in rule:
                s += '[' + json_get(rule, 'subId', str) + ']'
        out.write(s + '\n')
        out.write('Message: ' + json_get(m, 'message', str) + '\n')

        repls = '; '.join(json_get(r, 'value', str)
                                for r in json_get(m, 'replacements', list))
        out.write('Suggestion: ' + repls + '\n')

        cont = json_get(m, 'context', dict)
        txt = json_get(cont, 'text', str)
        beg = json_get(cont, 'offset', int)
        length = json_get(cont, 'length', int)
        out.write(txt.replace('\t', ' ') + '\n')
        out.write(' ' * beg + '^' * length + '\n')

        if 'urls' in rule:
            urls = json_get(rule, 'urls', list)
            if urls:
                out.write('More info: ' + json_get(urls[0], 'value', str)
                                + '\n')

        out.write('\n')

    out.flush()     # in case redirected to file


#   on option --list-unknown
#
def output_list_unknown(unkn, file, out):
    if not unkn.split():
        return
    out.write('=== ' + file + ' ===\n')
    out.write(unkn)

def generate_text_report(run_proofreader, out):
    if cmdline.server == 'lt':
        sys.stderr.write(msg_LT_server_txt)
    for file in cmdline.file:
        (tex, plain, charmap, matches) = run_proofreader(file)
        if cmdline.list_unknown:
            output_list_unknown(plain, file, out)
        else:
            output_text_report(tex, plain, charmap, matches, file, out)

#   XXX: these should be passed
#
def init(vars):
    global cmdline
    cmdline = vars.cmdline
    global json_get
    json_get = vars.json_get
    global msg_LT_server_txt
    msg_LT_server_txt = vars.msg_LT_server_txt

