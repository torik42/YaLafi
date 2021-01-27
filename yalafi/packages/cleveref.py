
#
#   YaLafi module for LaTeX package cleveref
#

from yalafi.defs import InitModule, Macro, VoidToken
import re


require_packages = []

re_cref = re.compile(r'\\\\cref\{([^\}\{]+)\}$')
re_Cref = re.compile(r'\\\\Cref\{([^\}\{]+)\}$')
re_command = re.compile(r'''
\\
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
\s*\Z               # possible whitespaces at the end
''', re.VERBOSE)
re_cC = re.compile(r'(\[cC\])')



def init_module(parser, options):
    parms = parser.parms


    macros_latex = r''

    macros_python = [

        Macro(parms, '\\LTReadSed', args='A', repl=h_read_sed),
        Macro(parms, '\\label', args='OA', repl=''),

    ]

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)


def h_read_sed(parser, buf, mac, args, delim, pos):
    if not parser.read_macros:
        return []
    file = parser.get_text_expanded(args[0])
    ok, sed = parser.read_macros(file)
    if not ok:
        return utils.latex_error('could not read file ' + repr(file), pos, parser.latex, parser.parms)

    replacements = []
    for line in sed.split('\n'):
        if line != '':
            replacements.append(line.split('/')[1:3])

    cref = {}
    Cref = {}
    macros = []
    for rep in replacements:
        m = re_cref.match(rep[0])
        if m:
            cref[m.group(1)] = rep[1]
            continue
        m = re_Cref.match(rep[0])
        if m:
            Cref[m.group(1)] = rep[1]
            continue
        m = re_command.match(rep[0])
        if m:
            args = 'A'*int((m.end(3)-m.start(3))/4)
            if m.group(2):
                macros.append(Macro(parser.parms, re_cC.sub('c',m.group(1)), args=args, repl=rep[1]))
                macros.append(Macro(parser.parms, re_cC.sub('C',m.group(1)), args=args, repl=rep[1]))
            else:
                macros.append(Macro(parser.parms, m.group(1), args=args, repl=rep[1]))
    macros.append(Macro(parser.parms, '\\cref', args='A', repl=h_make_cref(cref)))
    macros.append(Macro(parser.parms, '\\Cref', args='A', repl=h_make_cref(Cref)))
    return []


def h_make_cref(cref):
    def f(praser, buf, mac, args, delim, pos):
        rep = parser.get_text_expanded(args[0])
        if rep in cref:
            toks = parser.parms.scanner.scan(cref[rep])
            for t in toks:
                t.pos = pos
            return toks
        return []
    return f
