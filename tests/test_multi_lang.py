
#
#   splitting of multi-language texts into several parts
#

from yalafi import parameters, parser, utils
from yalafi.packages import babel

prefix = '\\usepackage{babel}\n'

def get_ml(latex):
    parms = parameters.Parameters(language='de-DE')
    parms.multi_language = True

    babel.modify_language_map('lang1', 'de-DE')
    babel.modify_language_map('lang2', 'en-GB')
    babel.modify_language_map('lang3', 'ru-RU')

    p = parser.Parser(parms)
    toks = p.parse(prefix + latex)
    return utils.get_txt_pos_ml(toks, 'de-DE', parms)

def get_ml_txt(latex):
    ml = get_ml(latex)
    return {k: [tp[0] for tp in v] for (k,v) in ml.items()}

latex_1 = r"""
A
"""
plain_1 = {
'de-DE': [
"""
A
"""
]
}
def test_1():
    plain = get_ml_txt(latex_1)
    assert plain == plain_1

latex_2 = r"""
\newcommand{\xxx}{lang2}
\selectlanguage{\xxx}
A
"""
plain_2 = {
# NB: the initial line break is for de-DE
'en-GB': [
"""A
"""
],
'de-DE': [
"""
"""
]
}
def test_2():
    plain = get_ml_txt(latex_2)
    assert plain == plain_2

latex_3 = r"""
G \foreignlanguage{lang2}{E E E}
G
"""
plain_3 = {
'de-DE': [
"""
G L-L-L
G
"""
],
'en-GB': [
"""E E E"""
]
}
def test_3():
    plain = get_ml_txt(latex_3)
    assert plain == plain_3

#   Here, the intermediate text is too long.
#   cf. utils.ml_check_lang_section()
#
latex_4 = r"""
G \foreignlanguage{lang2}{E E E E} G
"""
plain_4 = {
'de-DE': [
"""
G """,  # note the space
""" G
"""
],
'en-GB': [
"""E E E E"""
]
}
def test_4():
    plain = get_ml_txt(latex_4)
    assert plain == plain_4

#   footnote should have original language
#
latex_5 = r"""
A\footnote{F} B
\selectlanguage{lang2}

C
"""
plain_5 = {
'de-DE': [
"""
A B
"""
,
"""F
"""
],
'en-GB': [
"""
C



"""
]
}
def test_5():
    plain = get_ml_txt(latex_5)
    assert plain == plain_5

#   test multi-lang in \text{...}
#
latex_6 = r"""
\usepackage{amsmath}
A
\begin{align}
    x &= y \text{ \foreignlanguage{lang2}{for all} } y
\end{align}
B
"""
plain_6 = {
'de-DE': [
"""
A
  V-V-V  gleich W-W-W L-L-L X-X-X
B
"""
],
'en-GB': [
"""for all"""
]
}
def test_6():
    plain = get_ml_txt(latex_6)
    assert plain == plain_6

