
#
#   YaLafi module for LaTeX package glossaries-extra
#
#   PLEASE NOTE the comments at the beginning of glossaries.py
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

