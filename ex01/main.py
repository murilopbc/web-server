from http.server import SimpleHTTPRequestHandler, HTTPServer

port = 8000

handler = SimpleHTTPRequestHandler

server = HTTPServer(('localhost', port), handler)

print(f"Servidor está rodando em http://localhost:{port}")

server.serve_forever()