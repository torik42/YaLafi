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

"""
Collection of functions and classes used within yalafi.
"""

import copy
import re
import sys
from yalafi import defs


def latex_error(parser, err, pos):
    r"""
    Print error message to stderr and return error token sequence.

    Args:
        parser: Current parser.
        err: Error message.
        pos: Position where the error occurred in LaTeX source.

    Returns:
        List of tokens suitable to be inserted into the filter output.
    """
    latex = parser.latex
    parms = parser.parms
    lin = latex.count('\n', 0, pos) + 1
    nl = latex.rfind('\n', 0, pos) + 1
    col = pos - nl + 1
    sys.stderr.write('*** LaTeX error: code in ' + repr(parser.source)
                        + ', line ' + str(lin)
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
    """
    Write error to stderr and exit program.
    """
    sys.stderr.write('*** ' + sys.argv[0] + ': internal error:\n*** '
                        + err + '\n')
    sys.exit(1)


def warning(err):
    """
    Write warning to stderr and continue program.
    """
    sys.stderr.write('*** ' + sys.argv[0] + ': warning:\n*** '
                        + err + '\n')
    sys.stderr.flush()


def get_txt_pos(toks):
    """
    Get text and position mapping from list of tokens.

    Returns:
        A tuple ``(txt, pos)`` where ``txt`` is a string representation
        of ``toks``. And ``pos`` is a list of integers, with the same
        length as ``txt``, such that ``txt[n]`` comes from the
        ``pos[n]``-th character in the original LaTeX source.
    """
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
    """
    _summary_

    Args:
        txt: (parsed) string with removed markup.
        pos: List of positions for all characters in ``txt``.
        lines: List of replacements given as strings like ``old & new #
          optional comment``. See ???.

    Returns:
        Modified ``txt`` and ``pos``, where all replacements have been applied.
    """

    for line in lines:
        i = line.find('#')
        if i >= 0:
            line = line[:i]
        line = line.split()

        t = s = ''
        for i, word in enumerate(line):
            if word == '&':
                break
            t += s + re.escape(word)
                    # protect e.g. '.' and '$'
            s = r'(?:[ \t]*\n[ \t]*|[ \t]+)'
                    # at least one space character, but stay in paragraph
        if not t:
            continue
        if t[0].isalpha():
            t = r'\b' + t       # require word boundary
        if t[-1].isalpha():
            t = t + r'\b'

        r = ' '.join(line[i+1:])
        txt, pos = substitute(txt, pos, t, r)
    return txt, pos


def substitute(txt, pos, expr, repl):
    """
    Substitute all occurrences of ``expr`` in ``txt`` and update ``pos``.

    Args:
        txt: (Parsed) string with removed markup.
        pos: List of positions for all characters in ``txt``.
        expr: String to be replaced in ``txt``.
        repl: Replacement for all occurrences of ``expr``.

    Returns:
        A tuple consisting of ``txt``, where all occurrences of ``expr``
        are replaced with ``repl`` and an accordingly updated list of
        positions from ``pos``.
    """
    out_txt = ''
    out_pos = []
    r_len = len(repl)
    last = 0
    for m in re.finditer(expr, txt):
        m_len = len(m.group(0))
        if not m_len:
            continue
        cur = m.start(0)
        out_txt += txt[last:cur] + repl
        out_pos += pos[last:cur]
        if r_len <= m_len:
            out_pos += pos[cur:cur+r_len]
        else:
            out_pos += (pos[cur:cur+m_len]
                        + [pos[cur+m_len-1]] * (r_len - m_len))
        last = m.end(0)
    return out_txt + txt[last:], out_pos + pos[last:]


def get_module_handler(name, prefix):
    """
    Get handler for importing a Python module corresponding to a LaTeX package.

    Replace non-alphanumeric characters except `.` in LaTeX package name
    `name` by `_`. If `name` starts with `.`, remove that dot and try to
    `import name`, i.e. load the Python module from the current python
    path.  If `name` does not starts with `.`, try to `import
    prefix.name`.

    As an example, the `amsmath` LaTeX package included within YaLafi
    will be loaded with `name='amsmath'` and `prefix='yalafi.packages'`
    by `import yalafi.packages.amsmath`.  If `yalafi` is called with
    `--pack .custom`, this function will be called with `name='.custom'`
    and `prefix=''` and YaLafi will try to `import custom`.

    Args:
        name: Name of the LaTeX package. Maybe proceeded by a `.`, see
          above.
        prefix: Name of Python package, from which to load the module
          `name`.

    Returns:
        Tuple `(require_packages, init_module)` loaded from Python
        module `name` if it could be successfully loaded. Otherwise, it
        returns a dummy and prints a warning to stderr.
    """
    name = ''.join((c if c.isalnum() or c == '.' else '_') for c in name)
    if name.startswith('.'):
        mod = name[1:]
    else:
        mod = prefix + '.' + name
    try:
        exec('import ' + mod)
        return (eval(mod + '.require_packages'),
                        eval(mod + '.init_module'))
    except Exception:
        warning('could not load module ' + repr(mod))
        return [], lambda p, o, n: defs.InitModule()


def filter_set_toks(toks, pos, tok_typ):
    """
    Filter tokens based on type and set their position.

    First, if ``tok_type`` is not `None`, ``toks`` is filtered for
    tokens of type ``tok_type``.  Then their positions are set to
    ``pos`` and they are returned.  The returned tokens are actually
    copies such that the original tokens are not modified.

    Args:
        toks: List of tokens.
        pos: The new position written to all returned tokens.
        tok_typ: The class for which to filter ``toks`` or ``None``.

    Returns:
        A list with all tokens from ``toks`` which are of type
        ``tok_typ`` with position set to ``pos``.
    """
    def f(t):
        t = copy.copy(t)
        t.pos = pos
        return t
    return [f(t) for t in toks if tok_typ is None or type(t) is tok_typ]


class LanguageSection:
    """
    Language Section of parsed text.

    Attributes:
        lang: See :attr:`yalafi.defs.LanguageToken.lang`.
        back: See :attr:`yalafi.defs.LanguageToken.back`.
        brk: See :attr:`yalafi.defs.LanguageToken.brk`.
        txt: Text of the section.
        pos: Position list of the section.
          See :func:`yalafi.utils.get_txt_pos`.
    """
    def __init__(self, lang, back, brk, txt, pos):
        self.lang = lang
        self.back = back        # e.g., started by end of \foreignlanguage
        self.brk = brk          # e.g., started by \selectlanguage
        self.txt = txt
        self.pos = pos


def get_txt_pos_ml(toks, main_lang, parms):
    """
    Get text and position mapping from list of tokens split by language.

    The list of tokens is split at :class:`yalafi.defs.LanguageToken`,
    which indicate a language change.  The individual parts are then
    separately handled as in :func:`get_txt_pos`, such that each part
    can be passed to a proofreader separately.

    Args:
        toks: List of tokens
        main_lang: String specifying main language for toks.  See
          :attr:`yalafi.defs.LanguageToken.lang`.  This is the language
          used before any language switching happens.
        parms: :class:`yalafi.parameters.Parameters` object for handling
          current settings.

    Returns:
        Dictionary where the keys correspond to different languages,
        e.g. ``en-GB``, and the values are lists of lists ``[txt, pos]``
        corresponding to the output of :func:`get_txt_pos`.
    """

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


def ml_append_placeholder(sec, incl, parms):
    """
    Append placeholder for “short” language switch to current section.

    Args:
        sec: Current section.
        incl: Section to be included.
        parms: :class:`yalafi.parameters.Parameters` object for handling
          current settings.
    """
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


def ml_check_lang_section(sec, parms):
    """
    Heuristic to determine whether a (short) language section can be
    substituted with a placeholder, so that previous and subsequent
    sections can be glued together

    Args:
        sec: _description_
        parms: :class:`yalafi.parameters.Parameters` object for handling
          current settings.

    Returns:
        `True`, if the language section can be substituted, else
        `False`.
    """
    # accept, if less than 4 words
    return len(sec.txt.split()) <= parms.ml_continue_thresh
