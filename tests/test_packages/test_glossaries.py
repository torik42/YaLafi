

import pytest
from yalafi import parameters, parser, utils

preamble_pre_4_47 = (
    '\\usepackage{glossaries}\n'
    + '\\LTinput{tests/test_packages/glossaries_pre_4_47.glsdefs}\n')

preamble_post_4_47 = (
    '\\usepackage{glossaries}\n'
    + '\\LTinput{tests/test_packages/glossaries_post_4_47.glsdefs}\n')

def gen_get_plain(preamble):
    def get_plain(latex):
        def read(file):
            try:
                with open(file) as f:
                    return True, f.read()
            except:
                return False, ''
        parms = parameters.Parameters()
        p = parser.Parser(parms, read_macros=read)
        plain, nums = utils.get_txt_pos(
            p.parse(preamble + latex, source='t.tex'))
        assert len(plain) == len(nums)
        return plain
    return get_plain

get_plain_versions = [gen_get_plain(preamble_pre_4_47),
                      gen_get_plain(preamble_post_4_47)]

data_test_macros_latex = [

    (r'\gls{pp}', 'ppm'),
    (r'\gls[OOO]{pp}', 'ppm'),
    (r'\glspl{pp}', 'ppms'),
    (r'\Gls{pp}', 'Ppm'),
    (r'\Glspl{pp}', 'Ppms'),
    (r'\GLS{pp}', 'PPM'),
    (r'\GLSpl{pp}', 'PPMS'),
    (r'\gls{ex}', 'example'),
    (r'\glspl{ex}', 'examples'),
    (r'\Gls{ex}', 'Example'),
    (r'\Glspl{ex}', 'Examples'),
    (r'\GLS{ex}', 'EXAMPLE'),
    (r'\GLSpl{ex}', 'EXAMPLES'),

    (r'\glsdesc{ex}', 'a sample'),
    (r'\Glsdesc{ex}', 'A sample'),
    (r'\GLSdesc{ex}', 'A SAMPLE'),

    (r'\glsdisp{ex}{xyz}', 'xyz'),
    (r'\glslink{ex}{xyz}', 'xyz'),

    (r'\glstext{ex}', 'example'),
    (r'\Glstext{ex}', 'Example'),
    (r'\GLStext{ex}', 'EXAMPLE'),

    (r'\longnewglossaryentry{ex}{name=example}{a sample}', 'A sample.'),
    (r'\longnewglossaryentry{ex}{name=example}{a sample.}', 'A sample.'),
    (r'\longnewglossaryentry{ex}{name=example}{a sample?}', 'A sample?'),
    (r'\newacronym{pp}{ppm}{parts per million}', 'Parts per million.'),
    (r'\newacronym{pp}{ppm}{parts per million.}', 'Parts per million.'),
    (r'\newacronym{pp}{ppm}{parts per million?}', 'Parts per million?'),
    (r'\newglossaryentry{ex}{name=example, description = {a sample}}',
                                                            'A sample.'),
    (r'\newglossaryentry{ex}{name=example, description = {a sample.}}',
                                                            'A sample.'),
    (r'\newglossaryentry{ex}{name=example, description = {a sample?}}',
                                                            'A sample?'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_latex)
@pytest.mark.parametrize('get_plain', get_plain_versions)
def test_macros_latex(latex, plain_expected, get_plain):
    plain = get_plain(latex)
    assert plain == plain_expected

latex_1 = r"""
\gls{XXX}
"""
plain_1 = """
 LATEXXXERROR 
"""
stderr_1 = r"""*** LaTeX error: code in 't.tex', line 4, column 1:
*** could not find label for \gls... - did you include "\LTinput{<main file>.glsdefs}"?
"""
@pytest.mark.parametrize('get_plain', get_plain_versions)
def test_1(capsys, get_plain):
    capsys.readouterr()
    plain = get_plain(latex_1)
    cap = capsys.readouterr()
    assert plain == plain_1
    assert cap.err == stderr_1
