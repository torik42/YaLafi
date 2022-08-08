import pytest
from yalafi import parameters, parser, utils

preamble = r'\usepackage[poorman]{cleveref}'


def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_latex = [

    (r'A\crefname{type}{singular}{plural}B', 'AB'),
    (r'A\Crefname{type}{singular}{plural}B', 'AB'),
    (r'A\crefalias{counter}{type}B', 'AB'),

]


@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected


preamble_sed = r'''\usepackage[poorman]{cleveref}
\YYCleverefInput{tests/test_packages/cleveref.sed}'''


def get_plain_sed(latex):
    def read(file):
        try:
            with open(file) as f:
                return True, f.read()
        except:
            return False, ''
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    plain, nums = utils.get_txt_pos(p.parse(preamble_sed + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_sed = [

    (r'\cref{a}', 'equation\N{NO-BREAK SPACE}(0)'),
    (r'\Cref{a}', 'Equation\N{NO-BREAK SPACE}(0)'),
    # (r'\crefrange{a}{b}', ''),
    # (r'\Crefrange{a}{b}', ''),
    (r'\cpageref{a}', 'page\N{NO-BREAK SPACE}0'),
    (r'\Cpageref{a}', 'Page\N{NO-BREAK SPACE}0'),
    (r'\cpagerefrange{a}{b}', 'pages\N{NO-BREAK SPACE}0 to\N{NO-BREAK SPACE}0'),
    (r'\Cpagerefrange{a}{b}', 'Pages\N{NO-BREAK SPACE}0 to\N{NO-BREAK SPACE}0'),
    (r'\namecref{a}', 'equation'),
    (r'\nameCref{a}', 'Equation'),
    (r'\namecrefs{a}', 'equations'),
    (r'\nameCrefs{a}', 'Equations'),
    (r'\lcnamecref{a}', 'equation'),
    (r'\lcnamecrefs{a}', 'equations'),

]


@pytest.mark.parametrize('latex,plain_expected', data_test_macros_sed)
def test_macros_sed(latex, plain_expected):
    plain = get_plain_sed(latex)
    assert plain == plain_expected


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
\usepackage{hyperref}
\YYCleverefInput{latex.sed}
\Cref*{eq:1}
"""
sed_2 = r"""
s/\\Cref\*{eq:1}/\\Cref@equation@name""" \
+ r""" \\nobreakspace \\textup {(\\ref \*{eq:1})}/g
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


latex_4 = r"""
\usepackage[poorman]{cleveref}
A\cref{lab}B
"""
plain_4 = """
A LATEXXXERROR B
"""

stderr_4 = r"""*** LaTeX error: code in 't.tex', line 3, column 2:
*** To use cleveref with YaLafi, you should use
*** \YYCleverefInput to load the sed file, e.g.
*** '\YYCleverefInput{main.sed}' if your LaTeX
*** document is called 'main.tex'.

"""


def test_4(capsys):
    capsys.readouterr()
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    toks = p.parse(latex_4, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    captured = capsys.readouterr()
    assert plain_4 == plain
    assert stderr_4 == captured.err


latex_5 = r"""
\usepackage[poorman]{cleveref}
\YYCleverefInput{main.sed}
A\cref{lab}B
"""
sed_5 = r"""
s/\\crefrange{eq:1}{eq:3}//g
"""
plain_5 = """
A LATEXXXERROR B
"""

stderr_5 = r"""*** LaTeX error: code in 't.tex', line 4, column 2:
*** No replacement for \cref{lab} known.
*** Run LaTeX again to build a new sed file.

"""


def test_5(capsys):
    def read(file):
        return True, sed_5
    capsys.readouterr()
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_5, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    captured = capsys.readouterr()
    assert plain_5 == plain
    assert stderr_5 == captured.err


latex_6 = r"""
A\usepackage{cleveref}B
\YYCleverefInput{main.sed}
"""
sed_6 = r"""
s/\\crefrange{eq:1}{eq:3}//g
"""
plain_6 = """
A LATEXXXERROR B
"""

stderr_6 = r"""*** LaTeX error: code in 't.tex', line 2, column 2:
*** To use cleveref with YaLafi, you need to use
*** the 'poorman' option and \YYCleverefInput
*** to load the sed file.

"""


def test_6(capsys):
    def read(file):
        return True, sed_6
    capsys.readouterr()
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_6, source='t.tex')
    plain, pos = utils.get_txt_pos(toks)
    captured = capsys.readouterr()
    assert plain_6 == plain
    assert stderr_6 == captured.err


latex_7 = r"""
\usepackage[poorman]{cleveref}
\YYCleverefInput{latex.sed}
\cref{eq: S^n $ [ . ] a*b}
"""
sed_7 = r"""
s/\\cref{eq: S\^n \$ \[ \. \] a\*b}/\\cref@equation@name \\nobreakspace \\textup {(\\ref {eq: S\^n \$ \[ \. \] a\*b})}/g
s/\\cref@equation@name /eq\./g
"""
plain_7 = """
eq.\N{NO-BREAK SPACE}(0)
"""


def test_7():
    def read(file):
        return True, sed_7
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    toks = p.parse(latex_7)
    plain, pos = utils.get_txt_pos(toks)
    assert plain_7 == plain
