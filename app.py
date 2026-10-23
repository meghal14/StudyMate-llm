"""Run with python app.py, then visit http://127.0.0.1:8000."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from llm import ModelError, generate, status

STATIC = Path(__file__).resolve().parent / 'static'
FILES = {'/': ('index.html', 'text/html'), '/style.css': ('style.css', 'text/css'),
         '/script.js': ('script.js', 'text/javascript')}

class Handler(BaseHTTPRequestHandler):
    def reply(self, code, body, content_type='application/json'):
        if content_type == 'application/json':
            body = json.dumps(body).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', content_type + '; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/api/status':
            try:
                self.reply(200, status())
            except ModelError as exc:
                self.reply(503, {'ready': False, 'message': str(exc)})
        elif path in FILES:
            filename, kind = FILES[path]
            self.reply(200, (STATIC / filename).read_bytes(), kind)
        else:
            self.reply(404, {'error': 'Not found'})

    def do_POST(self):
        if self.path != '/api/generate':
            return self.reply(404, {'error': 'Not found'})
        origin = self.headers.get('Origin')
        allowed = {f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}'}
        if origin and origin not in allowed:
            return self.reply(403, {'error': 'Use the local StudyMate page.'})
        if self.headers.get_content_type() != 'application/json':
            return self.reply(415, {'error': 'Send application/json.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 8192:
                return self.reply(413, {'error': 'Request is empty or too large.'})
            data = json.loads(self.rfile.read(length))
            self.reply(200, generate(data))
        except (ValueError, UnicodeError) as exc:
            self.reply(400, {'error': str(exc)})
        except ModelError as exc:
            self.reply(503, {'error': str(exc)})

    def log_message(self, *_):
        pass  # Do not log study questions or answers.


def main():
    parser = argparse.ArgumentParser(description='StudyMate local study assistant')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    with ThreadingHTTPServer(('127.0.0.1', args.port), Handler) as server:
        print(f'StudyMate is running at http://127.0.0.1:{args.port} (Ctrl+C to stop)')
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nGoodbye!')

if __name__ == '__main__':
    main()
