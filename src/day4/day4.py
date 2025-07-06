import http.server
import socketserver
import os

PORT = 8000

current_directory = os.getcwd()

print(f'Serving files from {current_directory}')
print(f'Server will be accessible at http://localhost:{PORT}')
print('Press Ctrl+C to stop the server')

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(('', PORT), Handler) as httpd:
    httpd.serve_forever()