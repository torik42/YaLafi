

import pytest
from yalafi import parameters, parser, utils

preamble = ('\\usepackage{glossaries-extra}\n'
                + '\\LTinput{tests/test_packages/glossaries-extra.glsdefs}\n')

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
    assert len(plain) == len(nums)
    return plain

#   we first repeat tests from package glossaries, since the format of
#   .glsdefs file is slightly different for glossaries-extra
#
from tests.test_packages import test_glossaries
@pytest.mark.parametrize('latex,plain_expected',
                                test_glossaries.data_test_macros_latex)
def test_macros_latex_glossaries(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

data_test_macros_latex = [

    (r'\newabbreviation{pp}{ppm}{parts per million}', 'Parts per million.'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
def test_macros_latex(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

