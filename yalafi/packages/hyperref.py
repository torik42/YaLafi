
#
#   YaLafi module for LaTeX package hyperref
#

from yalafi.defs import InitModule, Macro

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = r"""

        \newcommand{\href}[3][]{#3}
        \newcommand{\texorpdfstring}[2]{#1}
        \newcommand{\url}[1]{#1}

    """

    macros_python = [

        Macro(parms, '\\ref', args='*A', repl='0'),
        Macro(parms, '\\pdfbookmark', args='OAA', extract='#2'),
        Macro(parms, '\\currentpdfbookmark', args='AA', extract='#1'),
        Macro(parms, '\\belowpdfbookmark', args='AA', extract='#1'),
        Macro(parms, '\\subpdfbookmark', args='AA', extract='#1'),
        
    ]

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

