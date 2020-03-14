#
#   YaLafi: emulation of Tex2txt interface,
#   can be directly used by tex2txt/shell.py
#   - simplified: only option lang is recognised
#

from yalafi import parameters, parser, utils

def tex2txt(latex, opts):
    parms = parameters.Parameters(opts.lang)
    toks = parser.Parser(parms).parse(latex)
    txt, pos = utils.get_txt_pos(toks)
    pos = [n + 1 for n in pos]
    return txt, pos

#########################################################
#
#   the rest is copied from tex2txt/tex2txt.py
#
#########################################################

import argparse
import re
import sys

class Aux:
    pass
def fatal(msg, detail=None):
    raise_error('internal error', msg, detail, xit=1)
def warning(msg, detail=None):
    raise_error('warning', msg, detail)
def myopen(f, encoding, mode='r'):
    try:
        return open(f, mode=mode, encoding=encoding)
    except:
        raise_error('problem', 'could not open file "' + f + '"', xit=1)
warning_or_error = Aux()
warning_or_error.msg = ''
def raise_error(kind, msg, detail=None, xit=None):
    warning_or_error.msg = parms.warning_error_msg
    err = '\n*** ' + sys.argv[0] + ': ' + kind + ':\n' + msg + '\n'
    if detail:
        err += strip_internal_marks(detail) + '\n'
    sys.stderr.write(err)
    if xit is not None:
        sys.exit(xit)
def strip_internal_marks(s):
    # will be redefined below
    return s
def text_get_txt(text):
    return text[0]
def text_get_num(text):
    return text[1]

#   output of text string and line number information
#
def write_output(text, ft, fn):
    if ft:
        ft.write(text_get_txt(text))
    if fn:
        for n in text_get_num(text):
            s = str(abs(n))
            if n < 0:
                s += '+'
            fn.write(s + '\n')

#   function for translation of line and column numbers
#
def translate_numbers(tex, plain, charmap, starts, lin, col):

    if lin < 1 or col < 1:
        return None

    # get start position of line number lin in plain
    if lin > len(starts):
        return None
    n = starts[lin - 1]

    # add column number col
    s = plain[n:]
    i = s.find('\n')
    if i >= 0 and col > i or i < 0 and col > len(s):
        # line is not that long
        return None
    n += col - 1

    # map to character position in tex
    if n >= len(charmap):
        return None
    n = charmap[n]
    if n < 0:
        flag = True
        n = -n
    else:
        flag = False

    # get line and column in tex
    if n > len(tex):
        return None
    s = tex[:n]
    lin = s.count('\n') + 1
    col = len(s) - (s.rfind('\n') + 1)

    r = Aux()
    r.lin = lin
    r.col = max(1, col)
    r.flag = flag
    return r

#   auxiliary function for translation of line and column numbers
#
def get_line_starts(s):
    return list(m.start(0) for m in re.finditer(r'\n', '\n' + s))

#   function for reading replacement file
#
def read_replacements(fn, encoding):
    if not fn:
        return None
    f = myopen(fn, encoding=encoding)
    lines = f.readlines()
    f.close()
    return (lines, fn)

#   function for reading definition file
#
def read_definitions(fn, encoding):
    if not fn:
        return Definitions(None, '?')
    f = myopen(fn, encoding=encoding)
    s = f.read()
    f.close()
    return Definitions(s, fn)

#   class for parsing of file from option --defs
#
class Definitions:
    def __init__(self, code, name):
        self.project_macros = ()
        self.system_macros = ()
        self.heading_macros = ()
        self.environments = ()
        self.equation_environments = ()
        self.environments = ()
        self.environment_begins = ()
        self.theorem_environments = ()
        self.misc_replace = ()
        if code:
            defs = self
            try:
                exec(code)
            except BaseException as e:
                import traceback
                i = 0 if isinstance(e, SyntaxError) else -1
                s = traceback.format_exc(limit=i)
                s = re.sub(r'\ATraceback \(most recent call last\):\n'
                                + r'  File "<string>"(, line \d+).*\n',
                                r'File "' + name + r'"\1\n', s)
                fatal('problem in file "' + name + '"\n' + s)

#   class for passing options to tex2txt()
#   LAB:OPTIONS
#
class Options:
    def __init__(self,
            repl=None,      # or set by read_replacements()
            char=False,     # True: character position tracking
            defs=None,      # or set by read_definitions()
            extr=None,      # or string: comma-separated macro list
            lang=None,      # or set to language code
            unkn=False):    # True: print unknowns
        self.repl = repl
        self.char = char
        self.defs = defs
        if not self.defs:
            # need default defs object
            self.defs = read_definitions(None, '?')
        self.extr = extr
        self.lang = lang
        self.unkn = unkn

#   function to be called for stand-alone script
#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?')
    parser.add_argument('--repl')
    parser.add_argument('--nums')
    parser.add_argument('--char', action='store_true')
    parser.add_argument('--defs')
    parser.add_argument('--extr')
    parser.add_argument('--lang')
    parser.add_argument('--ienc')
    parser.add_argument('--unkn', action='store_true')
    cmdline = parser.parse_args()

    if not cmdline.ienc:
        cmdline.ienc = 'utf-8'

    options = Options(
                repl=read_replacements(cmdline.repl, encoding=cmdline.ienc),
                char=cmdline.char,
                defs=read_definitions(cmdline.defs, encoding='utf-8'),
                                    # the Python code should be UTF-8
                extr=cmdline.extr,
                lang=cmdline.lang,
                unkn=cmdline.unkn)

    if cmdline.file:
        f = myopen(cmdline.file, encoding=cmdline.ienc)
        txt = f.read()
        f.close()
    else:
        # reopen stdin in text mode: handling of '\r', proper decoding
        txt = open(sys.stdin.fileno(), encoding=cmdline.ienc).read()

    if cmdline.nums:
        cmdline.nums = myopen(cmdline.nums, encoding='utf-8', mode='w')

    # ensure UTF-8 output under Windows, too
    sout = open(sys.stdout.fileno(), mode='w', encoding='utf-8')
    text = tex2txt(txt, options)
    write_output(text, sout, cmdline.nums)
    if cmdline.nums:
        cmdline.nums.close()

if __name__ == '__main__':
    # used as stand-alone script
    main()

