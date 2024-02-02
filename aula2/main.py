import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs


class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, 'index.html'), 'r')
            self.send_response(200)
            self.send_header('Content-type', "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close
            return None
        except FileNotFoundError:
            pass

        return super().list_directory(path)
    
    def do_GET(self):
        if self.path == '/login':
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header('Content-type', "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/enviar_login':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            print("Dados do Formulário: ")
            print("Email: ", form_data.get('email', ['']) [0])
            print("Senha ", form_data.get('senha', ['']) [0])

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("Dados recebidos com sucesso!".encode('utf-8'))
        else:
            super(MyHandler, self).do_POST()    
    
endereco_ip = '0.0.0.0'
porta = 8000

with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor Iniciado em {endereco_ip}: {porta}")
    httpd.serve_forever()