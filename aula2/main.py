import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs, urlparse

# abre o arquivo index.html

class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, 'index.html'), 'r')
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
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
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File not found")
                
        elif self.path == '/login_failed':
             
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
            mensagem = "Login e/ou senha incorreta. Tente novamente"

            content = content.replace('<!-- ERRO -->',
                                       f'<div class="error-message"><p>{mensagem}</p></div>')
            self.wfile.write(content.encode('utf-8'))
        
        elif self.path.startswith('/cadastro'):

            query_params = parse_qs(urlparse(self.path).query)

            login = query_params.get('email', [''])[0]
            senha = query_params.get('senha', [''])[0]


            welcome_message = f"Olá {login}, seja bem-vindo.Complete seu cadastro"

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r', encoding='utf-8') as cadastro_file:
                content = cadastro_file.read()

            content = content.replace('{login}', login)
            content = content.replace('{senha}', senha)
            content = content.replace('{welcome_message}', welcome_message)

            self.wfile.write(content.encode('utf-8'))

            return
            
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

# Confere se o usuario com o campo 'email' e 'senha' já existe
            
            login = form_data.get('email', ['']) [0]
            senha = form_data.get('senha', ['']) [0]

            if self.usuario_existente(login, senha):
                with open(os.path.join(os.getcwd(), 'usuario_existe.html'), 'r') as usuario_existe_file:
                    content = usuario_existe_file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                
            else:
                if any(line.startswith(f"{login};") for line in open('dados_login.txt', 'r', encoding='utf-8')):
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    return
                
                else:

# Dados login gravados em um arquivo txt 
            
                    with open('dados_login.txt', 'a') as file:
                        login = form_data.get('email', ['']) [0]
                        senha = form_data.get('senha',[''])[0]
                        file.write(f"{login};{senha}\n")

                    self.send_response(302)
                    self.send_header("Location", f"/cadastro?email={login}&senha={senha}")
                    self.end_headers()
                    # self.wfile.write(content.encode('utf-8'))

                    return

# Página html que será carregada após o usuário enviar o login
                    
                    # with open(os.path.join(os.getcwd(), 'resposta.html'), 'r') as resposta_file:
                    #     content = resposta_file.read()

        else:
            super(MyHandler, self).do_POST()    
    
endereco_ip = '0.0.0.0'
porta = 8000

with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor Iniciado em {endereco_ip}: {porta}")
    httpd.serve_forever()