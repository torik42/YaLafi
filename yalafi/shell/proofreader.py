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
from . import checks
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

##################################################################
#
#   functions for runnning proofreading tool,
#   application of additional rules (e.g., from --equation-punctuation)
#
##################################################################

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
    return run_proofreader_options(tex, file, source_defs,
                        cmdline.language, cmdline.disable, cmdline.enable,
                        cmdline.disablecategories, cmdline.enablecategories,
                        cmdline.lt_options[1:].split())

#   this can be used, if the shell is run as an HTTP server
#   - for that: overwrite CLI options from from fields of HTML request
#
def run_proofreader_options(tex, source, source_defs, language,
                            disable, enable,
                            disablecategories, enablecategories, lt_options):

    t2t_options = tex2txt.Options(char=True, repl=cmdline.replace,
                            defs=cmdline.define, lang=language,
                            extr=cmdline.extract, unkn=cmdline.list_unknown,
                            seqs=cmdline.simple_equations,
                            dcls=cmdline.documentclass, pack=cmdline.packages,
                            nosp=cmdline.no_specials)

    if cmdline.plain_input:
        plain_map = {language: [(tex, list(range(1, len(tex) + 1)))]}
    else:
        if cmdline.list_unknown:
            # only look for unknown macros and environemnts
            plain, charmap = tex2txt.tex2txt(tex, t2t_options, source=source,
                                                source_defs=source_defs)
            return (tex, plain, charmap, [])
        if cmdline.multi_language:
            def mod_parms(parms):
                parms.ml_continue_thresh = cmdline.ml_continue_threshold
            plain_map = tex2txt.tex2txt(tex, t2t_options, multi_language=True,
                                    modify_parms=mod_parms,
                                    source=source, source_defs=source_defs)
        else:
            plain, charmap = tex2txt.tex2txt(tex, t2t_options, source=source,
                                                source_defs=source_defs)
            plain_map = {language: [(plain, charmap)]}

    disa_thresh = disable
    if cmdline.ml_disable:
        if disa_thresh:
            disa_thresh += ','
        disa_thresh += cmdline.ml_disable
    disacat_thresh = disablecategories
    if cmdline.ml_disablecategories:
        if disacat_thresh:
            disacat_thresh += ','
        disacat_thresh += cmdline.ml_disablecategories

    delim = '\n\n'              # NB: issue #6
    matches_tot = []
    plain_tot = ''
    charmap_tot = []
    for lang in plain_map:
        for plain, charmap in plain_map[lang]:
            if not plain.strip():
                continue

            # here, we could dispatch to other tools, see for instance
            #   - https://textgears.com/api
            #   - Python package prowritingaid.python
            #
            if cmdline.textgears:
                matches = run_textgears(plain)
            else:
                flag = (cmdline.multi_language
                        and len(plain.split()) <= cmdline.ml_rule_threshold)
                matches = run_languagetool(plain, lang,
                            disa_thresh if flag else disable,
                            enable,
                            disacat_thresh if flag else disablecategories,
                            enablecategories, lt_options)

            matches += checks.create_single_letter_matches(plain, cmdline)
            matches += checks.create_equation_punct_messages(plain, cmdline,
                                            equation_replacements_display,
                                            equation_replacements_inline,
                                            equation_replacements)

            for m in matches:
                m['offset'] = json_get(m, 'offset', int) + len(plain_tot)
            matches_tot += matches
            plain_tot += plain
            charmap_tot += charmap
            plain_tot += delim
            charmap_tot += [charmap_tot[-1]] * len(delim)

    # sort matches according to position in LaTeX text
    #
    def f(m):
        beg = json_get(m, 'offset', int)
        if beg < 0 or beg >= len(charmap_tot):
            tex2txt.fatal('run_proofreader():'
                            + ' bad message read from proofreader')
        return abs(charmap_tot[beg])
    matches_tot.sort(key=f)

    return (tex, plain_tot, charmap_tot, matches_tot)

