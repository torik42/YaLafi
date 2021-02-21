
#
#   YaLafi module for LaTeX package cleveref
#   Contributed by @torik42 (at GitHub) in pull request #171
#

from yalafi.defs import InitModule, Macro, VoidToken
from yalafi import utils
import re


require_packages = []

macro_read_sed = '\\YYCleverefInput'

# Commands whose replacements are read from sed file based on given arguments.
# The boolean value indicates, whether it is a usual command taking only one
# argument or a range command taking two arguments.
reference_commands = [
    ('\\cref', False),
    ('\\Cref', False),
    ('\\crefrange', True),
    ('\\Crefrange', True),
    ('\\cpageref', False),
    ('\\Cpageref', False),
    ('\\cpagerefrange', True),
    ('\\Cpagerefrange', True),
    ('\\namecref', False),
    ('\\nameCref', False),
    ('\\namecrefs', False),
    ('\\nameCrefs', False),
    ('\\lcnamecref', False),
    ('\\lcnamecrefs', False),
]

usual_commands = []
range_commands = []
for name, isRange in reference_commands:
    if isRange:
        range_commands.append('\\' + name)
    else:
        usual_commands.append('\\' + name)

# Regular Expressions used to read sed file:
re_ref = re.compile(r'''
s/\\
(                   # group 1: match usual commands
''' + '|'.join(usual_commands) + r'''
)
(?:\\)?             # non capturing group
(\*?)               # group 2: '*' if present, '' else
\{
    ([^}{]+)        # group 3: the label of the reference
\}
/
    (.*)            # group 4: the replacement string
/g
''', re.VERBOSE)

re_ref_range = re.compile(r'''
s/\\
(                   # group 1: match range commands
''' + '|'.join(range_commands) + r'''
)
(?:\\)?             # non capturing group
(\*?)               # group 2: '*' if present, '' else
\{
    ([^}{]+)        # group 3: the label of the first reference
\}
\{
    ([^}{]+)        # group 4: the label of the second reference
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
re_escaped_symbols = re.compile(r'\\([\[\]*\^$.\\])')


def unescape_sed(string):
    r"""
    Replaces certain strings that are escaped in sed file.
    Escaped are: . \ [ ] * ^ $
    """
    return re_escaped_symbols.sub(r'\1', string)


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
        % \crefname is wrongly replaced by sed file!
        \newcommand{\Crefname}[3]{}
        \newcommand{\crefalias}[2]{}
    '''

    macros_python = [

        Macro(parms, macro_read_sed, args='A', repl=h_read_sed),
        Macro(parms, '\\label', args='OA', repl=''),

    ]

    # Define functions which warn the User, whenever cleveref
    # is used without invoking \YYCleverefInput. These will be overwritten
    # by invoking \YYCleverefInput.
    for name, isRange in reference_commands:
        args = '*A' + 'A'*isRange
        macro = Macro(parms, name, args=args, repl=h_cref_warning)
        macros_python.append(macro)

    environments = []

    # Warn the user, whenever cleveref is used
    # without the poorman option:
    inject_tokens = []
    if not is_poorman_used(options):
        inject_tokens = utils.latex_error(parser, msg_poorman_option, position)

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
        return utils.latex_error(parser, 'could not read file ' + repr(file),
                                 pos)

    # Nested Dictionary in which all arguments and replacements are stored.
    # The structure is as follows
    #     '<command name>':
    #         '*':
    #             '<argument>' or ('<first argument>', '<second argument>'):
    #                 '<replacement>'
    #         '':
    #             '<argument>' or ('<first argument>', '<second argument>'):
    #                 '<replacement>'
    # The command name is any of the commands in reference_commands. The '*' or
    # '' says, whether a certain command is given with or without a star. The
    # argument is one particular argument given to the command. If the command
    # is a \…range command which takes to arguments a tuple of arguments is
    # given. The replacement is the string with which the particular command
    # should be replaced.
    refs = {}
    for name, isRange in reference_commands:
        refs[name] = {'': {}, '*': {}}

    for rep in sed.split('\n'):
        # only consider non-empty lines:
        if rep == '':
            continue

        # Match usual reference commands (e.g. \cref) and
        # save the replacement string:
        m = re_ref.match(rep)
        if m:
            refs[m.group(1)][m.group(2)][unescape_sed(m.group(3))] \
                = unescape_sed(m.group(4))
            continue

        # Match range reference command (e.g. \crefrange) and
        # save the replacement string:
        m = re_ref_range.match(rep)
        if m:
            key = (unescape_sed(m.group(3)), unescape_sed(m.group(4)))
            refs[m.group(1)][m.group(2)][key] \
                = unescape_sed(m.group(5))

        # Match any other command and create Macro objects for them.
        # See definition of re_command for more details:
        m = re_command.match(rep)
        if m:
            args = 'A'*int((m.end(3)-m.start(3))/4)
            string = unescape_sed(m.group(4))
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

    # Make the Macro objects for all commands in reference_commands:
    for name, isRange in reference_commands:
        if isRange:
            parser.the_macros[name] = Macro(parser.parms,
                                            name, args='*AA',
                                            repl=h_make_crefrange(refs[name]))
        else:
            parser.the_macros[name] = Macro(parser.parms,
                                            name, args='*A',
                                            repl=h_make_cref(refs[name]))

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
        return utils.latex_error(parser,
                                 msg_cref_undefined.format(mac.name,rep), pos)
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
        return utils.latex_error(parser,
                                 msg_crefrange_undefined.format(mac.name,*rep),
                                 pos)
    return f


def h_cref_warning(parser, buf, mac, args, delim, pos):
    return utils.latex_error(parser, msg_sed_not_loaded, pos)


def is_poorman_used(options):
    for opt in reversed(options):
        if 'poorman' in opt:
            return True
    return False
