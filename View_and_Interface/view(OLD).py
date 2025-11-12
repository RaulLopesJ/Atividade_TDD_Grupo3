from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import controler as ctl
from html import escape

def _esc(v):
    return escape("" if v is None else str(v))

controller = ctl.Controller()

class BibliotecaController(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/menu")
            self.end_headers()

        elif self.path == "/menu":
            with open("View_and_Interface/index.html", "rb") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo)

        elif self.path == "/listar_emprestimos":
            emprestimos = controller.get_emprestimos()
            resposta = ""
            for emp in emprestimos:
                loan_date = emp.get('loanDate', '').split('T')[0]  # Pega só a data
                status_class = 'status-' + emp.get('status', '').lower()
                resposta += f'''
                    <div class="emprestimo-item {status_class}">
                        <span class="loan-id">ID: {_esc(emp.get('loanId'))}</span>
                        <span class="user-id">Usuário: {_esc(emp.get('userId'))}</span>
                        <span class="book-id">Livro: {_esc(emp.get('bookId'))}</span>
                        <span class="date">Data: {_esc(loan_date)}</span>
                        <span class="status">Status: {_esc(emp.get('status'))}</span>
                    </div>
                '''
            
            with open("View_and_Interface/index.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = conteudo.replace("<!--EMPRESTIMOS-->", resposta)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path.startswith("/verificar_livro/"):
            book_id = int(self.path.split("/")[-1])
            resultado = controller.verificar_disponibilidade(book_id)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resultado).encode("utf-8"))

    def do_POST(self):
        if self.path == "/registrar_emprestimo":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            try:
                user_id = int(params.get("userId", [""])[0])
                book_id = int(params.get("bookId", [""])[0])

                resultado = controller.registrar_emprestimo(user_id, book_id)
                
                if resultado.get("sucesso"):
                    emprestimo = resultado.get("loan", {})
                    item_formatado = f'''
                        <div class="resultado-emprestimo">
                            <h2>Empréstimo Registrado com Sucesso!</h2>
                            <p><span class="label">ID do Empréstimo:</span> {_esc(emprestimo.get('loanId'))}</p>
                            <p><span class="label">Usuário:</span> {_esc(emprestimo.get('userId'))}</p>
                            <p><span class="label">Livro:</span> {_esc(emprestimo.get('bookId'))}</p>
                            <p><span class="label">Data:</span> {_esc(emprestimo.get('loanDate').split('T')[0])}</p>
                            <p><span class="label">Devolução Prevista:</span> {_esc(emprestimo.get('dueDate').split('T')[0])}</p>
                        </div>
                    '''
                else:
                    item_formatado = f'''
                        <div class="erro-emprestimo">
                            <h2>Erro ao Registrar Empréstimo</h2>
                            <p class="erro">{_esc(resultado.get('erro'))}</p>
                        </div>
                    '''

                with open("View_and_Interface/index.html", "r", encoding="utf-8") as f:
                    conteudo = f.read()
                conteudo = conteudo.replace("<!--RESULTADO-->", item_formatado)
                
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(conteudo.encode("utf-8"))

            except ValueError as e:
                self.send_error(400, f"Dados inválidos: {str(e)}")

        elif self.path == "/registrar_devolucao":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            try:
                loan_id = int(params.get("loanId", [""])[0])
                resultado = controller.registrar_devolucao(loan_id)

                if resultado.get("sucesso"):
                    emprestimo = resultado.get("loan", {})
                    item_formatado = f'''
                        <div class="resultado-devolucao">
                            <h2>Devolução Registrada com Sucesso!</h2>
                            <p><span class="label">ID do Empréstimo:</span> {_esc(emprestimo.get('loanId'))}</p>
                            <p><span class="label">Data de Devolução:</span> {_esc(emprestimo.get('returnDate').split('T')[0])}</p>
                            <p><span class="label">Status:</span> {_esc(emprestimo.get('status'))}</p>
                        </div>
                    '''
                else:
                    item_formatado = f'''
                        <div class="erro-devolucao">
                            <h2>Erro ao Registrar Devolução</h2>
                            <p class="erro">{_esc(resultado.get('erro'))}</p>
                        </div>
                    '''

                with open("View_and_Interface/index.html", "r", encoding="utf-8") as f:
                    conteudo = f.read()
                conteudo = conteudo.replace("<!--RESULTADO-->", item_formatado)
                
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(conteudo.encode("utf-8"))

            except ValueError as e:
                self.send_error(400, f"Dados inválidos: {str(e)}")

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, BibliotecaController)
    print(f"Servidor iniciado na porta {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()