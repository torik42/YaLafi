#
#   Tex2txt, a flexible LaTeX filter
#   YaLafi: Yet another LaTeX filter
#   Copyright (C) 2018-2020 Matthias Baumann
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

##################################################################
#
#   run yalafi.shell as server
#
##################################################################

from . import utils
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['content-length'])
        data = self.rfile.read(length)
        requ = parse_qs(data.decode('utf-8'))
        message = self.create_message(requ)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(message).encode('ascii'))

    #   - include options given in HTML request fileds
    #   - run proofreader
    #   - map offset and length in each match to position in LaTeX text
    #
    def create_message(self, requ):
        language = requ['language'][0]
        latex = requ['text'][0]
        disable = requ.get('disabledRules', [''])[0]
        enable = requ.get('enabledRules', [''])[0]
        disablecategories = requ.get('disabledCategories', [''])[0]
        enablecategories = requ.get('enabledCategories', [''])[0]
        old_opts = self.server.my_lt_options.copy()
        new_opts = []
        option_map = self.server.my_option_map
        for f in option_map:
            if f not in requ or f == 'language':
                # NB: languagetool-commandline.jar does not like repeated
                # option --language
                continue
            new_opts.append(option_map[f][0][0])
            if option_map[f][1] == 1:
                new_opts.append(requ[f][0])
            while True:
                pos = next((i for i in range(len(old_opts))
                                if old_opts[i] in option_map[f][0]), -1)
                if pos < 0:
                    break
                # entry in --lt-options corresponds to HTML request field
                # --> remove
                old_opts[pos:pos+1+option_map[f][1]] = []
        latex, plain, charmap, matches = self.server.my_proofreader(
                                        latex, language, disable, enable,
                                        disablecategories, enablecategories,
                                        old_opts + new_opts)
        return {'matches': [utils.map_match_position(m, latex, charmap)
                                                        for m in matches]}

class Server(HTTPServer):
    def __init__(self, addr_port, handler, my_proofreader,
                                my_option_map, my_lt_options):
        super().__init__(addr_port, handler)
        self.my_proofreader = my_proofreader 
        self.my_option_map = my_option_map 
        self.my_lt_options = my_lt_options 
        
def run_server(addr, port, proofreader, option_map, lt_options):
    httpd = Server((addr, port), Handler, proofreader, option_map, lt_options)
    httpd.serve_forever()

