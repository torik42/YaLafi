
#
#   tex2txt.py:
#   - test of \verb and \begin{verbatim}
#

from yalafi import tex2txt, defs, parameters, parser, utils

options = tex2txt.Options(lang='en', char=True)

def test_verb():

    latex = '\\verb?%x\\y?\\label{z}?'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == '%x\\y?'


def test_verbatim():

    # extra blank lines: see LAB:VERBATIM in tex2txt.py
    latex = 'A\\begin{verbatim}\\verb?%\\x?\n\\end{verbatim}B'
    plain, nums = tex2txt.tex2txt(latex, options)
    assert plain == 'A\n\n\\verb?%\\x?\n\n\nB'

latex_1 = r"""
X\begin{verbatim}
Y
\end{verbatim}Z
"""
plain_1 = r"""
X

Y


Z
"""
def test_1():
    # keep verbatim
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain == plain_1

plain_2 = r"""
XZ
"""
def test_2():
    # remove verbatim
    parms = parameters.Parameters()
    parms.environment_defs.append(defs.Environ(parms, 'verbatim',
                                    remove=True, add_pars=False))
    p = parser.Parser(parms)
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain == plain_2

plain_3 = r"""
X

[verbatim]

Z
"""
def test_3():
    # replace verbatim
    parms = parameters.Parameters()
    parms.environment_defs.append(defs.Environ(parms, 'verbatim',
                            repl='[verbatim]', remove=True))
    p = parser.Parser(parms)
    toks = p.parse(latex_1)
    plain, pos = utils.get_txt_pos(toks)
    assert plain == plain_3

