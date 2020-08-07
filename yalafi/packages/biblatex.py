
#
#   YaLafi module for LaTeX package biblatex
#
#   very simple approximation
#   - citation text is fixed --> variable cite_text
#   - we always add [] brackets (even for \cite and \footcite)
#

from yalafi import defs
from yalafi.defs import Macro, ModParm

require_packages = []

cite_text = '0'

def modify_parameters(parms):

    macros_latex = ''

    macros_python = [

        Macro(parms, '\\cite', args='*OOA', repl=h_cite),
        Macro(parms, '\\Cite', args='*OOA', repl=h_cite),
        Macro(parms, '\\footcite', args='*OOA', repl=h_footcite),
        Macro(parms, '\\footcitetext', args='*OOA', repl=h_footcite),
        Macro(parms, '\\parencite', args='*OOA', repl=h_cite),
        Macro(parms, '\\Parencite', args='*OOA', repl=h_cite),

    ]

    environments = []

    return ModParm(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)


def h_cite(parser, buf, mac, args, pos):
    opt1 = args[1]
    opt2 = args[2]
    if len(opt1) == 1 and type(opt1[0]) is defs.VoidToken:
        # only [] given
        opt1 = []
    if opt2:
        pre = opt1
        if len(opt2) == 1 and type(opt2[0]) is defs.VoidToken:
            # only [] given
            opt2 = []
        post = opt2
    else:
        pre = []
        post = opt1
        
    out = [defs.TextToken(pos, '[', pos_fix=True)]
    if pre:
        out += pre
        out.append(defs.SpaceToken(out[-1].pos, ' ', pos_fix=True))
    out.append(defs.TextToken(out[-1].pos, cite_text, pos_fix=True))
    if post:
        out += [defs.TextToken(out[-1].pos, ',', pos_fix=True),
                    defs.SpaceToken(out[-1].pos, ' ', pos_fix=True)]
        out += post
    out += [defs.TextToken(out[-1].pos, ']', pos_fix=True),
                defs.ActionToken(out[-1].pos)]
    return out

def h_footcite(parser, buf, mac, args, pos):
    out = [defs.MacroToken(pos, '\\footnote'),
                defs.SpecialToken(pos, '{')]
    out += h_cite(parser, buf, mac, args, pos)
    out += [defs.TextToken(out[-1].pos, '.', pos_fix=True),
                defs.SpecialToken(out[-1].pos, '}'), defs.ActionToken(out[-1].pos)]
    return out

