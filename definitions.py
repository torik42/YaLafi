
#
#   run-time modification of default parameters for scanner and parser
#   as defined in yalafi/parameters.py
#
#   Usage:
#       python -m yalafi --pyth definitions ...
#       python -m yalafi.shell --python-defs definitions ...
#


from yalafi.defs import Environ
from yalafi import handlers

def modify_parameters(parms):

    def thm(s):
        return handlers.h_theorem(s)

    parms.environment_defs += [

        # comment environment
        #
        Environ(parms, 'comment', repl='', remove=True, add_pars=False),

        # German theorem-style environments
        #
        Environ(parms, 'Anmerkung', args='O', repl=thm('Anmerkung')),
        Environ(parms, 'Beispiel', args='O', repl=thm('Beispiel')),
        Environ(parms, 'Definition', args='O', repl=thm('Definition')),
        Environ(parms, 'Korollar', args='O', repl=thm('Korollar')),
        Environ(parms, 'Nachweis', args='O', repl=thm('Nachweis')),
        Environ(parms, 'Proposition', args='O', repl=thm('Proposition')),
        Environ(parms, 'Satz', args='O', repl=thm('Satz')),

    ]

