#
# Special tests for \newcommand, \renewcommand, \providecommand and \def
#


import pytest
from yalafi import parameters, parser, utils


def trim(string):
    """
    Remove first and last line and the first eight characters from every
    line in string.
    """
    lines = string.split('\n')
    return '\n'.join(line[8:] for line in lines[1:-1])


def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, pos = utils.get_txt_pos(p.parse(latex, source='t.tex'))
    return plain


data_test_newcommand = [
    # Spaces in the following are important!
    # From each string, the first and last line will be stripped.
    # From every other line, the first eight characters (all space)
    # will be stripped.
    (
    # LaTeX:
        r"""
        \newcommand{\xxx}[1][X]{#1Z}
        \xxx
        \xxx
        [A]
        """,
    # Plain:
        r"""
        XZAZ
        """
    ),
    (
    # LaTeX:
        r"""
        \newcommand{\xxx}[2][X]{#2#1}
        \xxx{ A }
        \xxx[B]C
        """,
    # Plain:
        r"""
         A X
        CB
        """
    ),
    (
    # LaTeX:
        r"""
        \def\xxx#1#2{X#2Y#1Z}
        \xxx AB
        """,
    # Plain:
        r"""
        XBYAZ
        """
    ),
    (
    # LaTeX:
        r"""
        \def\zB{z.\,B.\ }
        X \zB Y
        """,
    # Plain:
        """
        X z.\N{NARROW NO-BREAK SPACE}B. Y
        """
    ),
    (
    # LaTeX:
        r"""
        \def\xxx[#1]{#1:#1}
        X\xxx
        [a]Y
        """,
    # Plain:
        r"""
        Xa:aY
        """
    ),
    (
    # \newcommand currenly overwrites existing commands
    # LaTeX:
        r"""
        \newcommand{\test}[1]{A #1}
        \newcommand{\test}[1]{B #1}
        \test{C}
        """,
    # Plain:
        r"""
        B C
        """
    ),
    (
    # \renewcommand should overwrite existing commands
    # LaTeX:
        r"""
        \newcommand{\test}[1]{A #1}
        \renewcommand{\test}[1]{B #1}
        \test{C}
        """,
    # Plain:
        r"""
        B C
        """
    ),
    (
    # \providecommand should NOT overwrite existing commands
    # LaTeX:
        r"""
        \newcommand{\test}[1]{A #1}
        \providecommand{\test}[1]{B #1}
        \test{C}
        """,
    # Plain:
        r"""
        A C
        """
    ),
    (
    # LaTeX:
        r"""
        \providecommand{\test}[1]{B #1}
        \test{C}
        """,
    # Plain:
        r"""
        B C
        """
    ),

]


@pytest.mark.parametrize('latex,plain_expected', data_test_newcommand)
def test_newcommand(latex, plain_expected):
    plain = get_plain(trim(latex))
    assert plain == trim(plain_expected)


data_test_newcommand_error = [
    # Spaces in the following are important!
    # From each string, the first and last line will be stripped.
    # From every other line, the first eight characters (all space)
    # will be stripped.
    (
    # LaTeX:
        r"""
        \def
        """,
    # Plain:
        r"""
         LATEXXXERROR 
        """,
    # stderr:
        r"""
        *** LaTeX error: code in 't.tex', line 1, column 1:
        *** \def: missing macro name

        """
    ),
    (
    # LaTeX:
        r"""
        \def \;
        """,
    # Plain:
        r"""
         LATEXXXERROR  
        """,
    # stderr:
        r"""
        *** LaTeX error: code in 't.tex', line 1, column 6:
        *** \def: illegal macro name "\;"

        """
    ),
    (
    # LaTeX:
        r"""
        \def\xxx
        """,
    # Plain:
        r"""
         LATEXXXERROR 
        """,
    # stderr:
        r"""
        *** LaTeX error: code in 't.tex', line 1, column 1:
        *** \def: missing macro body

        """
    ),
    (
    # LaTeX:
        r"""
        \def\xxx#1#3{}
        """,
    # Plain:
        r"""
         LATEXXXERROR 
        """,
    # stderr:
        r"""
        *** LaTeX error: code in 't.tex', line 1, column 11:
        *** \def: unexpected argument '#3'

        """
    ),
    (
    # LaTeX:
        r"""
        \def\xxx#1{#3}
        """,
    # Plain:
        r"""
         LATEXXXERROR 
        """,
    # stderr:
        r"""
        *** LaTeX error: code in 't.tex', line 1, column 12:
        *** \def: illegal argument reference '#3'

        """
    ),
]


@pytest.mark.parametrize('latex,plain_expected,stderr_expected', data_test_newcommand_error)
def test_newcommand_error(latex, plain_expected, stderr_expected, capsys):
    capsys.readouterr()
    plain = get_plain(trim(latex))
    cap = capsys.readouterr()
    assert plain == trim(plain_expected)
    assert cap.err == trim(stderr_expected)
