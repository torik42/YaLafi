

import pytest
from yalafi import parameters, parser, utils

preamble = '\\documentclass{beamer}\n'


def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_latex = [

    (r'\setbeamercolor{A}{B}', ''),
    (r'\setbeamerfont{A}{B}', ''),
    (r'\setbeameroption{A}', ''),
    (r'\tableofcontents', ''),
    (r'\tableofcontents[A]', ''),
    (r'\usecolortheme[A]{B}', ''),
    (r'\usefonttheme[A]{B}', ''),
    (r'\useinnertheme[A]{B}', ''),
    (r'\useoutertheme[A]{B}', ''),
    (r'\usetheme[A]{B}', ''),

    (r'A\alert<1->{B}', 'AB'),
    (r'A\alert<article| beamer:1>{B}', 'AB'),
    (r'A\emph<1->{B}', 'AB'),
    (r'A\color<1->{blue}B', 'AB'),
    (r'A\invisible<1->{B}', 'AB'),
    (r'A\textcolor<1->{blue}{B}', 'AB'),
    (r'A\textsf<2->B', 'AB'),
    (r'A\uncover<1->{B}', 'AB'),
    (r'A\visible<1->{B}', 'AB'),

    (r'A\only<1->{B}C', 'ABC'),
    (r'A\only<1-> {B}C', 'ABC'),
    (r'A\only <1->{B}C', 'ABC'),
    (r'A\only{B}<1->C', 'ABC'),
    (r'A\only {B}<1->C', 'ABC'),
    (r'A\onslide<1->{B}', 'AB'),
    (r'A\onslide*<1->{B}', 'AB'),
    (r'A\onslide+<1->{B}', 'AB'),

    (r'A\part<1->{B}', 'AB. '),
    (r'A\section<1->{B}', 'AB. '),
    (r'A\section{B}', 'AB. '),
    (r'A\subsection{B}', 'AB. '),

    (r'A\item<+->B', 'A  B'),
    (r'A\item <+->B', 'A  B'),
    (r'A\item[C]<+->B', 'A C B'),
    (r'A\item[C] <+->B', 'A C B'),
    (r'A\item [C] <+->B', 'A C B'),
    (r'A\item<+->[C]B', 'A C B'),
    (r'A\item <+->[C]B', 'A C B'),
    (r'A\item<+-> [C]B', 'A C B'),
    (r'A\item <+-> [C] B', 'A C B'),
    (r'A\item<3-| alert@3>B', 'A  B'),

    (r'A\label<2>{label}B', 'AB'),

    (r'\frametitle<2->[hi]{ho}', 'hi. ho. '),
    (r'\framesubtitle<2->{ho}', 'ho. '),
    (r'\hyperlink<2->{reference}{Text}', 'Text'),
    (r'\hypertarget<2->{reference}{Text}', 'Text'),
    (r'\note<2->{B}', '\n\n\nB\n'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

