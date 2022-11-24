

import pytest
from yalafi import parameters, parser, utils

preamble = ''

def get_plain_pos(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, pos = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(pos)
    return plain, pos

def get_plain(latex):
    plain, pos = get_plain_pos(latex)
    return plain

def pos_range(start, length):
    return [i for i in range(start, start+length)]

data_test_macros_latex = [

    (r'\AA', 'Å'),
    (r'\aa', 'å'),
    (r'\AE', 'Æ'),
    (r'A\addtocounter{name}{value}B', 'AB'),
    (r'\ae', 'æ'),
    (r'\author{name}', 'name.'),
    (r'A\bibitem{lab}B', 'A  B'),
    (r'A\bibliographystyle{alphadin}B', 'AB'),
    (r'A\footnotemark B', 'AB'),
    (r'A\footnotemark[1] B', 'A B'),
    (r'A\hfill B', 'A B'),
    (r'A\include{x_y.tex}B', 'AB'),
    (r'A\includeonly{x_y.tex}B', 'AB'),
    (r'A\index{x_y}B', 'AB'),
    (r'A\input{x_y.tex}B', 'AB'),
    (r'\L', 'Ł'),
    (r'\l', 'ł'),
    (r'A\label{l}B', 'AB'),
    (r'A\LaTeX B', 'ALaTeXB'),
    (r'A\newcounter{name}B', 'AB'),
    (r'A\newline B', 'A B'),
    (r'A\nobreakspace B', 'A\N{NO-BREAK SPACE}B'),
    (r'\O', 'Ø'),
    (r'\o', 'ø'),
    (r'\OE', 'Œ'),
    (r'\oe', 'œ'),
    (r'A\pagenumbering{roman}B', 'AB'),
    (r'\pageref{l}', '0'),
    (r'A\pagestyle{empty}B', 'AB'),
    (r'A\par B', 'A\n\nB'),
    (r'A\qquad B', 'A B'),
    (r'A\quad B', 'A B'),
    (r'\ref{l}', '0'),
    (r'A\refstepcounter{name}B', 'AB'),
    (r'\S', '§'),
    (r'A\setcounter{name}{value}B', 'AB'),
    (r'\ss', 'ß'),
    (r'A\stepcounter{name}B', 'AB'),
    (r'A\TeX B', 'ATeXB'),
    (r'\textasciicircum', '^'),
    (r'\textasciitilde', '~'),
    (r'\textbackslash', '\\'),
    (r'A\thispagestyle{empty}B', 'AB'),
    (r'A\vphantom{X}B', 'AB'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected


data_test_macros_python = [

    (r'\chapter[hi]{ho}', 'ho.'),
    (r'\chapter*{ho}', 'ho.'),
    (r'\chapter{ho?}', 'ho?'),
    (r'\cite{c}', '[0]'),
    (r'\cite[x]{c}', '[0, x]'),
    (r'A\documentclass[opts]{xxxx}B', 'AB'),
    (r'\framebox[x][y]{T}', 'T'),
    (r'A\hphantom{X}B', 'A B'),
    (r'A\hphantom{\label{l}}B', 'AB'),
    (r'A\hspace{1em}B', 'A B'),
    (r'A\hspace*{1em}B', 'A B'),
    (r'A\hspace{0cm}B', 'AB'),
    (r'A\hspace{ .0cm}B', 'AB'),
    (r'A\hspace{ ,5cm}B', 'A B'),
    (r'A\hspace{0.2pt}B', 'A B'),
    (r'A\hspace{0,2cm}B', 'A B'),
    (r'A\hspace{1.2,3cm}B', 'A B'),
    (r'A\linebreak B', 'A B'),
    (r'A\linebreak[4] B', 'A  B'),
    (r'A\linebreak[4]B', 'A B'),
    (r'A\linebreak [4]B', 'A B'),
    (r'A\linebreak[0] B', 'A B'),
    (r'A\linebreak[0]B', 'AB'),
    (r'A\linebreak [0]B', 'AB'),
    (r'A\linebreak[3] B', 'A B'),
    (r'A\linebreak[3]B', 'AB'),
    (r'A\linebreak [3]B', 'AB'),
    (r'A\linebreak[10]B', 'A LATEXXXERROR B'),
    (r'A\linebreak[ 3]B', 'AB'),
    (r'\newcommand{\test}{4}A\linebreak[ \test{} ]B', 'A B'),
    (r'\MakeLowercase{TeSt}', 'test', pos_range(15, 4)),
    (r'\MakeUppercase{TeSt}', 'TEST', pos_range(15, 4)),
    (r'\MakeUppercase{3 apples}', '3 APPLES'),
    (r'\newcommand{\test}{tesst}\MakeUppercase{A\test B}', 'ATESSTB', [40]+5*[41]+[47]),
    (r'A\newcommand{\xxx}{X}B', 'AB'),
    (r'A\newcommand*{\xxx}[1][x]{X}B', 'AB'),
    (r'A\newtheorem{xxx}{XYZ} B', 'AB'),
    (r'A\newtheorem{xxx}[c]{XYZ}[d] B', 'A B'),
    (r'\paragraph[hi]{ho}', 'ho.'),
    (r'\paragraph*{ho}', 'ho.'),
    (r'\paragraph{ho?}', 'ho?'),
    (r'\part[hi]{ho}', 'ho.'),
    (r'\part*{ho}', 'ho.'),
    (r'\part{ho?}', 'ho?'),
    (r'A\phantom{X}B', 'A B'),
    (r'A\phantom{\label{l}}B', 'AB'),
    (r'A\renewcommand{\xxx}{X}B', 'AB'),
    (r'A\renewcommand*{\xxx}[1][x]{X}B', 'AB'),
    (r'\section[hi]{ho}', 'ho.'),
    (r'\section*{ho}', 'ho.'),
    (r'\section{ho?}', 'ho?'),
    (r'\subsection[hi]{ho}', 'ho.'),
    (r'\subsection*{ho}', 'ho.'),
    (r'\subsection{ho?}', 'ho?'),
    (r'\subsubsection[hi]{ho}', 'ho.'),
    (r'\subsubsection*{ho}', 'ho.'),
    (r'\subsubsection{ho?}', 'ho?'),
    (r'\title[hi]{ho}', 'ho.'),
    (r'\title*{ho}', 'ho.'),
    (r'\title{ho?}', 'ho?'),
    (r'A\usepackage[opts]{xxxx}B', 'AB'),
    (r'A\vspace{1ex}B', 'A B'),
    (r'A\vspace*{1ex}B', 'A B'),

    (r'A\LTadd{x}B', 'AxB'),
    (r'A\LTalter{x}{y}B', 'AyB'),
    (r'A\LTinput{xxxx}B', 'AB'),
    (r'A\LTskip{x}B', 'AB'),

]

@pytest.mark.parametrize('latex,plain_expected', filter(lambda x: len(x)!=3,data_test_macros_python))
def test_macros_python(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected


@pytest.mark.parametrize('latex,plain_expected,pos_expected', filter(lambda x: len(x)==3, data_test_macros_python))
def test_macros_python_pos(latex, plain_expected, pos_expected):
    plain, pos = get_plain_pos(latex)
    assert plain == plain_expected
    assert pos == pos_expected


data_test_specials = [

    (r'A~B', 'A\N{NO-BREAK SPACE}B'),
    (r'A``B', 'A\N{LEFT DOUBLE QUOTATION MARK}B'),
    (r"A''B", 'A\N{RIGHT DOUBLE QUOTATION MARK}B'),
    (r'A--B', 'A\N{EN DASH}B'),
    (r'A---B', 'A\N{EM DASH}B'),

    (r'A\ B', 'A B'),
    ('A\\\tB', 'A B'),
    ('A\\\nB', 'A B'),
    (r'A\,B', 'A\N{NARROW NO-BREAK SPACE}B'),
    (r'A\:B', 'A B'),
    (r'A\;B', 'A B'),
    ('A\n\\;\nB', 'A\nB'),      # avoid new blank line
    (r'A\!B', 'AB'),

    (r'\{', '{'),
    (r'\}', '}'),
    (r'\$', '$'),
    (r'\#', '#'),
    (r'\&', '&'),
    (r'\_', '_'),
    (r'\%', '%'),

    (r'A\/B', 'AB'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_specials)
def test_specials(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected


data_test_environments = [

    (r'A\begin{figure}B\end{figure}C', 'ABC'),
    (r'A\begin{figure}[o]B\end{figure}C', 'ABC'),
    (r'A\begin{minipage}{0.5\linewidth}B\end{minipage}C', 'A\n\nB\n\nC'),
    (r'A\begin{table}B\end{table}C', 'ABC'),
    (r'A\begin{table}[o]B\end{table}C', 'ABC'),
    (r'A\begin{tabular}{|||}B\end{tabular}C', 'ABC'),
    (r'A\begin{thebibliography}{lab}B', 'A\n\nB'),
    (r'A\begin{verbatim}B\end{verbatim}C', 'A\n\nB\n\nC'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_environments)
def test_environments(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

