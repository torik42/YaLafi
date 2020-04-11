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

    #   correct offset and length in each match
    #
    def create_message(self, requ):
        language = requ['language'][0]
        latex = requ['text'][0]
        disable = requ.get('disabledRules', [''])[0]
        options = []
        option_map = self.server.my_option_map
        for f in option_map:
            if f in requ:
                options.append(option_map[f][0][0])
                if option_map[f][1] == 1:
                    options.append(requ[f][0])
        latex, plain, charmap, matches = self.server.my_proofreader(
                                        latex, language, disable, options)
        def f(m):
            beg = min(max(0, m['offset']), len(charmap) - 1)
            end = min(max(0, beg + m['length'] - 1), len(charmap) - 1)
            m['offset'] = abs(charmap[beg]) - 1
            m['length'] = abs(charmap[end]) - abs(charmap[beg]) + 1
            return m
        return {'matches': [f(m) for m in matches]}

class Server(HTTPServer):
    def __init__(self, addr_port, handler, my_proofreader, my_option_map):
        super().__init__(addr_port, handler)
        self.my_proofreader = my_proofreader 
        self.my_option_map = my_option_map 
        
def run_server(addr, port, proofreader, option_map):
    httpd = Server((addr, port), Handler, proofreader, option_map)
    httpd.serve_forever()

