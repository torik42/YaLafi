#
#   Tex2txt, a flexible LaTeX filter
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

#
#   Python3:
#   application of tex2txt as module,
#   use LanguageTool to create a proofreading report in text or HTML format
#
#   Usage: see README.md
#
#   CREDITS for mode of HTML report:
#   This idea goes back to Sylvain Hallé who developed TeXtidote.
#

# path of LT java archive
# - zip file can be obtained from from www.languagetool.org/download,
#   and be unzipped with 'unzip xxx.zip'
# - Java has to be installed,
#   under Cygwin the Windows version is used
#
ltdirectory = '../LT/LanguageTool-4.7/'
ltcommand = 'java -jar languagetool-commandline.jar'

# on option --server lt: address of server hosted by LT
#
ltserver = 'https://languagetool.org/api/v2/check'

# on option --server my: use local LT server
#
ltserver_local = 'http://localhost:8081/v2/check'
ltserver_local_cmd = ('java -cp'
            + ' languagetool-server.jar org.languagetool.server.HTTPServer'
            + ' --port 8081')

# config file
#
config_file = '.t2t-shell'

# default option values
#
default_option_lt_directory = ltdirectory
default_option_language = 'en-GB'
default_option_encoding = 'utf-8'
default_option_disable = 'WHITESPACE_RULE'
default_option_context = 2

# option --include: inclusion macros
#
inclusion_macros = 'include,input'

# equation replacements used for option --equation-punctuation
# - have to start and end with a letter for proper operation
# - also used by option --single-letters
#
equation_replacements_display = r'U-U-U|V-V-V|W-W-W|X-X-X|Y-Y-Y|Z-Z-Z'
equation_replacements_inline = r'B-B-B|C-C-C|D-D-D|E-E-E|F-F-F|G-G-G'
equation_replacements = (equation_replacements_display
                            + r'|' + equation_replacements_inline)

# option --textgears
#
textgears_server = 'https://api.textgears.com/check.php'

# HTML: properties of <span> tag for highlighting
#
highlight_style = 'background: orange; border: solid thin black'
highlight_style_unsure = 'background: yellow; border: solid thin black'

# HTML: style for display of line numbers
#
number_style = 'color: grey'

# messages on usage of server hosted by LT
#
msg_LT_server_txt = '''===
=== Using LanguageTool server at https://languagetool.org/
=== For conditions and restrictions, refer to
===     http://wiki.languagetool.org/public-http-api
===
'''
msg_LT_server_html = '''
<H2>Using LanguageTool server at
<a href="https://languagetool.org/" target="_blank">
https://languagetool.org/</a></H2>
For conditions and restrictions, refer to
<a href="http://wiki.languagetool.org/public-http-api" target="_blank">
http://wiki.languagetool.org/public-http-api</a>
<hr><hr>
'''


#####################################################################
#
#   implementation
#
#####################################################################

import os
import re
import sys
import subprocess
# import tex2txt
from yalafi import tex2txt
import argparse
import json
import urllib.parse
import urllib.request
import time
import signal
import xml.etree.ElementTree as ET

# parse command line
#
parser = argparse.ArgumentParser()
parser.add_argument('--lt-directory', default=default_option_lt_directory)
parser.add_argument('--output', choices=['plain', 'html', 'xml'],
                                                    default='plain')
parser.add_argument('--link', action='store_true')
parser.add_argument('--context', type=int)
parser.add_argument('--include', action='store_true')
parser.add_argument('--skip')
parser.add_argument('--plain-input', action='store_true')
parser.add_argument('--list-unknown', action='store_true')
parser.add_argument('--language')
parser.add_argument('--t2t-lang')
parser.add_argument('--encoding')
parser.add_argument('--replace')
parser.add_argument('--define')
parser.add_argument('--python-defs')
parser.add_argument('--extract')
parser.add_argument('--disable')
parser.add_argument('--lt-options')
parser.add_argument('--single-letters')
parser.add_argument('--equation-punctuation')
parser.add_argument('--server')
parser.add_argument('--lt-server-options')
parser.add_argument('--textgears')
parser.add_argument('file', nargs='+')

