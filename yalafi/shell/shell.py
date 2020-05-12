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
config_file = '.yalafi.shell'

# default option values
#
default_option_lt_directory = ltdirectory
default_option_lt_command = ltcommand
default_option_language = 'en-GB'
default_option_encoding = 'utf-8'
default_option_disable = 'WHITESPACE_RULE'
default_option_enable = ''
default_option_disablecategories = ''
default_option_enablecategories = ''
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
import argparse
import json
import signal
from yalafi import tex2txt

# parse command line
#
parser = argparse.ArgumentParser()
parser.add_argument('--lt-directory', default=default_option_lt_directory)
parser.add_argument('--lt-command', default=default_option_lt_command)
parser.add_argument('--as-server', type=int)
parser.add_argument('--output', default='plain',
                        choices=['plain', 'html', 'xml', 'xml-b', 'json'])
parser.add_argument('--link', action='store_true')
parser.add_argument('--context', default=default_option_context, type=int)
parser.add_argument('--include', action='store_true')
parser.add_argument('--skip')
parser.add_argument('--plain-input', action='store_true')
parser.add_argument('--list-unknown', action='store_true')
parser.add_argument('--language', default=default_option_language)
parser.add_argument('--encoding', default=default_option_encoding)
parser.add_argument('--replace')
parser.add_argument('--define')
parser.add_argument('--python-defs')
parser.add_argument('--extract')
parser.add_argument('--disable', default=default_option_disable)
parser.add_argument('--enable', default=default_option_enable)
parser.add_argument('--disablecategories',
                        default=default_option_disablecategories)
parser.add_argument('--enablecategories',
                        default=default_option_enablecategories)
parser.add_argument('--lt-options', default='')
parser.add_argument('--single-letters')
parser.add_argument('--equation-punctuation')
parser.add_argument('--server', choices=['my', 'lt', 'stop'], default='')
parser.add_argument('--lt-server-options', default='')
parser.add_argument('--textgears')
parser.add_argument('--no-config', action='store_true')
parser.add_argument('file', nargs='*')

cmdline = parser.parse_args(sys.argv[1:])
if not cmdline.no_config:
    # try to read config file
    try:
        f = open(config_file)
        config = f.read().splitlines()
        f.close()
        # split a line only once --> option argument may contain space
        config = sum((lin.strip().split(maxsplit=1) for lin in config), [])
    except:
        config = []
    cmdline = parser.parse_args(config + sys.argv[1:])

ltcommand = cmdline.lt_command + ' --json --encoding utf-8'
if cmdline.context < 0:
    # huge context: display whole text
    cmdline.context = int(1e8)
if not (cmdline.file or cmdline.as_server or cmdline.server == 'stop'):
    tex2txt.fatal('no input file given')
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


# on option --include: add included files to work list
# otherwise: remove duplicates
#
if cmdline.include:
    sys.stderr.write('=== checking for file inclusions ... ')
    sys.stderr.flush()
    opts = tex2txt.Options(extr=inclusion_macros, repl=cmdline.replace,
                            defs=cmdline.define, lang=cmdline.language[:2],
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

# hack for passing of globals
#
vars = tex2txt.Aux()
vars.cmdline = cmdline
vars.ltcommand = ltcommand
vars.ltserver = ltserver
vars.ltserver_local = ltserver_local
vars.ltserver_local_cmd = ltserver_local_cmd
vars.textgears_server = textgears_server
vars.json_decoder = json_decoder
vars.json_get = json_get
vars.json_fatal = json_fatal
vars.equation_replacements_display = equation_replacements_display
vars.equation_replacements_inline = equation_replacements_inline
vars.equation_replacements = equation_replacements
vars.msg_LT_server_txt = msg_LT_server_txt 
vars.msg_LT_server_html = msg_LT_server_html 
vars.highlight_style = highlight_style 
vars.number_style = number_style 
vars.lt_option_map = lt_option_map 

# import functions for calling proofreader
#
from yalafi.shell import proofreader
proofreader.init(vars)

# run as server
#
if cmdline.as_server is not None:
    from yalafi.shell import server
    server.run_server('localhost', cmdline.as_server,
                        proofreader.run_proofreader_options,
                        lt_option_map, cmdline.lt_options[1:].split())
    sys.exit()

# generate reports
# - ensure UTF-8 encoding for output (not standard with Windows Python)
#
out_utf8 = open(sys.stdout.fileno(), mode='w', encoding='utf-8')

if cmdline.output == 'plain' or cmdline.list_unknown:
    from yalafi.shell import gentext
    gentext.init(vars)
    # do not enforce UTF-8: we might be working in a Windows command console
    gentext.generate_text_report(proofreader.run_proofreader, sys.stdout)
elif cmdline.output in ('xml', 'xml-b'):
    from yalafi.shell import genxml
    genxml.init(vars)
    genxml.generate_xml_report(proofreader.run_proofreader, out_utf8,
                                            cmdline.output == 'xml-b')
elif cmdline.output == 'html':
    from yalafi.shell import genhtml
    genhtml.init(vars)
    genhtml.generate_html_report(proofreader.run_proofreader, out_utf8)
elif cmdline.output == 'json':
    from yalafi.shell import genjson
    genjson.generate_json_report(cmdline, proofreader.run_proofreader,
                                            json_get, out_utf8)

