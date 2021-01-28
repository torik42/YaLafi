from yalafi import parameters, parser, utils


latex_1 = r"""
\usepackage[poorman]{cleveref}
% this definition should be ignored
\newcommand{\LTReadSed}[1]{}
\LTReadSed{latex.sed}
\cref{eq:1}
"""
sed_1 = r"""
s/\\cref{eq:1}/\\cref@equation@name \\nobreakspace \\textup {(\\ref {eq:1})}/g
s/\\cref@equation@name /eq\./g
"""
plain_1 = """
eq.\xa0(0)
"""


def test_1():
    def read(file):
        return True, sed_1
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_1 == plain
