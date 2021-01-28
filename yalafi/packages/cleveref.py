
#
#   YaLafi module for LaTeX package cleveref
#

from yalafi.defs import InitModule, Macro, VoidToken
from yalafi import utils
import re
import sys


require_packages = []

re_ref = re.compile(r's/\\(\\cref|\\Cref)\{([^\}\{]+)\}/(.*)/g')
re_ref_range = re.compile(r's/\\(\\crefrange|\\Crefrange)\{([^\}\{]+)\}\{([^\}\{]+)\}/(.*)/g')
re_command = re.compile(r'''
s/\\
(                   # group 1: command
    \\
    (               # group 2: capturing cC
        \[cC\]
    )?
    [a-zA-Z@]+
)
(                   # group 3: possible arguments
    (?:\{\.\*\})+
)?
\s*                 # possible whitespaces inbetween
/
    (.*)            # group 4: replacement
/g
''', re.VERBOSE)
re_cC = re.compile(r'(\[cC\])')
re_dot = re.compile(r'\\\.')
re_double_backslash = re.compile(r'\\\\')

macro_read_sed = '\\LTReadSed'

msg_poorman_option = f'''
*** LaTeX warning:
*** To use cleveref with YaLafi, you need to use the 'poorman' option
*** and {macro_read_sed} to load the .sed file.
'''

msg_sed_not_loaded = f'''To use cleveref with YaLafi, you should use {macro_read_sed} to load
*** the sed file, e.g. '{macro_read_sed}{{main.sed}}' if your LaTeX
*** document is called 'main.tex'.
'''


def init_module(parser, options):
    parms = parser.parms
    parms.newcommand_ignore.append(macro_read_sed)

    macros_latex = r'''
        \newcommand{\crefname}[3]{}
        \newcommand{\Crefname}[3]{}
        \newcommand{\nobreakspace}{~}
    '''

    macros_python = [

        Macro(parms, macro_read_sed, args='A', repl=h_read_sed),
        Macro(parms, '\\label', args='OA', repl=''),
        Macro(parms, '\\cref', args='A', repl=h_cref_warning),
        Macro(parms, '\\Cref', args='A', repl=h_cref_warning),
        Macro(parms, '\\crefrange', args='AA', repl=h_cref_warning),
        Macro(parms, '\\Crefrange', args='AA', repl=h_cref_warning),

    ]

    environments = []

    poorman_warning(options)

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)


def h_read_sed(parser, buf, mac, args, delim, pos):
    if not parser.read_macros:
        return []
    file = parser.get_text_expanded(args[0])
    ok, sed = parser.read_macros(file)
    if not ok:
        return utils.latex_error('could not read file ' + repr(file), pos, parser.latex, parser.parms)

    refs = {'\\cref': {}, '\\Cref': {}, '\\crefrange': {}, '\\Crefrange': {}}
    for rep in sed.split('\n'):
        if rep == '':
            continue
        m = re_ref.match(rep)
        if m:
            refs[m.group(1)][m.group(2)] = re_double_backslash.sub('\\\\', m.group(3))
            continue
        m = re_ref_range.match(rep)
        if m:
            refs[m.group(1)][(m.group(2), m.group(3))] = re_double_backslash.sub('\\\\', m.group(4))
        m = re_command.match(rep)
        if m:
            args = 'A'*int((m.end(3)-m.start(3))/4)
            string = m.group(4)
            string = re_dot.sub('.', string)
            string = re_double_backslash.sub('\\\\', string)
            if m.group(2):
                name = re_cC.sub('c', m.group(1))
                parser.the_macros[name] = Macro(parser.parms, name, args=args, repl=string)
                name = re_cC.sub('C', m.group(1))
                parser.the_macros[name] = Macro(parser.parms, name, args=args, repl=string)
            else:
                name = m.group(1)
                parser.the_macros[name] = Macro(parser.parms, name, args=args, repl=string)
    for ref in ['\\cref','\\Cref']:
        parser.the_macros[ref] = Macro(parser.parms, ref, args='A', repl=h_make_cref(refs[ref]))
    for ref in ['\\crefrange','\\Crefrange']:
        parser.the_macros[ref] = Macro(parser.parms, ref, args='AA', repl=h_make_crefrange(refs[ref]))
    return []


def h_make_cref(cref):
    def f(parser, buf, mac, args, delim, pos):
        rep = parser.get_text_direct(args[0])
        if rep in cref:
            toks = parser.parms.scanner.scan(cref[rep])
            for t in toks:
                t.pos = pos
            return toks
        return utils.latex_error(f'Reference {rep} for command {mac.name} undefined.\n*** Run LaTeX again to build a new .sed file', pos, parser.latex, parser.parms)
    return f


def h_make_crefrange(cref):
    def f(parser, buf, mac, args, delim, pos):
        rep = (parser.get_text_direct(args[0]), parser.get_text_direct(args[1]))
        if rep in cref:
            toks = parser.parms.scanner.scan(cref[rep])
            for t in toks:
                t.pos = pos
            return toks
        return []
    return f


def h_cref_warning(parser, buf, mac, args, delim, pos):
    return utils.latex_error(msg_sed_not_loaded, pos, parser.latex, parser.parms)


def poorman_warning(options):
    for opt in reversed(options):
        if 'poorman' in opt:
            return
    sys.stderr.write(msg_poorman_option)
    return
