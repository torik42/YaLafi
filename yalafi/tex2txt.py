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

#
#   YaLafi: emulation of Tex2txt interface,
#   can be directly used by tex2txt/shell.py
#
#   differences:
#   - option '--char' is  always assumed to be set
#   - option '--defs file' reads macro definitions as LaTeX code
#   - option '--pyth module' calls function modify_parameters() from module
#

from . import parameters, parser, utils

def tex2txt(latex, opts):
    def read(file):
        try:
            with open(file, encoding=opts.ienc) as f:
                return True, f.read()
        except:
            return False, ''
    parms = parameters.Parameters(opts.lang)
    if opts.defs:
        parms.add_latex_macros(opts.defs)
    if opts.pyth:
        exec('import ' + opts.pyth)
        exec(opts.pyth + '.modify_parameters(parms)')
    if opts.extr:
        extr = ['\\' + s for s in opts.extr.split(',')]
    else:
        extr = []
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex, extract=extr)
    txt, pos = utils.get_txt_pos(toks)
    if opts.repl:
        txt, pos = utils.replace_phrases(txt, pos, opts.repl)
    if opts.unkn:
        txt = '\n'.join(p.get_unknowns()) + '\n'
        pos = [0 for n in range(len(txt))]
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
def raise_error(kind, msg, detail=None, xit=None):
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
    return lines

#   function for reading definition file
#
def read_definitions(fn, encoding):
    if not fn:
        return ''
    f = myopen(fn, encoding=encoding)
    s = f.read()
    f.close()
    return s

#   class for passing options to tex2txt()
#   LAB:OPTIONS
#
class Options:
    def __init__(self,
            ienc='utf-8',
            repl=None,      # or set by read_replacements()
            char=False,     # True: character position tracking
            defs=None,      # or set by read_definitions()
            pyth=None,      # import module for parameter modification
            extr=None,      # or string: comma-separated macro list
            lang=None,      # or set to language code
            unkn=False):    # True: print unknowns
        self.ienc = ienc
        self.repl = repl
        self.char = char
        self.defs = defs
        if not self.defs:
            # need default defs object
            self.defs = read_definitions(None, '?')
        self.pyth = pyth
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
    parser.add_argument('--pyth')
    parser.add_argument('--extr')
    parser.add_argument('--lang')
    parser.add_argument('--ienc')
    parser.add_argument('--unkn', action='store_true')
    cmdline = parser.parse_args()

    if not cmdline.ienc:
        cmdline.ienc = 'utf-8'

    options = Options(
                ienc=cmdline.ienc,
                repl=read_replacements(cmdline.repl, encoding=cmdline.ienc),
                char=cmdline.char,
                defs=read_definitions(cmdline.defs, encoding=cmdline.ienc),
                pyth=cmdline.pyth,
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

