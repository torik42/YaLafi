

import pytest
from yalafi import parameters, parser, utils

preamble = ('\\usepackage{glossaries-extra}\n'
                + '\\LTinput{tests/test_packages/glossaries.glsdefs}\n')

def get_plain(latex):
    def read(file):
        try:
            with open(file) as f:
                return True, f.read()
        except:
            return False, ''
    parms = parameters.Parameters()
    p = parser.Parser(parms, read_macros=read)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    return plain


data_test_macros_latex = [

    (r'\newabbreviation{pp}{ppm}{parts per million}', 'Parts per million.'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

