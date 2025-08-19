# pi0system/api.py    
"""  
HTTP API for pi0system using built-in server.  
"""  
  
from http.server import BaseHTTPRequestHandler, HTTPServer  
import json  
  
from .core import PI0Kernel  
from .security import USSManager, D12S12Mask  
  
# initialize singletons  
kernel = PI0Kernel()  
uss = USSManager(master_key=b'secretkey123456')  
# precompute 12 slates for example  
slate = uss.salt('init')  
masker = D12S12Mask([uss.slate(slate, d) for d in range(12)])  
  
class RequestHandler(BaseHTTPRequestHandler):  
    def _send_json(self, obj, status=200):  
        self.send_response(status)  
        self.send_header('Content-Type', 'application/json')  
        self.end_headers()  
        self.wfile.write(json.dumps(obj).encode())  
  
    def do_POST(self):  
        length = int(self.headers.get('Content-Length'))  
        body = self.rfile.read(length)  
        data = json.loads(body)  
  
        if self.path == '/apply_operator':  
            name = data.get('operator_name')  
            state = bytes.fromhex(data.get('state'))  
            params = data.get('params', {})  
            try:  
                new_state = kernel.apply_operator(name, state, **params)  
                self._send_json({'new_state': new_state.hex()})  
            except KeyError as e:  
                self._send_json({'error': str(e)}, status=404)  
        else:  
            self._send_json({'error': 'unknown_endpoint'}, status=404)  
  
def run_server(port=8000):  
    server = HTTPServer(('0.0.0.0', port), RequestHandler)  
    print('Server running on port', port)  
    server.serve_forever()  
  
if __name__ == '__main__':  
    run_server()  