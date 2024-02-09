import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs

# abre o arquivo index.html

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

# Método GET acessa o arquivo login.html por uma rota /login
    
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

# Função para verificar se o login e senha já existe
              
    def usuario_existente(self, login, senha):
        with open("dados_login.txt", "r") as file:
            for line in file:
                stored_login, stored_senha = line.strip().split(';')
                if login == stored_login:
                    print("Senha"+ senha)
                    return senha == stored_senha
        return False

# Método POST envia os dados do login para a página resposta.html através de uma rota /enviar_login
            
    def do_POST(self):
        if self.path == '/enviar_login':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            print("Dados do Formulário: ")
            print("Email: ", form_data.get('email', ['']) [0])
            print("Senha ", form_data.get('senha', ['']) [0])

# Confere se o usuario com o campo 'email' já existe
            
            login = form_data.get('email', ['']) [0]
            if self.usuario_existente(login):
                with open(os.path.join(os.getcwd(), 'usuario_existe.html'), 'r') as usuario_existe_file:
                    content = usuario_existe_file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                
            else:

# Dados login gravados em um arquivo txt 
            
                with open('dados_login.txt', 'a') as file:
                    login = form_data.get('email', ['']) [0]
                    senha = form_data.get('senha',[''])[0]
                    file.write(f"{login};{senha}\n")

# Página html que será carregada após o usuário enviar o login
                
                with open(os.path.join(os.getcwd(), 'resposta.html'), 'r') as resposta_file:
                    content = resposta_file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
        else:
            super(MyHandler, self).do_POST()    
    
endereco_ip = '0.0.0.0'
porta = 8000

with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor Iniciado em {endereco_ip}: {porta}")
    httpd.serve_forever()