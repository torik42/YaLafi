

import pytest
from yalafi import parameters, parser, utils

preamble = '\\documentclass{book}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    return plain


