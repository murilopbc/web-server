import os
from http.server import SimpleHTTPRequestHandler
import socketserver

class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, 'login.html'), 'r')
            self.send_response(200)
            self.send_header('Content-type', "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close
            return None
        except FileNotFoundError:
            pass

        return super().list_directory(path)
    
endereco_ip = '0.0.0.0'
porta = 8000

with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor Iniciado em {endereco_ip}: {porta}")
    httpd.serve_forever()
