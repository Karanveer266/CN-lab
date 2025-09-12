import http.server
import socketserver
import os
import hashlib
from datetime import datetime
import time

PORT = 8000
HOSTNAME = "localhost"
FILE_TO_SERVE = "index.html"

class CachingRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                self._handle_cached_file()
            else:
                super().do_GET()
        except ConnectionResetError:
            print(f"Client disconnected during request to {self.path}")
        except Exception as e:
            print(f"Error: {e}")
            try:
                self.send_error(500, 'Internal Server Error')
            except:
                pass  # Client already disconnected

    def _handle_cached_file(self):
        file_stat = os.stat(FILE_TO_SERVE)
        last_modified_time = file_stat.st_mtime
        last_modified_str = datetime.fromtimestamp(last_modified_time).strftime('%a, %d %b %Y %H:%M:%S GMT')

        with open(FILE_TO_SERVE, 'rb') as f:
            content = f.read()
            raw_etag = hashlib.md5(content).hexdigest()
            quoted_etag = f'"{raw_etag}"'

        client_etag = self.headers.get('If-None-Match')
        client_last_modified = self.headers.get('If-Modified-Since')

        # Debug logging
        print(f"Client ETag: {client_etag}")
        print(f"Server ETag: {quoted_etag}")

        if client_etag and client_etag == quoted_etag:
            self.send_response(304)
            self.end_headers()
            print("SUCCESS: Cache hit (ETag). Responded with 304 Not Modified.")
            return

        if client_last_modified:
            try:
                client_modified_time_dt = datetime.strptime(client_last_modified, '%a, %d %b %Y %H:%M:%S GMT')
                client_modified_time_ts = time.mktime(client_modified_time_dt.timetuple())
                
                if client_modified_time_ts >= last_modified_time:
                    self.send_response(304)
                    self.end_headers()
                    print("SUCCESS: Cache hit (Last-Modified). Responded with 304 Not Modified.")
                    return
            except ValueError:
                print("WARNING: Malformed If-Modified-Since header from client.")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(file_stat.st_size))
        self.send_header('Last-Modified', last_modified_str)
        self.send_header('ETag', quoted_etag)
        self.send_header('Cache-Control', 'private, max-age=3600')
        self.end_headers()
        self.wfile.write(content)
        print("Cache miss. Responded with 200 OK and new cache headers.")

    def log_message(self, format, *args):
        # Suppress some verbose logging
        pass

# Server setup with better error handling
with socketserver.TCPServer((HOSTNAME, PORT), CachingRequestHandler) as httpd:
    httpd.allow_reuse_address = True  # Helps prevent "Address already in use" errors
    print(f"Serving on http://{HOSTNAME}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopping.")
        httpd.shutdown()
