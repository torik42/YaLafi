
#
#   aux functions for tests
#

from yalafi import parameters, parser, utils

def get_plain_pos(latex, preamble='', lang='en-GB'):
    parms = parameters.Parameters(language=lang)
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain, nums

def get_plain(latex, preamble='', lang='en-GB'):
    plain, nums = get_plain_pos(latex, preamble, lang)
    return plain