try:
    f = open(config_file)
    config = f.read().splitlines()
    f.close()
    # split a line only once --> option argument may contain space
    config = sum((lin.strip().split(maxsplit=1) for lin in config), [])
except:
    config = []
cmdline = parser.parse_args(config + sys.argv[1:])

if cmdline.language is None:
    cmdline.language = default_option_language
if cmdline.t2t_lang is None:
    cmdline.t2t_lang = cmdline.language[:2]
if cmdline.encoding is None:
    cmdline.encoding = default_option_encoding
if cmdline.disable is None:
    cmdline.disable = default_option_disable
if cmdline.context is None:
    cmdline.context = default_option_context
if cmdline.context < 0:
    # huge context: display whole text
    cmdline.context = int(1e8)
if cmdline.server is not None and cmdline.server not in ('lt', 'my', 'stop'):
    tex2txt.fatal('mode for --server has to be one of lt, my, stop')
if cmdline.plain_input and (cmdline.include or cmdline.replace):
    tex2txt.fatal('cannot handle --plain-input together with'
                                        + ' --include or --replace')
if cmdline.single_letters and cmdline.single_letters.endswith('||'):
    cmdline.single_letters += equation_replacements
if cmdline.replace:
    cmdline.replace = tex2txt.read_replacements(cmdline.replace,
                                                encoding=cmdline.encoding)
if cmdline.define:
    cmdline.define = tex2txt.read_definitions(cmdline.define,
                                                encoding=cmdline.encoding)

# only stop local LT server?
#
if cmdline.server == 'stop':
    done = False
    try:
        for pid in [s for s in os.listdir('/proc') if s.isdecimal()]:
            with open('/proc/' + pid + '/cmdline') as f:
                args = ' '.join(f.read().split('\000')[1:])
            # for Cygwin with Window's Java: do not check image name
            if ' '.join(ltserver_local_cmd.split()[1:]) not in args:
                continue
            os.kill(int(pid), signal.SIGINT)
            done = True
            break
    except:
        pass
    if done:
        sys.stderr.write('=== done: killed local LT server "'
                                    + ltserver_local_cmd + '"\n')
        sys.exit()
    tex2txt.fatal('could not kill LT server "' + ltserver_local_cmd + '"')

# complement LT options
#
ltcommand = ltcommand.split() + ['--json', '--encoding', 'utf-8',
                            '--language', cmdline.language]
if cmdline.disable:
    ltcommand += ['--disable', cmdline.disable]
if cmdline.lt_options:
    ltcommand += cmdline.lt_options[1:].split()
ltcommand += ['-']
if cmdline.lt_server_options:
    ltserver_local_cmd += ' ' + cmdline.lt_server_options[1:]

# on option --include: add included files to work list
# otherwise: remove duplicates
#
if cmdline.include:
    sys.stderr.write('=== checking for file inclusions ... ')
    sys.stderr.flush()
    opts = tex2txt.Options(extr=inclusion_macros, repl=cmdline.replace,
                            defs=cmdline.define, lang=cmdline.t2t_lang,
                            pyth=cmdline.python_defs)

def skip_file(fn):
    # does file name match regex from option --skip?
    return cmdline.skip and re.search(r'\A' + cmdline.skip + r'\Z', fn)

todo = cmdline.file
done = []
while todo:
    f = todo.pop(0)
    if f in done or skip_file(f):
        continue
    done.append(f)
    if not cmdline.include:
        continue
    fp = tex2txt.myopen(f, encoding=cmdline.encoding)
    tex = fp.read()
    fp.close()
    (plain, _) = tex2txt.tex2txt(tex, opts)
    for f in plain.split():
        if not f.endswith('.tex'):
            f += '.tex'
        if f not in done + todo and not skip_file(f):
            todo.append(f)

cmdline.file = done
if cmdline.include:
    sys.stderr.write(', '.join(cmdline.file) + '\n')
    sys.stderr.flush()

