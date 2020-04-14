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
from . import utils
import re

#####################################################################
#
#   HTML report
#
#####################################################################

#   protect text between HTML tags from being seen as HTML code,
#   preserve text formatting
#   - '<br>\n' is used by generate_highlight() and add_line_numbers()
#
def protect_html(s):
    s = re.sub(r'&', r'&amp;', s)
    s = re.sub(r'"', r'&quot;', s)
    s = re.sub(r'<', r'&lt;', s)
    s = re.sub(r'>', r'&gt;', s)
    s = re.sub(r'\t', ' ' * 8, s)
    s = re.sub(r' ', '&ensp;', s)
    s = re.sub(r'\n', r'<br>\n', s)
    return s

#   generate HTML tag from LT message
#
def begin_match(m, lin, unsure):
    cont = json_get(m, 'context', dict)
    txt = json_get(cont, 'text', str)
    beg = json_get(cont, 'offset', int)
    end = beg + json_get(cont, 'length', int)
    rule = json_get(m, 'rule', dict)

    msg = protect_html(json_get(m, 'message', str)) + '\n'

    msg += protect_html('Line ' + str(lin) + ('+' if unsure else '')
                        + ': >>>' + txt[beg:end] + '<<<')
    rule_id = json_get(rule, 'id', str)
    if 'subId' in rule:
            rule_id += '[' + json_get(rule, 'subId', str) + ']'
    msg += protect_html('    (Rule ID: ' + rule_id + ')') + '\n'

    repls = '; '.join(json_get(r, 'value', str)
                        for r in json_get(m, 'replacements', list))
    msg += 'Suggestion: ' + protect_html(repls) + '\n'

    txt = txt[:beg] + '>>>' + txt[beg:end] + '<<<' + txt[end:]
    msg += 'Context: ' + protect_html(txt)

    style = highlight_style_unsure if unsure else highlight_style
    beg_tag = '<span style="' + style + '" title="' + msg + '">'
    end_href = ''
    if cmdline.link and 'urls' in rule:
        urls = json_get(rule, 'urls', list)
        if urls:
            beg_tag += ('<a href="' + json_get(urls[0], 'value', str)
                        + '" target="_blank">')
            end_href = '</a>'
    return (beg_tag, end_href)

def end_match():
    return '</span>'

#   hightlight a text region
#   - avoid that span tags cross line breaks (otherwise problems in <table>)
#
def generate_highlight(m, s, lin, unsure):
    (pre, end_href) = begin_match(m, lin, unsure)
    s = protect_html(s)
    post = end_href + end_match()
    def f(m):
        return pre + m.group(1) + post + m.group(2)
    return re.sub(r'((?:.|\n)*?(?!\Z)|(?:.|\n)+?)(<br>\n|\Z)', f, s)

