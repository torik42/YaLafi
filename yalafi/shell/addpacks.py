
#
#   YaLafi: Yet another LaTeX filter
#   Copyright (C) 2020 Matthias Baumann
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

#
#   extract packages included by a file
#   - register as package extension module at yalafi
#   - overwrite macros \documentclass, \usepackage
#   - track calls of these macros
#

from yalafi import defs, tex2txt

require_packages = []
def modify_parameters(parms):
    def add(parser, buf, mac, args, pos):
        packages.append(parser.get_text_expanded(args[1]))
        return []
    macros_python = [
        defs.Macro(parms, '\\documentclass', args='OA', repl=add),
        defs.Macro(parms, '\\usepackage', args='OA', repl=add),
    ]
    return defs.ModParm(macros_python=macros_python)

packages = []
def addpacks(cmdline):
    packs = '.yalafi.shell.addpacks'
    if cmdline.packages.strip(','):
        packs = cmdline.packages.strip(',') + ',' + packs
    opts = tex2txt.Options(defs=cmdline.define, lang=cmdline.language[:2],
                                    pack=packs)
    f = tex2txt.myopen(cmdline.add_packages, encoding=cmdline.encoding)
    latex = f.read()
    f.close()
    tex2txt.tex2txt(latex, opts)
    return packages

