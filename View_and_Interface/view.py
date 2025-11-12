from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from html import escape
import sys
import os

# Adiciona o diretório pai ao path para importar controler e mocks
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from controler import controller
    import mock_catalogo
    import mock_usuarios
    CONTROLLER_AVAILABLE = True
except ImportError:
    CONTROLLER_AVAILABLE = False


def _esc(v):
    """Escapa valores HTML para evitar XSS"""
    return escape("" if v is None else str(v))


class BibliotecaView(BaseHTTPRequestHandler):
    """
    Servidor HTTP que controla todas as telas do SGBU via Python.
    Os alunos devem implementar as classes em Model/ e integrar via controler.py
    """

    def do_GET(self):
        """Trata requisicoes GET - exibe paginas"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Redireciona raiz para cadastro
        if path == '/':
            self.send_response(302)
            self.send_header("Location", "/cadastro")
            self.end_headers()
        
        # Modulo 1: Cadastro de Usuarios
        elif path == '/cadastro':
            self.render_cadastro()
        elif path == '/cadastro/novo':
            self.render_form_usuario()
        
        # Modulo 2: Catalogo de Livros
        elif path == '/livros':
            self.render_livros()
        elif path == '/livros/novo':
            self.render_form_livro()
        elif path == '/autores':
            self.render_autores()
        
        # Modulo 3: Emprestimos
        elif path == '/emprestimos':
            self.render_emprestimos()
        elif path == '/emprestimos/novo':
            self.render_form_emprestimo()
        elif path.startswith('/emprestimos/devolver/'):
            loan_id = int(path.split('/')[-1])
            self.processar_devolucao(loan_id)
        
        # Modulo 4: Relatorios
        elif path == '/relatorios':
            self.render_relatorios()
        
        else:
            self.send_error(404, "Pagina nao encontrada")

    def do_POST(self):
        """Trata requisicoes POST - processa formularios"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(body)
        
        # Converte para dict simples
        data = {k: v[0] if len(v) == 1 else v for k, v in params.items()}
        
        if path == '/cadastro/salvar':
            self.processar_usuario(data)
        elif path == '/livros/salvar':
            self.processar_livro(data)
        elif path == '/emprestimos/salvar':
            self.processar_emprestimo(data)
        elif path == '/emprestimos/devolver':
            # Espera loan_id como campo (pode vir múltiplos: loan_id=1&loan_id=2)
            loan_ids = []
            if 'loan_id' in data:
                # parse_qs já normalizou para strings simples no início
                # Se houver vírgula, aceita também formatos como "1,2"
                raw = data.get('loan_id')
                if isinstance(raw, list):
                    for v in raw:
                        for part in str(v).split(','):
                            part = part.strip()
                            if part:
                                try:
                                    loan_ids.append(int(part))
                                except ValueError:
                                    pass
                else:
                    for part in str(raw).split(','):
                        part = part.strip()
                        if part:
                            try:
                                loan_ids.append(int(part))
                            except ValueError:
                                pass
            self.processar_devolucoes(loan_ids)
        else:
            self.send_error(404)

    # ========== RENDERIZACAO - MODULO 1: USUARIOS ==========
    
    def render_cadastro(self):
        """Renderiza pagina de listagem de usuarios"""
        with open("View_and_Interface/cadastro.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        # TODO: Buscar usuarios via controler.py
        conteudo = """
            <div class="actions">
                <h2>Lista de Usuarios</h2>
                <a href="/cadastro/novo" class="btn btn-primary">+ Novo Usuario</a>
            </div>
            <div class="table-container">
                <div class="empty-state">
                    <h3>Funcionalidade nao implementada</h3>
                    <p>Os alunos devem implementar a classe <strong>Usuario</strong> em <code>Model/Usuario.py</code></p>
                    <p>e integrar via <code>controler.py</code> para listar usuarios aqui.</p>
                </div>
            </div>
        """
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_form_usuario(self):
        """Renderiza formulario de cadastro de usuario"""
        with open("View_and_Interface/cadastro.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="form-container">
                <h2>Novo Usuario</h2>
                <form action="/cadastro/salvar" method="post">
                    <div class="form-group">
                        <label>Matricula *</label>
                        <input type="text" name="matricula" required>
                    </div>
                    <div class="form-group">
                        <label>Nome Completo *</label>
                        <input type="text" name="nome" required>
                    </div>
                    <div class="form-group">
                        <label>Tipo de Usuario *</label>
                        <select name="tipo" required>
                            <option value="">Selecione...</option>
                            <option value="aluno">Aluno</option>
                            <option value="professor">Professor</option>
                            <option value="funcionario">Funcionario</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" name="email">
                    </div>
                    <div class="form-actions">
                        <a href="/cadastro" class="btn btn-secondary" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                        <button type="submit" class="btn btn-primary">Salvar</button>
                    </div>
                </form>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def processar_usuario(self, data):
        """Processa formulario de usuario (exibe dados mas nao salva)"""
        with open("View_and_Interface/cadastro.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        # TODO: Salvar via controler.py
        mensagem = f'''
            <div class="alert alert-success">
                Dados recebidos com sucesso!
            </div>
            <div class="alert alert-error">
                <strong>Funcionalidade nao implementada:</strong> Os alunos devem implementar
                a classe Usuario em Model/Usuario.py e integrar via controler.py
            </div>
            <div style="background: white; padding: 20px; border-radius: 12px;">
                <h3>Dados enviados:</h3>
                <p><strong>Matricula:</strong> {_esc(data.get('matricula'))}</p>
                <p><strong>Nome:</strong> {_esc(data.get('nome'))}</p>
                <p><strong>Tipo:</strong> {_esc(data.get('tipo'))}</p>
                <p><strong>Email:</strong> {_esc(data.get('email', 'Nao informado'))}</p>
            </div>
            <br>
            <a href="/cadastro" class="btn btn-primary">Voltar para lista</a>
        '''
        
        html = html.replace('<!--CONTEUDO-->', mensagem)
        self.send_html(html)

    # ========== RENDERIZACAO - MODULO 2: LIVROS ==========
    
    def render_livros(self):
        """Renderiza pagina de catalogo de livros"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="tabs">
                <a href="/livros" class="tab active">Livros</a>
                <a href="/autores" class="tab">Autores</a>
            </div>
            <div class="actions" style="justify-content: space-between; display: flex;">
                <h2>Catalogo de Livros</h2>
                <a href="/livros/novo" class="btn btn-primary">+ Novo Livro</a>
            </div>
            <div class="table-container">
                <div class="empty-state">
                    <h3>Funcionalidade nao implementada</h3>
                    <p>Os alunos devem implementar a classe <strong>Livro</strong> em <code>Model/Livro.py</code></p>
                    <p>e integrar via <code>controler.py</code> para listar livros aqui.</p>
                </div>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_autores(self):
        """Renderiza pagina de autores"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="tabs">
                <a href="/livros" class="tab">Livros</a>
                <a href="/autores" class="tab active">Autores</a>
            </div>
            <div class="actions" style="justify-content: space-between; display: flex;">
                <h2>Lista de Autores</h2>
                <a href="#" class="btn btn-primary">+ Novo Autor</a>
            </div>
            <div class="table-container">
                <div class="empty-state">
                    <h3>Funcionalidade nao implementada</h3>
                    <p>Os alunos devem implementar a classe <strong>Autor</strong> em <code>Model/Autor.py</code></p>
                    <p>e integrar via <code>controler.py</code> para listar autores aqui.</p>
                </div>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_form_livro(self):
        """Renderiza formulario de cadastro de livro"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="form-container">
                <h2>Novo Livro</h2>
                <form action="/livros/salvar" method="post">
                    <div class="form-group">
                        <label>ISBN *</label>
                        <input type="text" name="isbn" required>
                    </div>
                    <div class="form-group">
                        <label>Titulo *</label>
                        <input type="text" name="titulo" required>
                    </div>
                    <div class="form-group">
                        <label>Categoria *</label>
                        <select name="categoria" required>
                            <option value="">Selecione...</option>
                            <option value="Ficcao">Ficcao</option>
                            <option value="Tecnico">Tecnico</option>
                            <option value="Didatico">Didatico</option>
                            <option value="Cientifico">Cientifico</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Quantidade em Estoque *</label>
                        <input type="number" name="estoque" min="0" required>
                    </div>
                    <div class="form-actions">
                        <a href="/livros" class="btn btn-secondary" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                        <button type="submit" class="btn btn-primary">Salvar</button>
                    </div>
                </form>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def processar_livro(self, data):
        """Processa formulario de livro (exibe dados mas nao salva)"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        mensagem = f'''
            <div class="alert alert-success">
                Dados recebidos com sucesso!
            </div>
            <div class="alert alert-error">
                <strong>Funcionalidade nao implementada:</strong> Os alunos devem implementar
                a classe Livro em Model/Livro.py e integrar via controler.py
            </div>
            <div style="background: white; padding: 20px; border-radius: 12px;">
                <h3>Dados enviados:</h3>
                <p><strong>ISBN:</strong> {_esc(data.get('isbn'))}</p>
                <p><strong>Titulo:</strong> {_esc(data.get('titulo'))}</p>
                <p><strong>Categoria:</strong> {_esc(data.get('categoria'))}</p>
                <p><strong>Estoque:</strong> {_esc(data.get('estoque'))}</p>
            </div>
            <br>
            <a href="/livros" class="btn btn-primary">Voltar para catalogo</a>
        '''
        
        html = html.replace('<!--CONTEUDO-->', mensagem)
        self.send_html(html)

    # ========== RENDERIZACAO - MODULO 3: EMPRESTIMOS ==========
    
    def render_emprestimos(self):
        """Renderiza pagina de emprestimos"""
        with open("View_and_Interface/emprestimos.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        # Tenta buscar emprestimos via controller se disponível
        if CONTROLLER_AVAILABLE:
            try:
                emprestimos = controller.get_emprestimos()
                ativos = len([e for e in emprestimos if e['status'] == 'ACTIVE'])
                devolvidos = len([e for e in emprestimos if e['status'] == 'RETURNED'])
                total = len(emprestimos)
                
                # Monta tabela de emprestimos
                linhas_tabela = ""
                if emprestimos:
                    for emp in emprestimos:
                        status_badge = "🟢 ATIVO" if emp['status'] == "ACTIVE" else "🔵 DEVOLVIDO"
                        checkbox = ""
                        botao_devolver = ""
                        if emp['status'] == "ACTIVE":
                            # Checkbox para seleção em devolução em lote
                            checkbox = f'<input type="checkbox" name="loan_id" value="{emp["loanId"]}" />'
                            botao_devolver = f'<a href="/emprestimos/devolver/{emp["loanId"]}" class="btn btn-danger">Devolver</a>'
                        linhas_tabela += f"""
                        <tr>
                            <td style="width:48px; text-align: center;">{checkbox}</td>
                            <td>{emp['loanId']}</td>
                            <td>{emp['userId']}</td>
                            <td>{emp['bookId']}</td>
                            <td>{emp['loanDate'][:10]}</td>
                            <td>{emp['dueDate'][:10]}</td>
                            <td>{status_badge}</td>
                            <td style="text-align: center;">{botao_devolver}</td>
                        </tr>
                        """
                else:
                    linhas_tabela = "<tr><td colspan='8' style='text-align: center;'>Nenhum empréstimo registrado</td></tr>"
                
                # Formulário com possibilidade de devolução em lote
                conteudo = f'''
                    <div class="stats">
                        <div class="stat-card">
                            <h3>Emprestimos Ativos</h3>
                            <div class="value">{ativos}</div>
                        </div>
                        <div class="stat-card">
                            <h3>Emprestimos Devolvidos</h3>
                            <div class="value">{devolvidos}</div>
                        </div>
                        <div class="stat-card">
                            <h3>Total</h3>
                            <div class="value">{total}</div>
                        </div>
                    </div>
                    <div class="actions" style="justify-content: space-between; display: flex;">
                        <h2>Lista de Emprestimos</h2>
                        <a href="/emprestimos/novo" class="btn btn-primary">+ Novo Emprestimo</a>
                    </div>
                    <div class="table-container">
                        <form action="/emprestimos/devolver" method="post" id="devolverForm">
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="background-color: #f3f4f6; border-bottom: 2px solid #d1d5db;">
                                    <th style="padding: 12px; text-align: center; border: 1px solid #d1d5db; width:48px;">Sel</th>
                                    <th style="padding: 12px; text-align: left; border: 1px solid #d1d5db;">ID</th>
                                    <th style="padding: 12px; text-align: left; border: 1px solid #d1d5db;">Usuário ID</th>
                                    <th style="padding: 12px; text-align: left; border: 1px solid #d1d5db;">Livro ID</th>
                                    <th style="padding: 12px; text-align: left; border: 1px solid #d1d5db;">Empréstimo</th>
                                    <th style="padding: 12px; text-align: left; border: 1px solid #d1d5db;">Devolução</th>
                                    <th style="padding: 12px; text-align: left; border: 1px solid #d1d5db;">Status</th>
                                    <th style="padding: 12px; text-align: center; border: 1px solid #d1d5db;">Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {linhas_tabela}
                            </tbody>
                        </table>
                        <div style="padding:12px; display:flex; justify-content:flex-end; gap:8px;">
                            <a href="/emprestimos" class="btn btn-secondary">Cancelar</a>
                            <button type="submit" class="btn btn-primary" onclick="return confirm('Confirma devolver os empréstimos selecionados?')">Devolver selecionados</button>
                        </div>
                        </form>
                    </div>
                '''
            except Exception as e:
                conteudo = f'''
                    <div class="alert alert-error">
                        Erro ao buscar empréstimos: {str(e)}
                    </div>
                    <div class="actions" style="justify-content: space-between; display: flex;">
                        <h2>Lista de Emprestimos</h2>
                        <a href="/emprestimos/novo" class="btn btn-primary">+ Novo Emprestimo</a>
                    </div>
                    <div class="table-container">
                        <div class="empty-state">
                            <h3>Funcionalidade parcialmente implementada</h3>
                            <p>Certifique-se de que todos os módulos estão configurados corretamente.</p>
                        </div>
                    </div>
                '''
        else:
            conteudo = '''
                <div class="stats">
                    <div class="stat-card">
                        <h3>Emprestimos Ativos</h3>
                        <div class="value">?</div>
                    </div>
                    <div class="stat-card">
                        <h3>Emprestimos em Atraso</h3>
                        <div class="value">?</div>
                    </div>
                    <div class="stat-card">
                        <h3>Devolvidos Hoje</h3>
                        <div class="value">?</div>
                    </div>
                </div>
                <div class="actions" style="justify-content: space-between; display: flex;">
                    <h2>Lista de Emprestimos</h2>
                    <a href="/emprestimos/novo" class="btn btn-primary">+ Novo Emprestimo</a>
                </div>
                <div class="table-container">
                    <div class="empty-state">
                        <h3>Funcionalidade nao implementada</h3>
                        <p>Os alunos devem implementar a classe <strong>Emprestimo</strong> em <code>Model/Emprestimo.py</code></p>
                        <p>e integrar via <code>controler.py</code> para listar emprestimos aqui.</p>
                        <p><strong>Nota:</strong> Este modulo depende de Usuario e Livro implementados!</p>
                    </div>
                </div>
            '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_form_emprestimo(self):
        """Renderiza formulario de novo emprestimo"""
        with open("View_and_Interface/emprestimos.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        opcoes_usuarios = ""
        opcoes_livros = ""
        
        # Tenta buscar usuarios e livros via mocks se disponível
        if CONTROLLER_AVAILABLE:
            try:
                usuarios = mock_usuarios.listar_usuarios()
                for usuario in usuarios:
                    opcoes_usuarios += f'<option value="{usuario["userId"]}">{usuario["userId"]} - {usuario["nome"]} ({usuario["tipo"]})</option>'
                
                livros = mock_catalogo.listar_livros_disponiveis()
                for livro in livros:
                    opcoes_livros += f'<option value="{livro["bookId"]}">{livro["bookId"]} - {livro["titulo"]}</option>'
            except Exception as e:
                opcoes_usuarios = f'<option value="">Erro ao carregar usuários: {str(e)}</option>'
                opcoes_livros = f'<option value="">Erro ao carregar livros: {str(e)}</option>'
        
        if not opcoes_usuarios:
            opcoes_usuarios = '<option value="">Nenhum usuário disponível</option>'
        if not opcoes_livros:
            opcoes_livros = '<option value="">Nenhum livro disponível</option>'
        
        conteudo = f'''
            <div class="form-container">
                <h2>Novo Emprestimo</h2>
                <form action="/emprestimos/salvar" method="post">
                    <div class="form-group">
                        <label>Usuario *</label>
                        <select name="user_id" required>
                            <option value="">Selecione um usuario...</option>
                            {opcoes_usuarios}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Livro Disponivel *</label>
                        <select name="book_id" required>
                            <option value="">Selecione um livro...</option>
                            {opcoes_livros}
                        </select>
                    </div>
                    <div class="form-actions">
                        <a href="/emprestimos" class="btn btn-secondary" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                        <button type="submit" class="btn btn-primary">Registrar Emprestimo</button>
                    </div>
                </form>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def processar_emprestimo(self, data):
        """Processa formulario de emprestimo via controller"""
        with open("View_and_Interface/emprestimos.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        user_id = int(data.get('user_id', 0)) if data.get('user_id') else 0
        book_id = int(data.get('book_id', 0)) if data.get('book_id') else 0
        
        if not user_id or not book_id:
            mensagem = '''
                <div class="alert alert-error">
                    <strong>Erro:</strong> Usuario e Livro são obrigatórios!
                </div>
                <br>
                <a href="/emprestimos/novo" class="btn btn-primary">Voltar ao formulário</a>
            '''
        elif CONTROLLER_AVAILABLE:
            try:
                # Tenta registrar o emprestimo via controller
                resultado = controller.registrar_emprestimo(user_id=user_id, book_id=book_id)
                
                if resultado.get("sucesso"):
                    loan = resultado["loan"]
                    mensagem = f'''
                        <div class="alert alert-success">
                            ✅ Empréstimo registrado com sucesso!
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 12px;">
                            <h3>Detalhes do Empréstimo:</h3>
                            <p><strong>ID do Empréstimo:</strong> {loan['loanId']}</p>
                            <p><strong>Usuário ID:</strong> {loan['userId']}</p>
                            <p><strong>Livro ID:</strong> {loan['bookId']}</p>
                            <p><strong>Data de Empréstimo:</strong> {loan['loanDate'][:10]}</p>
                            <p><strong>Data de Devolução Prevista:</strong> {loan['dueDate'][:10]}</p>
                            <p><strong>Status:</strong> {loan['status']}</p>
                        </div>
                        <br>
                        <a href="/emprestimos" class="btn btn-primary">Voltar para lista</a>
                    '''
                else:
                    erro = resultado.get("erro", "Erro desconhecido")
                    mensagem = f'''
                        <div class="alert alert-error">
                            <strong>❌ Erro ao registrar empréstimo:</strong> {erro}
                        </div>
                        <br>
                        <a href="/emprestimos/novo" class="btn btn-primary">Tentar novamente</a>
                    '''
            except Exception as e:
                mensagem = f'''
                    <div class="alert alert-error">
                        <strong>Erro ao processar:</strong> {str(e)}
                    </div>
                    <br>
                    <a href="/emprestimos/novo" class="btn btn-primary">Voltar ao formulário</a>
                '''
        else:
            mensagem = f'''
                <div class="alert alert-success">
                    Dados recebidos com sucesso!
                </div>
                <div class="alert alert-error">
                    <strong>Funcionalidade nao implementada:</strong> Os alunos devem implementar
                    a classe Emprestimo em Model/Emprestimo.py e integrar via controler.py
                </div>
                <div style="background: white; padding: 20px; border-radius: 12px;">
                    <h3>Dados enviados:</h3>
                    <p><strong>Usuario ID:</strong> {_esc(user_id)}</p>
                    <p><strong>Livro ID:</strong> {_esc(book_id)}</p>
                </div>
                <br>
                <a href="/emprestimos" class="btn btn-primary">Voltar para lista</a>
            '''
        
        html = html.replace('<!--CONTEUDO-->', mensagem)
        self.send_html(html)

    def processar_devolucao(self, loan_id):
        """Processa devolução de um empréstimo via controller"""
        with open("View_and_Interface/emprestimos.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        if not loan_id:
            mensagem = '''
                <div class="alert alert-error">
                    <strong>Erro:</strong> ID do empréstimo inválido!
                </div>
                <br>
                <a href="/emprestimos" class="btn btn-primary">Voltar para lista</a>
            '''
        elif CONTROLLER_AVAILABLE:
            try:
                # Tenta registrar a devolução via controller
                resultado = controller.registrar_devolucao(loan_id=loan_id)
                
                if resultado.get("sucesso"):
                    mensagem = f'''
                        <div class="alert alert-success">
                            ✅ Livro devolvido com sucesso!
                        </div>
                        <div style="background: white; padding: 20px; border-radius: 12px;">
                            <h3>Detalhes da Devolução:</h3>
                            <p><strong>ID do Empréstimo:</strong> {loan_id}</p>
                            <p><strong>Status:</strong> {resultado.get("status", "RETURNED")}</p>
                            <p><strong>Mensagem:</strong> {resultado.get("mensagem", "Devolução registrada com sucesso")}</p>
                        </div>
                        <br>
                        <a href="/emprestimos" class="btn btn-primary">Voltar para lista</a>
                    '''
                else:
                    erro = resultado.get("erro", "Erro desconhecido")
                    mensagem = f'''
                        <div class="alert alert-error">
                            <strong>❌ Erro ao devolver livro:</strong> {erro}
                        </div>
                        <br>
                        <a href="/emprestimos" class="btn btn-primary">Voltar para lista</a>
                    '''
            except Exception as e:
                mensagem = f'''
                    <div class="alert alert-error">
                        <strong>Erro ao processar devolução:</strong> {str(e)}
                    </div>
                    <br>
                    <a href="/emprestimos" class="btn btn-primary">Voltar para lista</a>
                '''
        else:
            mensagem = f'''
                <div class="alert alert-success">
                    Devolução de empréstimo ID: {loan_id}
                </div>
                <div class="alert alert-error">
                    <strong>Funcionalidade nao implementada:</strong> Os alunos devem implementar
                    a classe Emprestimo em Model/Emprestimo.py e integrar via controler.py
                </div>
                <br>
                <a href="/emprestimos" class="btn btn-primary">Voltar para lista</a>
            '''
        
        html = html.replace('<!--CONTEUDO-->', mensagem)
        self.send_html(html)

    def processar_devolucoes(self, loan_ids):
        """Processa devolução de múltiplos empréstimos via controller (POST)."""
        with open("View_and_Interface/emprestimos.html", "r", encoding="utf-8") as f:
            html = f.read()

        if not loan_ids:
            mensagem = '''
                <div class="alert alert-error">
                    <strong>Erro:</strong> Nenhum empréstimo selecionado para devolução!
                </div>
                <br>
                <a href="/emprestimos" class="btn btn-primary">Voltar para lista</a>
            '''
            html = html.replace('<!--CONTEUDO-->', mensagem)
            self.send_html(html)
            return

        results = []
        if CONTROLLER_AVAILABLE:
            for lid in loan_ids:
                try:
                    res = controller.registrar_devolucao(loan_id=lid)
                    if res.get('sucesso'):
                        results.append((lid, True, None))
                    else:
                        results.append((lid, False, res.get('erro')))
                except Exception as e:
                    results.append((lid, False, str(e)))
        else:
            for lid in loan_ids:
                results.append((lid, False, 'Controller não disponível'))

        # Monta mensagem resumida
        sucesso = [r for r in results if r[1]]
        falhas = [r for r in results if not r[1]]

        mensagem = ''
        if sucesso:
            mensagem += f"<div class=\"alert alert-success\">✅ {len(sucesso)} empréstimo(s) devolvido(s) com sucesso.</div>"
        if falhas:
            mensagem += '<div class="alert alert-error"><strong>Erros:</strong><ul>'
            for fid, ok, err in falhas:
                mensagem += f'<li>ID {fid}: {escape(str(err))}</li>'
            mensagem += '</ul></div>'

        mensagem += '<br><a href="/emprestimos" class="btn btn-primary">Voltar para lista</a>'

        html = html.replace('<!--CONTEUDO-->', mensagem)
        self.send_html(html)

    # ========== RENDERIZACAO - MODULO 4: RELATORIOS ==========
    
    def render_relatorios(self):
        """Renderiza pagina de relatorios"""
        with open("View_and_Interface/relatorios.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="report-cards">
                <div class="report-card">
                    <div class="icon">Stats</div>
                    <h3>Visao Geral</h3>
                    <p>Dashboard com estatisticas gerais</p>
                </div>
                <div class="report-card">
                    <div class="icon">Books</div>
                    <h3>Livros Mais Emprestados</h3>
                    <p>Ranking de popularidade</p>
                </div>
                <div class="report-card">
                    <div class="icon">Users</div>
                    <h3>Usuarios Mais Ativos</h3>
                    <p>Top usuarios por emprestimos</p>
                </div>
                <div class="report-card">
                    <div class="icon">Chart</div>
                    <h3>Taxa de Ocupacao</h3>
                    <p>Percentual de livros emprestados</p>
                </div>
            </div>
            <div class="empty-state">
                <h3>Funcionalidade nao implementada</h3>
                <p>Os alunos devem implementar a classe <strong>Relatorio</strong> em <code>Model/Relatorio.py</code></p>
                <p>e integrar via <code>controler.py</code> para gerar relatorios.</p>
                <p><strong>Nota:</strong> Este modulo depende de TODOS os outros modulos!</p>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)

    # ========== METODOS AUXILIARES ==========
    
    def send_html(self, html):
        """Envia resposta HTML"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def log_message(self, format, *args):
        """Log das requisicoes HTTP"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8000):
    """Inicia o servidor HTTP na porta especificada"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, BibliotecaView)
    print(f"Servidor SGBU iniciado em http://localhost:{port}")
    print(f"Acesse: http://localhost:{port}/cadastro")
    print(f"Pressione Ctrl+C para encerrar")
    print()
    print("ATENCAO: As funcionalidades de CRUD ainda nao estao implementadas.")
    print("   Os alunos devem implementar as classes em Model/ usando TDD.")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
