
#
#   "emulation" of LT server
#

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys

addr = 'localhost'
port = 8081
stop = '/stop'

match = {
    'offset': 5,
    'length': 3,
    'message': 'Error',
    'rule': {'id': 'None'},
    'replacements': [{'value': 'is'}],
    'context': {
        'text': 'This isx a test. ',
        'offset': 5,
        'length': 3,
    },
}
message = {'matches': [match]}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(message).encode('ascii'))
        if self.path == stop:
            sys.exit()

httpd = HTTPServer((addr, port), Handler)
httpd.serve_forever()