# prepare options for tex2txt()
#
options = tex2txt.Options(char=True, repl=cmdline.replace,
                            defs=cmdline.define, lang=cmdline.t2t_lang,
                            extr=cmdline.extract, unkn=cmdline.list_unknown,
                            pyth=cmdline.python_defs)

# helpers for robust JSON evaluation
#
json_decoder = json.JSONDecoder()

def json_fatal(item):
    tex2txt.fatal('error reading JSON output from proofreader, (sub-)item "'
                    + item + '"')
def json_get(dic, item, typ):
    if not isinstance(dic, dict):
        json_fatal(item)
    ret = dic.get(item)
    if not isinstance(ret, typ):
        json_fatal(item)
    return ret

#   for given file:
#   - print progress message to stderr
#   - read file
#   - extract plain text
#   - call proofreading program
#
def run_proofreader(file):

    sys.stderr.write('=== ' + file + '\n')
    sys.stderr.flush()
    f = tex2txt.myopen(file, encoding=cmdline.encoding)
    tex = f.read()
    f.close()
    if not tex.endswith('\n'):
        tex += '\n'

    if cmdline.plain_input:
        (plain, charmap) = (tex, list(range(1, len(tex) + 1)))
    else:
        (plain, charmap) = tex2txt.tex2txt(tex, options)
        if cmdline.list_unknown:
            # only look for unknown macros and environemnts
            return (tex, plain, charmap, [])

    # see yalafi Issue #6
    #
    if not plain.endswith('\n'):
        plain += '\n'
        charmap.append(charmap[-1] if charmap else 1)

    # here, we could dispatch to other tools, see for instance
    #   - https://textgears.com/api
    #   - Python package prowritingaid.python
    #
    if cmdline.textgears:
        matches = run_textgears(plain)
    else:
        matches = run_languagetool(plain)

    matches += create_single_letter_matches(plain)
    matches += create_equation_punct_messages(plain)

    # sort matches according to position in LaTeX text
    #
    def f(m):
        beg = json_get(m, 'offset', int)
        if beg < 0 or beg >= len(charmap):
            tex2txt.fatal('run_proofreader():'
                            + ' bad message read from proofreader')
        return abs(charmap[beg])
    matches.sort(key=f)

    return (tex, plain, charmap, matches)

#   translation between CLI option names and HTML request fields,
#   see package pyLanguagetool for field names
#
lt_option_map = {
    # (HTML request field): ([list of CLI option names], # of arguments)
    'language': (['--language', '-l'], 1),
    'disabledRules': (['--disable', '-d'], 1),
    'enabledRules': (['--enable', '-e'], 1),
    'enabledOnly': (['--enabledonly', '-eo'], 0),
    'disabledCategories': (['--disablecategories'], 1),
    'enabledCategories': (['--enablecategories'], 1),
}

#   run LT and return element 'matches' from JSON output
#
def run_languagetool(plain):
    if cmdline.server:
        # use Web server hosted by LT or local server
        if cmdline.server == 'lt':
            server = ltserver
        else:
            start_local_lt_server()
            server = ltserver_local
        data = {'text': plain, 'language': cmdline.language}
        if cmdline.disable:
            data['disabledRules'] = cmdline.disable
        if cmdline.lt_options:
            # translate options to entries in HTML request
            ltopts = cmdline.lt_options[1:].split()
            for opt in lt_option_map:
                entry = lt_option_map[opt]
                if not any(s in ltopts for s in entry[0]):
                    continue
                idx = max(ltopts.index(s) for s in entry[0] if s in ltopts)
                if entry[1]:
                    data[opt] = ltopts[idx+1] if idx + 1 < len(ltopts) else ''
                else:
                    data[opt] = 'true'

        data = urllib.parse.urlencode(data).encode(encoding='ascii')
        request = urllib.request.Request(server, data=data)
        try:
            reply = urllib.request.urlopen(request)
            out = reply.read()
            reply.close()
        except:
            tex2txt.fatal('error connecting to "' + server + '"')
    else:
        # use local installation
        try:
            out = subprocess.run(ltcommand, cwd=cmdline.lt_directory,
                        input=plain.encode('utf-8'), stdout=subprocess.PIPE)
            out = out.stdout
        except:
            tex2txt.fatal('error running "' + ltcommand[0] + '"')

    out = out.decode(encoding='utf-8')
    try:
        dic = json_decoder.decode(out)
    except:
        json_fatal('JSON root element')
    matches = json_get(dic, 'matches', list)
    return matches

