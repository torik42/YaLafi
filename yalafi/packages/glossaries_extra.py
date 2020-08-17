
#
#   YaLafi module for LaTeX package glossaries-extra
#
#   - In order to let LaTeX generate the .glsdefs file, say
#       \usepackage[docdef=true]{glossaries-extra}
#   - Please note the comments at the beginning of glossaries.py.
#   - You can keep all definitions of glossary entries in the preamble,
#     if you say
#       \usepackage[docdef=atom]{glossaries-extra}
#

from yalafi.defs import Macro, ModParm

require_packages = ['glossaries']

def modify_parameters(parms):

    macros_latex = ''

    macros_python = [

        Macro(parms, '\\newabbreviation', args='AAA',
                                            repl=r'\newacronym{#1}{#2}{#3}'),

    ]

    environments = []

    return ModParm(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

