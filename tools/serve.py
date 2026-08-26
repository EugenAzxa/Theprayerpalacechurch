#!/usr/bin/env python3
"""A local server that refuses to be cached.

`python3 -m http.server` sends Last-Modified and lets the browser decide, which
means an edit can land on disk, be served correctly, and still not reach the
tab that is open on it. This one says no-store on everything, so what you see is
always what is on disk.

    python3 tools/serve.py [port]        default 4173
"""
import http.server, os, socketserver, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4173


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"The Prayer Palace on http://localhost:{PORT}/  (serving {os.path.realpath(ROOT)})")
    httpd.serve_forever()