#   run LT and return element 'matches' from JSON output
#
def run_languagetool(plain, language, disable, enable,
                            disablecategories, enablecategories, lt_options):
    if cmdline.server:
        # use Web server hosted by LT or local server
        server = ltserver if cmdline.server == 'lt' else ltserver_local
        data = {'text': plain, 'language': language}
        if disable:
            data['disabledRules'] = disable
        if enable:
            data['enabledRules'] = enable
        if disablecategories:
            data['disabledCategories'] = disablecategories
        if enablecategories:
            data['enabledCategories'] = enablecategories
        if lt_options:
            # translate options to entries in HTML request
            ltopts = lt_options
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
        for _ in range(2):
            try:
                reply = urllib.request.urlopen(request)
                out = reply.read()
                reply.close()
                break
            except:
                if cmdline.server != 'my':
                    tex2txt.fatal('error connecting to "' + server + '"')
                start_local_lt_server(language)
    else:
        # use local installation
        lt_cmd = ltcommand.split() + ['--language', language]
        if disable:
            lt_cmd += ['--disable', disable]
        if enable:
            lt_cmd += ['--enable', enable]
        if disablecategories:
            lt_cmd += ['--disablecategories', disablecategories]
        if enablecategories:
            lt_cmd += ['--enablecategories', enablecategories]
        lt_cmd += lt_options
        lt_cmd.append('-')      # read from stdin
        try:
            out = subprocess.run(lt_cmd, cwd=cmdline.lt_directory,
                        input=plain.encode('utf-8'), stdout=subprocess.PIPE)
            out = out.stdout
        except:
            tex2txt.fatal('error running ' + repr(' '.join(lt_cmd))
                            + ' in directory ' + repr(cmdline.lt_directory))

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
def start_local_lt_server(language):
    def check_server():
        # check for running server
        global ltserver_local_running
        if ltserver_local_running:
            return True

        # NB: we need at least one character to check (issue #57)
        data = {'text': ' ', 'language': language}
        data = urllib.parse.urlencode(data).encode(encoding='ascii')
        request = urllib.request.Request(ltserver_local, data=data)
        try:
            reply = urllib.request.urlopen(request)
            reply.close()
            ltserver_local_running = True
            return True
        except urllib.error.HTTPError as e:
            # as we have no real text, this is probably a wrong language code
            tex2txt.fatal('The server couldn\'t fulfill the request;'
                            + ' error code: ' + repr(e.code)
                            + '\n(probably an unknown language code)')
        except:
            return False

    server_cmd = ltserver_local_cmd
    if cmdline.lt_server_options[1:]:
        server_cmd += ' ' + cmdline.lt_server_options[1:]
    if check_server():
        return

    # compare issue #12
    start_new_session = sys.platform != 'win32'
    try:
        subprocess.Popen(server_cmd.split(), cwd=cmdline.lt_directory,
                        start_new_session=start_new_session,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        tex2txt.fatal('error running ' + repr(server_cmd)
                            + ' in directory ' + repr(cmdline.lt_directory))

    # wait for server to be available
    #
    sys.stderr.write('=== starting local LT server at "' + cmdline.lt_directory
                        + '":\n=== ' + server_cmd + ' ')
    sys.stderr.flush()
    for x in range(20):
        time.sleep(0.5)
        sys.stderr.write('.') and sys.stderr.flush()
        if check_server():
            sys.stderr.write('\n') and sys.stderr.flush()
            return
    sys.stderr.write('\n') and sys.stderr.flush()
    tex2txt.fatal('error starting server "' + server_cmd + '"')


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
            'context': checks.create_context(plain, offset, length),
            'replacements': list({'value': r} for r in
                                    json_get(err, 'better', list)),
            'rule': {'id': 'Not available'},
        }
    return list(f(err) for err in json_get(dic, 'errors', list))


#   XXX: these should be passed
#
def init(vars):
    global cmdline
    cmdline = vars.cmdline
    global ltcommand
    ltcommand = vars.ltcommand
    global ltserver
    ltserver = vars.ltserver
    global ltserver_local
    ltserver_local = vars.ltserver_local
    global ltserver_local_cmd
    ltserver_local_cmd = vars.ltserver_local_cmd
    global textgears_server
    textgears_server = vars.textgears_server
    global json_decoder
    json_decoder = vars.json_decoder
    global json_get
    json_get = vars.json_get
    global json_fatal
    json_fatal = vars.json_fatal
    global equation_replacements_display
    equation_replacements_display = vars.equation_replacements_display
    global equation_replacements_inline
    equation_replacements_inline = vars.equation_replacements_inline
    global equation_replacements
    equation_replacements = vars.equation_replacements
    global lt_option_map 
    lt_option_map = vars.lt_option_map 
    global source_defs
    source_defs = vars.source_defs

