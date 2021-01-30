
#
#   YaLafi module for LaTeX package cleveref
#   Contributed by @torik42 (at GitHub) in pull request #171
#

from yalafi.defs import InitModule, Macro, VoidToken
from yalafi import utils
import re


require_packages = []

macro_read_sed = '\\YYCleverefInput'

# Regular Expressions used to read sed file:
re_ref = re.compile(r'''
s/\\
(                   # group 1: '\cref' or '\Cref'
    \\cref|\\Cref
)
(?:\\)?             # non capturing group
(\*?)               # group 2: '*' if present, '' else
\{
    ([^\}\{]+)      # group 3: the label of the reference
\}
/
    (.*)            # group 4: the replacement string
/g
''', re.VERBOSE)
re_ref_range = re.compile(r'''
s/\\
(                   # group 1: '\cref' or '\Cref'
    \\crefrange|\\Crefrange
)
(?:\\)?             # non capturing group
(\*?)               # group 2: '*' if present, '' else
\{
    ([^\}\{]+)      # group 3: the label of the first reference
\}
\{
    ([^\}\{]+)      # group 4: the label of the second reference
\}
/
    (.*)            # group 5: the replacement string
/g
''', re.VERBOSE)
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
re_escaped_dot = re.compile(r'\\\.')
re_escaped_backslash = re.compile(r'\\\\')
re_escaped_star = re.compile(r'\\\*')


def re_remove_escaped_symbols(string):
    r"""
    Replaces certain strings that are escaped in sed file:
    '\\.' -> '.'
    '\\\\' -> '\\'
    '\*' -> ''
    """
    string = re_escaped_dot.sub('.', string)
    string = re_escaped_star.sub('', string)
    string = re_escaped_backslash.sub(r'\\', string)
    return string


# Error messages
msg_poorman_option = f'''To use cleveref with YaLafi, you need to use
*** the 'poorman' option and {macro_read_sed}
*** to load the sed file.
'''
msg_sed_not_loaded = f'''To use cleveref with YaLafi, you should use
*** {macro_read_sed} to load the sed file, e.g.
*** '{macro_read_sed}{{main.sed}}' if your LaTeX
*** document is called 'main.tex'.
'''

msg_cref_undefined = r'''No replacement for {:}{{{:}}} known.
*** Run LaTeX again to build a new sed file.
'''
msg_crefrange_undefined = r'''No replacement for {:}{{{:}}}{{{:}}} known.
*** Run LaTeX again to build a new sed file.
'''


def init_module(parser, options, position):
    parms = parser.parms
    parms.newcommand_ignore.append(macro_read_sed)

    macros_latex = r'''
        \newcommand{\crefname}[3]{}
        \newcommand{\Crefname}[3]{}
    '''

    macros_python = [

        Macro(parms, macro_read_sed, args='A', repl=h_read_sed),
        Macro(parms, '\\label', args='OA', repl=''),

        # Define functions which warn the User, whenever cleveref
        # is used without invoking \YYCleverefInput. These will be overwritten
        # by invoking \YYCleverefInput.
        Macro(parms, '\\cref', args='*A', repl=h_cref_warning),
        Macro(parms, '\\Cref', args='*A', repl=h_cref_warning),
        Macro(parms, '\\crefrange', args='*AA', repl=h_cref_warning),
        Macro(parms, '\\Crefrange', args='*AA', repl=h_cref_warning),

    ]

    environments = []

    # Warn the user, whenever cleveref is used
    # without the poorman option:
    inject_tokens = []
    if not is_poorman_used(options):
        inject_tokens = utils.latex_error(msg_poorman_option,
                                          position, parser.latex, parms)

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                      environments=environments, inject_tokens=inject_tokens)


def h_read_sed(parser, buf, mac, args, delim, pos):
    if not parser.read_macros:
        return []

    # Read sed file into sed:
    file = parser.get_text_expanded(args[0])
    ok, sed = parser.read_macros(file)

    # Throw LaTeX error if the file could not be loaded:
    if not ok:
        return utils.latex_error('could not read file ' + repr(file),
                                 pos, parser.latex, parser.parms)

    refs = {'\\cref': {'':{}, '*': {}},
            '\\Cref': {'':{}, '*': {}},
            '\\crefrange': {'':{}, '*': {}},
            '\\Crefrange': {'':{}, '*': {}}}

    for rep in sed.split('\n'):
        # only consider non-empty lines:
        if rep == '':
            continue

        # Match \cref,\cref*,\Cref and \Cref* and save the replacement string:
        m = re_ref.match(rep)
        if m:
            refs[m.group(1)][m.group(2)][m.group(3)] \
                = re_remove_escaped_symbols(m.group(4))
            continue

        # Match \crefrange, \crefrange*, \Crefrange and \Crefrange* and
        # save the replacement string:
        m = re_ref_range.match(rep)
        if m:
            refs[m.group(1)][m.group(2)][(m.group(3), m.group(4))] \
                = re_remove_escaped_symbols(m.group(5))

        # Match any other command and create Macro objects for them.
        # See definition of re_command for more details:
        m = re_command.match(rep)
        if m:
            args = 'A'*int((m.end(3)-m.start(3))/4)
            string = re_remove_escaped_symbols(m.group(4))
            if m.group(2):
                name = re_cC.sub('c', m.group(1))
                parser.the_macros[name] = Macro(parser.parms,
                                                name, args=args, repl=string)
                name = re_cC.sub('C', m.group(1))
                parser.the_macros[name] = Macro(parser.parms,
                                                name, args=args, repl=string)
            else:
                name = m.group(1)
                parser.the_macros[name] = Macro(parser.parms,
                                                name, args=args, repl=string)

    # Make the \cref, …, \Crefrange* Macro objects:
    for ref in ['\\cref','\\Cref']:
        parser.the_macros[ref] = Macro(parser.parms,
                                       ref, args='*A',
                                       repl=h_make_cref(refs[ref]))
    for ref in ['\\crefrange','\\Crefrange']:
        parser.the_macros[ref] = Macro(parser.parms,
                                       ref, args='*AA',
                                       repl=h_make_crefrange(refs[ref]))

    # \YYCleverefInput should not produce any output:
    return []


def h_make_cref(cref):
    def f(parser, buf, mac, args, delim, pos):
        star = parser.get_text_direct(args[0])
        rep = parser.get_text_direct(args[1])
        if rep in cref[star]:
            toks = parser.parms.scanner.scan(cref[star][rep])
            for t in toks:
                t.pos = pos
            return toks
        return utils.latex_error(msg_cref_undefined.format(mac.name,rep),
                                 pos, parser.latex, parser.parms)
    return f


def h_make_crefrange(cref):
    def f(parser, buf, mac, args, delim, pos):
        star = parser.get_text_direct(args[0])
        rep = (parser.get_text_direct(args[1]), parser.get_text_direct(args[2]))
        if rep in cref[star]:
            toks = parser.parms.scanner.scan(cref[star][rep])
            for t in toks:
                t.pos = pos
            return toks
        return utils.latex_error(msg_crefrange_undefined.format(mac.name,*rep),
                                 pos, parser.latex, parser.parms)
    return f


def h_cref_warning(parser, buf, mac, args, delim, pos):
    return utils.latex_error(msg_sed_not_loaded,
                             pos, parser.latex, parser.parms)


def is_poorman_used(options):
    for opt in reversed(options):
        if 'poorman' in opt:
            return True
    return False