#   start local LT server, if none is running
#
ltserver_local_running = False
def start_local_lt_server():
    def check_server():
        # check for running server
        global ltserver_local_running
        if ltserver_local_running:
            return True

        data = {'text': '', 'language': 'en'}
        data = urllib.parse.urlencode(data).encode(encoding='ascii')
        request = urllib.request.Request(ltserver_local, data=data)
        try:
            reply = urllib.request.urlopen(request)
            reply.close()
            ltserver_local_running = True
            return True
        except:
            return False

    if check_server():
        return
    try:
        subprocess.Popen(ltserver_local_cmd.split(), cwd=cmdline.lt_directory,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        tex2txt.fatal('error running "' + ltserver_local_cmd + '"')

    # wait for server to be available
    #
    sys.stderr.write('=== starting local LT server at "' + cmdline.lt_directory
                        + '":\n=== ' + ltserver_local_cmd + ' ')
    sys.stderr.flush()
    for x in range(20):
        time.sleep(0.5)
        sys.stderr.write('.') and sys.stderr.flush()
        if check_server():
            sys.stderr.write('\n') and sys.stderr.flush()
            return
    sys.stderr.write('\n')
    tex2txt.fatal('error starting server "' + ltserver_local_cmd + '"')


#   contact TextGears server, translate JSON output to our format
#
def run_textgears(plain):
    data = {
        'key': cmdline.textgears,
        'text': plain,
    }
    data = urllib.parse.urlencode(data).encode(encoding='ascii')
    request = urllib.request.Request(textgears_server, data=data)
    try:
        reply = urllib.request.urlopen(request)
        out = reply.read()
        reply.close()
    except:
        tex2txt.fatal('error connecting to "' + textgears_server + '"')

    out = out.decode(encoding='utf-8')
    try:
        dic = json_decoder.decode(out)
    except:
        json_fatal('JSON root element')

    def f(err):
        offset = json_get(err, 'offset', int)
        length = json_get(err, 'length', int)
        return {
            'message': 'Error type: ' + json_get(err, 'type', str),
            'offset': offset,
            'length': length,
            'context': create_context(plain, offset, length),
            'replacements': list({'value': r} for r in
                                    json_get(err, 'better', list)),
            'rule': {'id': 'Not available'},
        }
    return list(f(err) for err in json_get(dic, 'errors', list))

#   create error messages for single letters
#
def create_single_letter_matches(plain):
    if cmdline.single_letters is None:
        # option not given: do not check
        return []

    #   some processing of the accepted patterns given in the option
    #
    accept = cmdline.single_letters.split('|')
    def f(s):
        # - replace '~' and '\\,' with UTF-8 (narrow) non-breaking space
        # - escape the rest, for instance dots '.'
        # - add word boundaries if appropriate
        #
        s = s.replace('~', '\N{NO-BREAK SPACE}')
        s = s.replace('\\,', '\N{NARROW NO-BREAK SPACE}')
        s = re.escape(s)
        if s[0].isalpha():
            s = r'\b' + s
        if s[-1].isalpha():
            s = s + r'\b'
        return r'(' + s + r')'
    accept = r'|'.join(f(s) for s in accept if s)

    #   a list of all occurences of accepted patterns
    #
    if accept:
        hits = list((m.start(0), m.end(0))
                        for m in re.finditer(accept, plain))
    else:
        hits = []

    def msg(m):
        return create_message(m, rule='PRIVATE::SINGLE_LETTER',
                    msg='Single letter detected.', repl='—')
    def f(m):
        #   return True if match of single letter occurs inside of
        #   a place in list 'hits'
        #
        for (beg, end) in hits:
            if beg <= m.start(0) < end:
                return True
        return False
    single = r'\b[^\W0-9_]\b'
    return list(msg(m) for m in re.finditer(single, plain) if not f(m))

#   create error messages for problem with equation punctuation
#
def create_equation_punct_messages(plain):
    if cmdline.equation_punctuation is None:
        return []

    mode = {
        'displayed': equation_replacements_display,
        'inline': equation_replacements_inline,
        'all': equation_replacements,
    }
    k = list(k for k in mode.keys()
                        if k.startswith(cmdline.equation_punctuation))
    if len(k) != 1:
        tex2txt.fatal('mode for --equation-punctuation has to determine'
                        + ' one of ' + ', '.join(mode.keys()))
    repls = mode[k[0]]

    def msg(m):
        return create_message(m, rule='PRIVATE::EQUATION_PUNCTUATION',
                    msg='Possibly incorrect punctuation after equation.',
                    repl='—')
    def f(m):
        #   return True if equation is followed by
        #   - another equation (possibly after punctuation in punct)
        #   - a dot
        #   - a lower-case word (possibly after punctuation in punct)
        #
        groups = m.groups()
        equ = groups[0]     # another equation follows: not consumed!
        dot = groups[-2]    # a dot follows
        word = groups[-1]   # a word follows
        return equ or dot or word and word[0].islower()
    punct = ',;:'
    equ = r'\b(?:' + repls + r')\b'
    expr = (r'(' + equ + r'(?=\s*[' + punct + r']?\s*' + equ + r'))|'
                + equ + r'\s*(?:(\.)|[' + punct + r']?\s*([^\W0-9_]+))?')
    return list(msg(m) for m in re.finditer(expr, plain) if not f(m))

def create_context(txt, offset, length):
    context_size = 45
    beg = max(offset - context_size, 0)
    end = min(offset + context_size, len(txt))
    s = txt[beg:end].replace('\t', ' ').replace('\n', ' ')
    return  {
        'text': '...' + s + '...',
        'offset': offset - beg + 3,
        'length': length,
    }

#   construct message element for a match from re.finditer()
#
def create_message(m, rule, msg, repl):
    offset = m.start(0)
    length = len(m.group(0))
    return {
        'offset': offset,
        'length': length,
        'context': create_context(m.string, offset, length),
        'rule': {'id': rule, 'category': {'name': 'Problem'}},
        'message': msg,
        'replacements': [{'value': repl}],
    }


#####################################################################
#
#   text report
#
#####################################################################

#   generate text report from element 'matches' of JSON output
#
#   - compare printMatches() in file CommandLineTools.java in directory
#     languagetool-commandline/src/main/java/org/languagetool/commandline/
#   - XXX: some code duplication with begin_match()
#
def output_text_report(tex, plain, charmap, matches, file):
    starts = tex2txt.get_line_starts(plain)

    for (nr, m) in enumerate(matches, 1):
        offset = json_get(m, 'offset', int)
        lin = plain.count('\n', 0, offset) + 1
        nl = plain.rfind('\n', 0, offset) + 1
        col = offset - nl + 1
        lc = tex2txt.translate_numbers(tex, plain, charmap, starts, lin, col)

        rule = json_get(m, 'rule', dict)
        print('=== ' + file + ' ===')

        s = (str(nr) + '.) Line ' + str(lc.lin) + ', column ' + str(lc.col)
                + ', Rule ID: ' + json_get(rule, 'id', str))
        if 'subId' in rule:
                s += '[' + json_get(rule, 'subId', str) + ']'
        print(s)
        print('Message: ' + json_get(m, 'message', str))

        repls = '; '.join(json_get(r, 'value', str)
                                for r in json_get(m, 'replacements', list))
        print('Suggestion: ' + repls)

        cont = json_get(m, 'context', dict)
        txt = json_get(cont, 'text', str)
        beg = json_get(cont, 'offset', int)
        length = json_get(cont, 'length', int)
        print(txt.replace('\t', ' '))
        print(' ' * beg + '^' * length)

        if 'urls' in rule:
            urls = json_get(rule, 'urls', list)
            if urls:
                print('More info: ' + json_get(urls[0], 'value', str))

        print('')

    sys.stdout.flush()  # in case redirected to file


#   on option --list-unknown
#
def output_list_unknown(unkn, file):
    if not unkn.split():
        return
    print('=== ' + file + ' ===')
    print(unkn)


if cmdline.output == 'plain' or cmdline.list_unknown:
    if cmdline.server == 'lt':
        sys.stderr.write(msg_LT_server_txt)
    for file in cmdline.file:
        (tex, plain, charmap, matches) = run_proofreader(file)
        if cmdline.list_unknown:
            output_list_unknown(plain, file)
        else:
            output_text_report(tex, plain, charmap, matches, file)
    sys.exit()


#####################################################################
#
#   XML report for vim-grammarous
#
#####################################################################

#   - XXX: some code duplication with begin_match()
#
def output_xml_report(tex, plain, charmap, matches, file, out):
    starts = tex2txt.get_line_starts(plain)
    out.write('<matches>\n')
    for m in matches:
        offset = json_get(m, 'offset', int)
        lin = plain.count('\n', 0, offset) + 1
        nl = plain.rfind('\n', 0, offset) + 1
        col = offset - nl + 1
        lc = tex2txt.translate_numbers(tex, plain, charmap, starts, lin, col)
        fromy = lc.lin - 1
        fromx = lc.col - 1

        length = json_get(m, 'length', int)
        end = offset + length - 1
        lin = plain.count('\n', 0, end) + 1
        nl = plain.rfind('\n', 0, end) + 1
        col = end - nl + 1
        lc = tex2txt.translate_numbers(tex, plain, charmap, starts, lin, col)
        toy = lc.lin - 1
        tox = lc.col

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


if cmdline.output == 'xml':
    if cmdline.server == 'lt':
        sys.stderr.write(msg_LT_server_txt)
    out = open(sys.stdout.fileno(), mode='w', encoding='utf-8')
    for file in cmdline.file:
        (tex, plain, charmap, matches) = run_proofreader(file)
        output_xml_report(tex, plain, charmap, matches, file, out)
    sys.exit()


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

        if (h.end == h.beg + 1 and tex[h.beg] == '\\'
                and re.search(r'(?<!\\)(\\\\)*\Z', tex[:h.beg])):
            # HACK:
            # if matched a single \ that is actually followed by macro name:
            # also highlight the macro name
            s = re.search(r'\A\\[a-zA-Z]+', tex[h.beg:])
            if s:
                h.end = h.beg + len(s.group(0))
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


#   generate HTML report: a part for each file
#
html_report_parts = []
for file in cmdline.file:
    (tex, plain, charmap, matches) = run_proofreader(file)
    html_report_parts.append(generate_html(tex, charmap, matches, file))

#   ensure UTF-8 encoding for stdout
#   (not standard with Windows Python)
#
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8')

page_prefix = '<html>\n<head>\n<meta charset="UTF-8">\n</head>\n<body>\n'
page_postfix = '\n</body>\n</html>\n'

sys.stdout.write(page_prefix)
if cmdline.server == 'lt':
    sys.stdout.write(msg_LT_server_html)
if len(html_report_parts) > 1:
    # start page with file index
    sys.stdout.write('<H3>Index</H3>\n<ul>\n')
    for r in html_report_parts:
        colour = '" style="color: red' if r[3] else ''
        s = '<li><a href="#' + r[1] + colour + '">' + r[0] + '</a></li>\n'
        sys.stdout.write(s)
    sys.stdout.write('</ul>\n<hr><hr>\n')
for (i, r) in enumerate(html_report_parts):
    if i:
        sys.stdout.write('<hr><hr>\n')
    sys.stdout.write(r[2])
sys.stdout.write(page_postfix)

