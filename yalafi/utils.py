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

from . import defs, parameters
import copy
import re
import sys


#   print error message to stderr,
#   return token sequence suitable to be inserted into filter output
#
def latex_error(err, pos, latex, parms):
    lin = latex.count('\n', 0, pos) + 1
    nl = latex.rfind('\n', 0, pos) + 1
    col = pos - nl + 1
    sys.stderr.write('*** LaTeX error: line ' + str(lin)
                        + ', column ' + str(col) + ':\n*** ' + err + '\n')
    sys.stderr.flush()
    mark = ' ' + parms.mark_latex_error + ' '
    if parms.mark_latex_error_verbose:
        mark += '(' + err + ') '
    mx = min(len(mark), len(latex) - pos)
    out = [defs.TextToken(pos, mark[:mx], pos_fix=True)]
    if mx < len(mark):
        out.append(defs.TextToken(pos + mx -1, mark[mx:], pos_fix=True))
    return out

def fatal(err):
    sys.stderr.write('*** ' + sys.argv[0] + ': internal error:\n*** '
                        + err + '\n')
    sys.exit(1)

def warning(err):
    sys.stderr.write('*** ' + sys.argv[0] + ': warning:\n*** '
                        + err + '\n')
    sys.stderr.flush()

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

#   get handler for importing a module:
#   - replace non-alphanumeric characters (except '.') in LaTeX package name
#     by '_'
#   - if module name starts with '.': remove that dot
#   - else: prepend given prefix
#   return handler, dummy on error
#
def get_module_handler(name, prefix):
    name = ''.join((c if c.isalnum() or c == '.' else '_') for c in name)
    if name.startswith('.'):
        mod = name[1:]
    else:
        mod = prefix + '.' + name
    try:
        exec('import ' + mod)
        return (eval(mod + '.require_packages'),
                        eval(mod + '.init_module'))
    except:
        warning('could not load module ' + repr(mod))
        return [], lambda p, o, n: defs.InitModule()

#   filter out tokens and set their position numbers
#
def filter_set_toks(toks, pos, tok_typ):
    def f(t):
        t = copy.copy(t)
        t.pos = pos
        return t
    return [f(t) for t in toks if tok_typ is None or type(t) is tok_typ]


class LanguageSection:
    def __init__(self, lang, back, brk, txt, pos):
        self.lang = lang
        self.back = back        # e.g., started by end of \foreignlanguage
        self.brk = brk          # e.g., started by \selectlanguage
        self.txt = txt
        self.pos = pos

#   transform a token list into text strings and position lists
#   - seperate into different languages
#   - heuristic: see comments below marked with HEURISTIC
#
def get_txt_pos_ml(toks, main_lang, parms):

    lang_stack = [main_lang]
    switch_back = False
    switch_brk = False

    #   split into sections separated by language switches
    #
    sections = []
    cur_sec = []
    for t in toks:
        if type(t) is not defs.LanguageToken:
            cur_sec.append(t)
            continue
        if t.lang == lang_stack[-1]:
            continue
        txt, pos = get_txt_pos(cur_sec)
        cur_sec = []
        if txt:
            sections.append(LanguageSection(
                        lang_stack[-1], switch_back, switch_brk, txt, pos))
        switch_back = t.back
        switch_brk = t.brk
        if t.back:
            if len(lang_stack) > 1:
                lang_stack.pop()
        else:
            if t.hard:
                lang_stack[-1] = t.lang
            else:
                lang_stack.append(t.lang)
    txt, pos = get_txt_pos(cur_sec)
    if txt:
        sections.append(LanguageSection(
                        lang_stack[-1], switch_back, switch_brk, txt, pos))

    #   try to combine sections, if only interrupted by short change to
    #   another language
    #
    out = []
    while sections:
        if (len(sections) > 1
                    # HEURISTIC to connect sections:
                    # ==============================
                    # - next section does not mandatorily break the text flow
                    #   (e.g., caused by \selectlanguage)
                and not sections[1].brk
                    # - next section must not start with a switch_back
                    #   (e.g., section not after \foreignlanguage call)
                and not sections[1].back
                    # - following section (if any) has to be same language
                and (len(sections) < 3
                            or sections[0].lang == sections[2].lang)
                    # - next section has to be "suitable" to be replaced
                and ml_check_lang_section(sections[1], parms)):

            # we have a short inclusion with another language
            incl = sections.pop(1)
            out.append(incl)
            ml_append_placeholder(sections[0], incl, parms)
            if len(sections) > 1:
                # append following section with same language
                sections[0].txt += sections[1].txt
                sections[0].pos += sections[1].pos
                sections.pop(1)
        else:
            out.append(sections.pop(0))

    #   combine all sections of same language into one list
    #
    ret = {}
    for sec in out:
        if sec.lang in ret:
            ret[sec.lang].append([sec.txt, sec.pos])
        else:
            ret[sec.lang] = [[sec.txt, sec.pos]]
    return ret

#   append placeholder for "short" language switch to current section
#
def ml_append_placeholder(sec, incl, parms):
    if not incl.txt.strip():
        # inclusion is empty or only contains space
        sec.txt += incl.txt
        sec.pos += incl.pos
        return

    lang = parms.check_parser_lang(sec.lang)
    repl = parms.parser_lang_settings[lang].lang_change_repl
    repl[:] = repl [1:] + repl[:1]
    txt = repl[0]

    start = next((n for n in range(len(incl.txt))
                            if not incl.txt[n].isspace()), 0)
    pos = [incl.pos[start]] * len(repl[0])

    # see issue #117
    if incl.txt.strip():
        if incl.txt[0].isspace():
            txt = incl.txt[0] + txt
            pos = [incl.pos[0]] + pos
        if incl.txt[-1].isspace():
            txt += incl.txt[-1]
            pos.append(incl.pos[-1])

    sec.txt += txt
    sec.pos += pos

#   heuristic to determine whether a (short) language section
#   can be substituted with a placeholder, so that previous and
#   subsequent sections can be glued together
#
def ml_check_lang_section(sec, parms):
    # accept, if less than 4 words
    return len(sec.txt.split()) <= parms.ml_continue_thresh

