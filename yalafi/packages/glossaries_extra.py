
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

from yalafi.defs import Macro, InitModule
from yalafi.packages.glossaries import h_gls, cap_first

require_packages = ['glossaries']

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\glsxtrfull}[1]{\glsxtrshort{#1} (\glsxtrlong{#1})}
        \newcommand{\Glsxtrfull}[1]{\glsxtrshort{#1} (\Glsxtrlong{#1})}

    """

    macros_python = [

        Macro(parms, '\\newabbreviation', args='AAA',
                                            repl=r'\newacronym{#1}{#2}{#3}'),
        Macro(parms, '\\glsxtrshort', args='OA', repl=h_gls('short', [])),
        Macro(parms, '\\Glsxtrshort', args='OA',
              repl=h_gls('short', [cap_first])),
        Macro(parms, '\\glsxtrlong', args='OA', repl=h_gls('long', [])),
        Macro(parms, '\\Glsxtrlong', args='OA',
              repl=h_gls('long', [cap_first])),

    ]

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

