'''

Description: Simple HTTP server that listens for POST requests and saves the JSON data to a file.
Projet : unsecured-web-server
@author: azim
@copyright:  2025 LORIA/Université de Lorraine. All rights reserved.
@license: GNU General Public License, Version 3
@version: 1.0
@email:  azim.roussanaly@loria.fr
@date: 28/04/2025
'''
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import uuid

SAVE_FOLDER = "./data"
os.makedirs(SAVE_FOLDER, exist_ok=True)
PORT = int(os.getenv("PORT", 80))

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        filename = f"{uuid.uuid4()}.json"
        filepath = os.path.join(SAVE_FOLDER, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"Saved to {filename}".encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Use POST with JSON data.")

def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Listening on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
