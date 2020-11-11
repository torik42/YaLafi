

import pytest
from yalafi import parameters, parser, utils

preamble = '\\documentclass{article}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    return plain

latex_1 = r"""
"""
plain_1 = """
"""
def test_1():
    plain = get_plain(latex_1)
    assert plain == plain_1

