
#
#   - test of nesting for macros
#   - test of nesting for environments with replacement
#

from yalafi import defs, parameters, parser, utils

parms = parameters.Parameters('en')
parms.environment_defs.append(
        defs.Environ(parms, 'table', repl='[Tabelle]', remove=True))
p = parser.Parser(parms)

def test_nested_macro():

    latex = '\\usepackage{xcolor}\\textcolor{x}{\\textcolor{y}{z}}'
    toks = p.parse(latex)
    plain, pos = utils.get_txt_pos(toks)
    assert plain == 'z'


def test_nested_table():

    latex = '\\begin{table}A\\begin{table}B\\end{table}C\\end{table}'
    toks = p.parse(latex)
    plain, pos = utils.get_txt_pos(toks)
    assert plain == '\n\n[Tabelle]\n\n'

    latex = '\\begin{table}A\\begin{tablx}B\\end{table}C\\end{table}'
    toks = p.parse(latex)
    plain, pos = utils.get_txt_pos(toks)
    assert plain == '\n\n[Tabelle]\n\nC\n\n'

