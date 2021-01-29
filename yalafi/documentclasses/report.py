
#
#   YaLafi: \documentclass{report}
#

from yalafi.defs import InitModule

require_packages = []

def init_module(parser, options, position):
    parms = parser.parms

    parser.global_latex_options += options

    return InitModule()

