
#
#   splitting of multi-language texts into several parts
#

from yalafi import parameters, parser, utils
from yalafi.packages import babel

prefix = '\\usepackage{babel}\n'

def get_ml(latex, lang='de-DE'):
    parms = parameters.Parameters(language=lang)
    parms.multi_language = True

    babel.modify_language_map('lang1', 'de-DE')
    babel.modify_language_map('lang2', 'en-GB')
    babel.modify_language_map('lang3', 'ru-RU')

    p = parser.Parser(parms)
    toks = p.parse(prefix + latex)
    return utils.get_txt_pos_ml(toks, lang, parms)

def get_ml_txt(latex, lang='de-DE'):
    ml = get_ml(latex, lang)
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

latex_7 = r"""
A"`B"'C"=D"-E
K""=L"\xxx M
\selectlanguage{english}
A"`B"'C"=D"-E
K""=L"\xxx M
"""
plain_7 = {
'de-DE': [
"""
A„B“C-DE
K"-L"M
"""
],
'en-GB': [
"""A"`B"'C"=D"-E
K""=L"M
"""
]
}
def test_7():
    plain = get_ml_txt(latex_7, lang='de-DE')
    assert plain == plain_7

latex_8 = r"""
"A"a"O"o"U"u"s
\selectlanguage{english}
"A"a"O"o"U"u"s
"""
plain_8 = {
'de-DE': [
"""
ÄäÖöÜüß
"""
],
'en-GB': [
""""A"a"O"o"U"u"s
"""
]
}
def test_8():
    plain = get_ml_txt(latex_8, lang='de-DE')
    assert plain == plain_8

#   issue #104
#
latex_9 = r"""
"`\foreignlanguage{english}{"`x"'}"'
"""
plain_9 = {
'de-DE': [
"""
„L-L-L“
"""
],
'en-GB': [
""""`x"'"""
]
}
def test_9():
    plain = get_ml_txt(latex_9, lang='de-DE')
    assert plain == plain_9

#   issue #104
#
latex_10 = r"""
"`\foreignlanguage{german}{"`x"'}"'
"""
plain_10 = {
'de-DE': [
"""„x“"""
],
'en-GB': [
"""
"`L-L-L"'
"""
]
}
def test_10():
    plain = get_ml_txt(latex_10, lang='en-GB')
    assert plain == plain_10

#   issue #109
#
latex_11 = r"""
"a
\usepackage{babel}
"a
\usepackage[english,german]{babel}
"a
\selectlanguage{english}
"a
"""
plain_11 = {
'de-DE': [
"""ä
"""
],
'en-GB': [
"""
"a
"a
""", """"a
"""
],
}
def test_11():
    plain = get_ml_txt(latex_11, lang='en-GB')
    assert plain == plain_11

#   issue #117: copy leading and trailing space to replacement
#
latex_12 = r"""
A\foreignlanguage{german}{ G
}B
"""
plain_12 = {
'de-DE': [
""" G
"""
],
'en-GB': [
"""
A L-L-L
B
"""
]
}
def test_12():
    plain = get_ml_txt(latex_12, lang='en-GB')
    assert plain == plain_12

latex_13 = r"""
A
\begin{otherlanguage}{german}
B
\end{otherlanguage}
C
\begin{otherlanguage}{german}
D%
\end{otherlanguage}
E
\begin{otherlanguage*}{german}
F%
\end{otherlanguage*}
G
"""
plain_13 = {
'de-DE': [
"""B
""",
"""D""",
"""F"""
],
'en-GB': [
"""
A
L-L-L
C
M-M-ME
N-N-N
G
"""
]
}
def test_13():
    plain = get_ml_txt(latex_13, lang='en-GB')
    assert plain == plain_13