#   generate HTML output
#
def generate_html(tex, charmap, matches, file):

    s = 'File "' + file + '" with ' + str(len(matches)) + ' problem(s)'
    title = protect_html(s)
    anchor = file
    anchor_overlap = file + '-@@@'
    prefix = '<a id="' + anchor + '"></a><H3>' + title + '</H3>\n'

    # collect data for highlighted places
    #
    hdata = []
    for m in matches:
        beg = json_get(m, 'offset', int)
        end = beg + max(1, json_get(m, 'length', int))
        if beg < 0 or end < 0 or beg >= len(charmap) or end >= len(charmap):
            tex2txt.fatal('generate_html():'
                            + ' bad message read from proofreader')
        h = tex2txt.Aux()
        h.unsure = (charmap[beg] < 0 or charmap[max(beg, end - 1)] < 0)
        h.beg = abs(charmap[beg]) - 1
        h.end = abs(charmap[max(beg, end - 1)])         # see issue #21
        if h.unsure or h.end <= h.beg:
            h.end = h.beg + 1

        if h.end == h.beg + 1 and tex[h.beg] == '\\':
            # HACK:
            # if matched a single \ that is actually followed by macro name:
            # also highlight the macro name
            h.end = h.beg + utils.correct_mark_macroname(h.beg, 1, tex)
        elif h.unsure and tex[h.beg].isalpha():
            # HACK:
            # if unsure: mark till end of word (only letters)
            s = re.search(r'\A.[^\W0-9_]+', tex[h.beg:])
            if s:
                h.end = h.beg + len(s.group(0))

        h.beglin = tex.count('\n', 0, h.beg)
        h.endlin = tex.count('\n', 0, h.end) + 1
        h.lin = h.beglin
        h.m = m
        hdata.append(h)

    # group adjacent matches into regions
    #
    regions = []
    starts = tex2txt.get_line_starts(tex)
    for h in hdata:
        h.beglin = max(h.beglin - cmdline.context, 0)
        h.endlin = min(h.endlin + cmdline.context, len(starts) - 1)
        if not regions or h.beglin >= max(h.endlin for h in regions[-1]):
            # start a new region
            regions.append([h])
        else:
            # match is part of last region
            regions[-1].append(h)

    # produce output
    #
    res_tot = ''
    overlaps = []
    line_numbers = []
    for reg in regions:
        #
        # generate output for one region:
        # collect all matches in that region
        #
        beglin = reg[0].beglin
        endlin = max(h.endlin for h in reg)
        res = ''
        last = starts[beglin]
        for h in reg:
            s = generate_highlight(h.m, tex[h.beg:h.end], h.lin + 1, h.unsure)
            if h.beg < last:
                # overlapping with last message
                overlaps.append((s, h.lin + 1))
                continue
            res += protect_html(tex[last:h.beg])
            res += s
            last = h.end

        res += protect_html(tex[last:starts[endlin]])
        res_tot += res + '<br>\n'
        line_numbers += list(range(beglin, endlin)) + [-1]

    if not line_numbers:
        # no problems found: just display first cmdline.context lines
        endlin = min(cmdline.context, len(starts) - 1)
        res_tot = protect_html(tex[:starts[endlin]])
        line_numbers = list(range(endlin))
    if line_numbers:
        res_tot = add_line_numbers(res_tot, line_numbers)

    postfix = ''
    if overlaps:
        prefix += ('<a href="#' + anchor_overlap + '">'
                        + '<H3>Overlapping message(s) found:'
                        + ' see here</H3></a>\n')
        postfix = ('<a id="' + anchor_overlap + '"></a><H3>'
                    + protect_html('File "' + file + '":')
                    + ' overlapping message(s)</H3>\n')
        postfix += '<table cellspacing="0">\n'
        for (s, lin) in overlaps:
            postfix += ('<tr><td style="' + number_style
                            + '" align="right" valign="top">' + str(lin)
                            + '&nbsp;&nbsp;</td><td>' + s + '</td></tr>\n')
        postfix += '</table>\n'

    return (title, anchor, prefix + res_tot + postfix, len(matches))

#   add line numbers using a large <table>
#
def add_line_numbers(s, line_numbers):
    aux = tex2txt.Aux()
    aux.lineno = 0
    def f(m):
        lin = line_numbers[aux.lineno]
        s = str(lin + 1) if lin >= 0 else ''
        aux.lineno += 1
        return (
            '<tr>\n<td style="' + number_style
            + '" align="right" valign="top">' + s + '&nbsp;&nbsp;</td>\n<td>'
            + m.group(1) + '</td>\n</tr>\n'
        )
    s = re.sub(r'((?:.|\n)*?(?!\Z)|(?:.|\n)+?)(<br>\n|\Z)', f, s)
    return '<table cellspacing="0">\n' + s + '</table>\n'


def generate_html_report(run_proofreader, out):

    #   generate HTML report: a part for each file
    #
    html_report_parts = []
    for file in cmdline.file:
        (tex, plain, charmap, matches) = run_proofreader(file)
        html_report_parts.append(generate_html(tex, charmap, matches, file))

    page_prefix = '<html>\n<head>\n<meta charset="UTF-8">\n</head>\n<body>\n'
    page_postfix = '\n</body>\n</html>\n'

    out.write(page_prefix)
    if cmdline.server == 'lt':
        out.write(msg_LT_server_html)
    if len(html_report_parts) > 1:
        # start page with file index
        out.write('<H3>Index</H3>\n<ul>\n')
        for r in html_report_parts:
            colour = '" style="color: red' if r[3] else ''
            s = '<li><a href="#' + r[1] + colour + '">' + r[0] + '</a></li>\n'
            out.write(s)
        out.write('</ul>\n<hr><hr>\n')
    for (i, r) in enumerate(html_report_parts):
        if i:
            out.write('<hr><hr>\n')
        out.write(r[2])
    out.write(page_postfix)

#   XXX: these should be passed
#
def init(vars):
    global json_get
    json_get = vars.json_get
    global cmdline
    cmdline = vars.cmdline
    global highlight_style
    highlight_style = vars.highlight_style
    global number_style
    number_style = vars.number_style
    global msg_LT_server_html
    msg_LT_server_html = vars.msg_LT_server_html

