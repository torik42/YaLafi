#
#   YaLafi: \documentclass{beamer}
#

from yalafi.defs import InitModule, Macro, MacroToken, Environ, TextToken, SpaceToken
from yalafi import handlers as hs
from yalafi import utils

require_packages = ['xcolor']

macro_name_addon = '\\YYBeamerInternal@'


def init_module(parser, options, position):
    parms = parser.parms

    parser.global_latex_options += options

    # Change the item macro to take an overlay
    parser.item_macro = Macro(parms, '\\item', args='', repl=h_item_overlay)

    macros_latex = r"""
        \newcommand{\setbeamercolor}[2]{}
        \newcommand{\setbeamerfont}[2]{}
        \newcommand{\setbeameroption}[1]{}
        \newcommand{\tableofcontents}[1][]{}
        \newcommand{\usecolortheme}[2][]{}
        \newcommand{\usefonttheme}[2][]{}
        \newcommand{\useinnertheme}[2][]{}
        \newcommand{\useoutertheme}[2][]{}
        \newcommand{\usetheme}[2][]{}
    """

    macros_python = [
        Macro(parms, '\\only', args='', repl=h_only),
        Macro(parms, '\\onslide', args='', repl=h_onsilde),
        Macro(parms, '\\setbeamertemplate', args='AOA', repl='#3'),
    ]

    # Add commands defined by beamer
    # which take an overlay infront of other arguments:
    macros_python_ignore_overlay = [
        Macro(parms, '\\alert', args='A', repl='#1'),
        Macro(parms, '\\framesubtitle', args='A',
              repl=h_heading_without_star_and_option),
        Macro(parms, '\\frametitle', args='OA', repl=h_heading_without_star),
        Macro(parms, '\\hyperlink', args='AA', repl='#2'),
        Macro(parms, '\\hypertarget', args='AA', repl='#2'),
        Macro(parms, '\\invisible', args='A', repl='#1'),
        Macro(parms, '\\note', args='OA', extract='#2'),
        # this needs to be fixed:
        Macro(parms, '\\temporal', args='AAA', repl='#1', extract='#2\\par#3'),
        Macro(parms, '\\uncover', args='A', repl='#1'),
        Macro(parms, '\\visible', args='A', repl='#1'),
    ]

    for macro in macros_python_ignore_overlay:
        name = macro.name
        macro_int = macro
        macro_int.name = macro_name_addon + name[1:]
        macros_python.append(macro_int)
        macros_python.append(Macro(parms, name, args='', repl=h_ignore_overlay))

    # Add overlay to already defined commands
    # If not already defined, the overlay is removed nevertheless
    macros_ignore_overlay = [
        '\\color',
        '\\emph',
        '\\label',
        '\\part',
        '\\section',
        '\\subsection',
        '\\subsubsection',
        '\\textbf',
        '\\textcolor',
        '\\textit',
        '\\textmd',
        '\\textnormal',
        '\\textrm',
        '\\textsc',
        '\\textsf',
        '\\textsl',
        '\\texttt',
        '\\textup',
    ]

    for name in macros_ignore_overlay:
        if name in parser.the_macros:
            macro = parser.the_macros[name]
            macro.name = macro_name_addon + name[1:]
            macros_python.append(macro)
        macros_python.append(Macro(parms, name, args='', repl=h_ignore_overlay))

    environments = [
        Environ(parms, 'frame', args='', repl=h_frame),
        Environ(parms, 'overlayarea', args='AA'),
        Environ(parms, 'overprint', args='O'),
        Environ(parms, 'beamercolorbox', args='OA'),
        Environ(parms, 'beamerboxesrounded', args='OA',
                repl=h_heading_without_star),
        Environ(parms, 'alertblock', args='', repl=h_overlay_environment),
        Environ(parms, 'block', args='', repl=h_overlay_environment),
        Environ(parms, 'exampleblock', args='', repl=h_overlay_environment),
    ]

    return InitModule(macros_latex=macros_latex,
                      macros_python=macros_python, environments=environments)


def h_ignore_overlay(parser, buf, mac, args, delim, pos):
    parse_argument(parser, buf, pos, '<', '>')
    return [MacroToken(pos, macro_name_addon + mac.name[1:])]


def h_heading_without_star(parser, buf, mac, args, delim, pos):
    int_args = args
    int_args.insert(0, [])
    return hs.h_heading(parser, buf, mac, int_args, delim, pos)


def h_heading_without_star_and_option(parser, buf, mac, args, delim, pos):
    int_args = args
    int_args.insert(0, [])
    int_args.insert(0, [])
    return hs.h_heading(parser, buf, mac, int_args, delim, pos)


def h_item_overlay(parser, buf, mac, args, delim, pos):
    overlay = parse_argument(parser, buf, pos, '<', '>')
    option = parse_argument(parser, buf, pos, '[', ']')
    if not overlay:
        overlay = parse_argument(parser, buf, pos, '<', '>')
    if option:
        return option
    return []


def h_only(parser, buf, mac, args, delim, pos):
    overlay = parse_argument(parser, buf, pos, '<', '>')
    argument = parse_argument(parser, buf, pos, '{', '}')
    if not overlay:
        overlay = parse_argument(parser, buf, pos, '<', '>', skip_space=False)
    if argument:
        return argument
    return []


def h_overlay_environment(parser, buf, mac, args, delim, pos):
    overlay = parse_argument(parser, buf, pos, '<', '>')
    argument = parse_argument(parser, buf, pos, '{', '}')
    if not overlay:
        overlay = parse_argument(parser, buf, pos, '<', '>', skip_space=False)
    if argument:
        append_dot(parser, argument)
        return argument
    return utils.latex_error(parser,
                             'Missing argument for environment ' + mac.name,
                             pos)


def h_onsilde(parser, buf, mac, args, delim, pos):
    tok = buf.cur()
    if tok and tok.txt in ('+', '*'):
        buf.next()
        tok = buf.skip_space()
    if tok and tok.txt == '<':
        parser.arg_buffer(buf, pos, end='>').all()
        tok = buf.skip_space()
    if tok and tok.txt == '{':
        return parser.arg_buffer(buf, pos).all()
    return []


def h_frame(parser, buf, mac, args, delim, pos):
    parse_argument(parser, buf, pos, '<', '>')
    parse_argument(parser, buf, pos, '[', ']')
    parse_argument(parser, buf, pos, '[', ']')
    title = parse_argument(parser, buf, pos, '{', '}')
    short_title = parse_argument(parser, buf, pos, '{', '}')
    if short_title:
        append_dot(parser, short_title)
    else:
        short_title = []
    if title:
        append_dot(parser, title)
    else:
        title = []
    return short_title + title


def parse_argument(parser, buf, pos, begin, end, skip_space=True):
    tok = buf.cur()
    old_tok = None
    if skip_space:
        old_tok = tok
        tok = buf.skip_space()
    argument = None
    if tok and tok.txt == begin:
        argument = parser.arg_buffer(buf, pos, end=end).all()
    elif old_tok and buf.is_space(old_tok):
        buf.back([old_tok])
    return argument


def append_dot(parser, toks):
    txt = parser.get_text_expanded(toks).strip()
    if (txt and parser.parms.heading_punct
            and txt[-1] not in parser.parms.heading_punct):
        toks.append(TextToken(toks[-1].pos, '.'))
    toks.append(SpaceToken(toks[-1].pos, ' '))
