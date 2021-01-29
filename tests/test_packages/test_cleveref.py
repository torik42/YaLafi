from yalafi import parameters, parser, utils


latex_1 = r"""
\usepackage[poorman]{cleveref}
\newcommand{\YYCleverefInput}[1]{}  % this definition should be ignored
\YYCleverefInput{latex.sed}
\cref{eq:1}
"""
sed_1 = r"""
s/\\cref{eq:1}/\\cref@equation@name \\nobreakspace \\textup {(\\ref {eq:1})}/g
s/\\cref@equation@name /eq\./g
"""
plain_1 = """
eq.\N{NO-BREAK SPACE}(0)
"""


def test_1():
    def read(file):
        return True, sed_1
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain


latex_2 = r"""
\usepackage[poorman]{cleveref}
\YYCleverefInput{latex.sed}
\Cref*{eq:1}
"""
sed_2 = r"""
s/\\Cref\*{eq:1}/\\Cref@equation@name \\nobreakspace \\textup {(\\ref \*{eq:1})}/g
s/\\Cref@equation@name /Equation/g
"""
plain_2 = """
Equation\N{NO-BREAK SPACE}(0)
"""


def test_2():
    def read(file):
        return True, sed_2
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_2)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_2 == plain


latex_3 = r"""
\usepackage[poorman]{cleveref}
\YYCleverefInput{latex.sed}
\crefrange{eq:1}{eq:3}
"""
sed_3 = r"""
s/\\crefrange{eq:1}{eq:3}//g
"""
plain_3 = """
"""


def test_3():
    def read(file):
        return True, sed_3
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_3)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_3 == plain
