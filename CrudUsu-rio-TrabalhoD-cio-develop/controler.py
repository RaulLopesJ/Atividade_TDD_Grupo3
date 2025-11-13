from dataclasses import dataclass, asdict, replace
from typing import Dict, List, Optional
from Model import Usuario as u
from Model import Livro as l
from Model import Relatorio as r
from Model import Emprestimo as e
from collections import Counter, defaultdict
import re
from datetime import datetime, timedelta
from enum import Enum
import json

class Controler:
    """
    Classe controladora que integra todos os módulos
    
    """

    pass


class UsuarioController:
    """
    Controller em memória para CRUD de Usuário.
    A lista é pré-populada com 3 usuários ao primeiro uso.
    """

    _usuarios: List[u.Usuario] = []

    def __init__(self, usuarios: List[u.Usuario] = None):
        # popula apenas uma vez
        if not self._usuarios and usuarios is None:
            self._seed()
        else:
            self._usuarios = usuarios or []


    def _seed(self):
        self._usuarios = [
            u.Usuario(
                id=1,
                nome="Joao",
                matricula="ESOFT",
                tipo="ALUNO",
                email="jp@fromTheSouth",
                ativoDeRegistro="2025-01-15T10:30:00Z",
                status="ATIVO",
            ),
            u.Usuario(
                id=2,
                nome="Ana",
                matricula="ABC123",
                tipo="ALUNO",
                email="ana@domain",
                ativoDeRegistro="2025-01-15T10:30:00Z",
                status="INATIVO",
            ),
            u.Usuario(
                id=3,
                nome="Jose",
                matricula="PSICO",
                tipo="PROFESSOR",
                email="jose@domain",
                ativoDeRegistro="2025-01-15T10:30:00Z",
                status="SUSPENSO",
            ),
        ]

    def listar(self) -> List[u.Usuario]:
        return self._usuarios if self._usuarios and len(self._usuarios) > 0 else []

    def obter_por_id(self, usuario_id: int) -> u.Usuario:
        u = next((x for x in self._usuarios if x.id == usuario_id), None)
        return u if u else None

    def criar(self, dados: dict) -> u.Usuario:
        # validações

        # campos obrigatórios
        required = ["nome", "email", "matricula", "tipo", "status", "ativoDeRegistro"]
        for field in required:
            if field not in dados or dados[field] is None:
                raise ValueError(f"Campo obrigatório ausente: {field}")

        # nome: 1-100 caracteres
        nome = str(dados["nome"]).strip()
        if not (1 <= len(nome) <= 100):
            raise ValueError("Nome deve ter entre 1 e 100 caracteres")

        # email: formato básico e único (case-insensitive)
        email = str(dados["email"]).strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise ValueError("Email inválido")
        if any((usr.email or "").lower() == email.lower() for usr in self._usuarios):
            raise ValueError("Email já cadastrado")

        # matricula: alfanumérica 5-20 e única (case-insensitive)
        matricula = str(dados["matricula"]).strip()
        if not (5 <= len(matricula) and len(matricula) <= 20):
            raise ValueError("Matrícula deve ser alfanumérica com 5 a 20 caracteres")
        if any((usr.matricula or "").lower() == matricula.lower() for usr in self._usuarios):
            raise ValueError("Matrícula já cadastrada")

        # tipo e status: devem existir nos enums em Model.Usuario (se os enums estiverem definidos)
        tipo_val = str(dados["tipo"]).strip()
        status_val = str(dados["status"]).strip()

        # validação flexível: se existem enums u.Tipo / u.Status, validamos contra eles; caso contrário, exigimos string não vazia
        def _validate_enum_or_nonempty(enum_cls, value, name):
            if hasattr(u, enum_cls):
                enum_type = getattr(u, enum_cls)
                try:
                    if isinstance(enum_type, type) and issubclass(enum_type, Enum):
                        valid_names = {e.name for e in enum_type}
                        valid_values = {str(e.value) for e in enum_type}
                        if value not in valid_names and value not in valid_values:
                            raise ValueError(f"{name} inválido; valores válidos: {sorted(valid_names | valid_values)}")
                        return
                except TypeError:
                    # enum_cls exists but is not a subclass of Enum -> fallthrough to non-empty check
                    pass
            if not value:
                raise ValueError(f"{name} inválido")

        _validate_enum_or_nonempty("Tipo", tipo_val, "Tipo")
        _validate_enum_or_nonempty("Status", status_val, "Status")

        # ativoDeRegistro: aceitar ISO 8601 com Z ou com offset ou sem timezone (validação simples)
        ativo = str(dados["ativoDeRegistro"]).strip()
        iso_parsed = False
        for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
            try:
                datetime.strptime(ativo, fmt)
                iso_parsed = True
                break
            except Exception:
                continue
        if not iso_parsed:
            raise ValueError("ativoDeRegistro deve estar em formato ISO 8601 (ex: 2025-01-15T10:30:00Z)")

        # criar id
        next_id = max((usr.id for usr in self._usuarios), default=0) + 1
        usuario = u.Usuario(
            id=dados.get("id", next_id),
            nome=nome,
            matricula=matricula,
            tipo=tipo_val,
            email=email,
            ativoDeRegistro=ativo,
            status=status_val,
        )
        self._usuarios.append(usuario)
        return usuario

    def atualizar(self, usuario_id: int, dados: dict) -> bool:
        # Validação do ID
        if not isinstance(usuario_id, int) or usuario_id <= 0:
            raise ValueError("ID deve ser um número inteiro positivo")

        # Validação dos dados
        if not dados:
            raise ValueError("Dados de atualização não podem estar vazios")

        usuario = next((u for u in self._usuarios if u.id == usuario_id), None)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        # Validações dos campos
        if "nome" in dados:
            nome = str(dados["nome"]).strip()
            if not (1 <= len(nome) <= 100):
                raise ValueError("Nome deve ter entre 1 e 100 caracteres")

        if "ativoDeRegistro" in dados:
            raise ValueError("Data de registro não pode ser alterada")

        if "id" in dados:
            raise ValueError("ID não pode ser alterado")

        if "matricula" in dados:
            matricula = str(dados["matricula"]).strip()
            if not (5 <= len(matricula) <= 20):
                raise ValueError("Matrícula deve ter entre 5 e 20 caracteres alfanuméricos")
            if not matricula.isalnum():
                raise ValueError("Matrícula deve conter apenas caracteres alfanuméricos")
            # Verificar duplicata de matrícula
            if any((u.matricula or "").lower() == matricula.lower() for u in self._usuarios if u.id != usuario_id):
                raise ValueError("Matrícula já está em uso")

        if "email" in dados and dados["email"] is not None and dados["email"] != "":
            email = str(dados["email"]).strip()
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                raise ValueError("Email deve ter formato válido")
            # Verificar duplicata de email
            if any((u.email or "").lower() == email.lower() for u in self._usuarios if u.id != usuario_id):
                raise ValueError("Email já está em uso")

        if "tipo" in dados:
            tipo = str(dados["tipo"]).strip().upper()
            tipos_validos = ["ALUNO", "PROFESSOR", "FUNCIONARIO"]
            if tipo not in tipos_validos:
                raise ValueError("Tipo deve ser ALUNO, PROFESSOR ou FUNCIONARIO")

        if "status" in dados:
            status = str(dados["status"]).strip().upper()
            status_validos = ["ATIVO", "INATIVO", "SUSPENSO"]
            if status not in status_validos:
                raise ValueError("Status deve ser ATIVO, INATIVO ou SUSPENSO")

        # Atualizar os campos
        idx = self._usuarios.index(usuario)
        atualizado = usuario.replace(
            nome=dados.get("nome", usuario.nome),
            matricula=dados.get("matricula", usuario.matricula),
            tipo=dados.get("tipo", usuario.tipo),
            email=dados.get("email", usuario.email),
            status=dados.get("status", usuario.status)
        )
        self._usuarios[idx] = atualizado
        return True

    def deletar(self, usuario_id: int) -> bool:
        for idx, u in enumerate(self._usuarios):
            print(f"Checking user with ID: {u.id} against target ID: {usuario_id}")
            if u.id == usuario_id:
                del self._usuarios[idx]
                return True
        return False

    # utilitários
    def buscar_por_matricula(self, matricula: str) -> List[u.Usuario]:
        """Busca por matrícula usando regex (case-insensitive, permite busca por pedaço).
        Se o padrão informado for inválido como regex, faz escape e busca literal.
        """
        if not matricula:
            return []
        try:
            pattern = re.compile(matricula, re.IGNORECASE)
        except re.error:
            pattern = re.compile(re.escape(matricula), re.IGNORECASE)
        return [usr for usr in self._usuarios if usr.matricula and pattern.search(usr.matricula)]


    def buscar_por_tipo(self, tipo: str) -> List[u.Usuario]:
        if tipo is None:
            return []
        input_tipo = str(tipo).upper()

        return [usr for usr in self._usuarios if usr.get_tipo().upper() == input_tipo.upper()]

    def buscar_por_nome(self, nome: str) -> List[u.Usuario]:
        """Busca por nome usando regex (case-insensitive, permite busca por pedaço da palavra).
        Se o padrão informado for inválido como regex, faz escape e busca literal.
        """
        if not nome or nome.strip() == "":
            return []
        try:
            pattern = re.compile(nome, re.IGNORECASE)
        except re.error:
            pattern = re.compile(re.escape(nome), re.IGNORECASE)
        return [usr for usr in self._usuarios if usr.get_nome() and pattern.search(usr.get_nome())]

    def contar(self) -> int:
        return len(self._usuarios)

def _esc(valor: str) -> str:
    """
    Escapa HTML para prevenir ataques XSS.
    
    Args:
        valor: String a ser escapada
        
    Returns:
        String com caracteres HTML escapados
    """
    return escape("" if valor is None else str(valor))


class LivroController:

    _db_livros: List[l.Livro] = []

    def __init__(self, livros: List[l.Livro] = None):
        # popula apenas uma vez
        if not self._db_livros and livros is None:
            self._seed()
        else:
            self._db_livros = livros or []


    def _seed(self):
        self._db_livros = [
            l.Livro(
                id=1,
                titulo="Dom Quixote",
                autor="Miguel de Cervantes",
                isbn="0101010101234",
            ),
            l.Livro(
                id=2,
                titulo="O Corcunda de Notre Dame",
                autor="Victor Hugo",
                isbn="0101010101567",
            ),
            l.Livro(
                id=3,
                titulo="Turma da Monica",
                autor="Mauricio de Souza",
                isbn="0101010101789",
            ),
        ]

    def criar_livro(self, data) -> Optional[l.Livro]:
        """
        Cria e adiciona um novo livro ao sistema.
        
        Args:
            titulo: Título do livro
            autor: Nome do autor
            isbn: Código ISBN (deve ser único)
        
        Returns:
            Livro criado ou None se houve erro (ISBN duplicado ou validação falhou)
        """
        # Verifica se já existe um livro com o mesmo ISBN
        if self.buscar_livro_por_isbn(data['isbn']):
            return None
        
        last_id = self._db_livros[-1].id if self._db_livros and len(self._db_livros) > 0 else 0
        new_id = last_id + 1

        try:
            livro = l.Livro(id=new_id, titulo=data['titulo'], autor=data['autor'], isbn=data['isbn'])
            self._db_livros.append(livro)
            return livro
        except ValueError:
            return None


    def listar_livros(self) -> List[l.Livro]:
        """
        Lista todos os livros cadastrados no sistema.
        
        Returns:
            Lista de livros (pode estar vazia)
        """
        return self._db_livros if self._db_livros and len(self._db_livros) > 0 else []

    def listar_autores(self) -> List[l.Livro]:
        """
        Lista todos os autores cadastrados no sistema.
        
        """
        autores = set()

        for livro in self._db_livros:
            autores.add(livro.autor)

        return list(autores) if autores else []

    def buscar_livro_por_isbn(self, isbn: str) -> Optional[l.Livro]:
        """
        Busca um livro pelo código ISBN.
        
        Args:
            isbn: Código ISBN a ser buscado
        
        Returns:
            Livro encontrado ou None se não existir
        """
        for livro in self._db_livros:
            if livro.isbn == isbn:
                return livro
        return None


    def atualizar_livro(isbn: str, novo_titulo: str, novo_autor: str) -> Optional[l.Livro]:
        """
        Atualiza informações de um livro existente.
        
        Args:
            isbn: ISBN do livro a ser atualizado
            novo_titulo: Novo título
            novo_autor: Novo autor
        
        Returns:
            Livro atualizado ou None se não encontrado
        """
        livro = buscar_livro_por_isbn(isbn)
        
        if not livro:
            return None
        
        livro.titulo = novo_titulo
        livro.autor = novo_autor
        return livro


    def deletar_livro(isbn: str) -> bool:
        """
        Remove um livro do sistema.
        
        Args:
            isbn: ISBN do livro a ser removido
        
        Returns:
            True se removido com sucesso, False se não encontrado
        """
        livro = buscar_livro_por_isbn(isbn)
        
        if not livro:
            return False
        
        _db_livros.remove(livro)
        return True 


class EmprestimoController:

    _emprestimos: List[e.Emprestimo] = []

    def __init__(self, emprestimos: List[e.Emprestimo] = None):
        # Não popula com seed - lista começa vazia
        self._emprestimos = emprestimos or []

    def listar(self) -> List[e.Emprestimo]:
        return self._emprestimos if self._emprestimos and len(self._emprestimos) > 0 else []

    def criar(self, usuario, livro, dias=7):
        """Cria um novo empréstimo e o salva."""
        # Validar se o livro está disponível
        if livro.status and livro.status.lower() != "disponivel":
            raise ValueError(f"Livro '{livro.titulo}' não está disponível. Status: {livro.status}")
        
        # Validar se já existe empréstimo ativo para este livro
        for emp in self._emprestimos:
            if emp.livro.isbn == livro.isbn and emp.status == "ATIVO":
                raise ValueError(f"Livro '{livro.titulo}' já foi emprestado e não foi devolvido")
        
        # Cria o empréstimo
        emprestimo = e.Emprestimo(usuario, livro, due_date=datetime.now() + timedelta(days=dias))
        
        # Marca o livro como indisponível
        livro.status = "emprestado"
        
        # Salva o empréstimo
        self._emprestimos.append(emprestimo)
        return emprestimo

    def atualizar(self, **kwargs):
        """Atualiza campos do empréstimo."""
        for chave, valor in kwargs.items():
            if hasattr(self, chave):
                setattr(self, chave, valor)
        return self

    def deletar(self, lista_emprestimos):
        """
        Remove o empréstimo de uma lista (simulando persistência).
        """
        lista_emprestimos[:] = [e for e in lista_emprestimos if e.loan_id != self.loan_id]

    def buscar_por_id(lista_emprestimos, loan_id):
        """Busca um empréstimo pelo ID."""
        for e in lista_emprestimos:
            if e.loan_id == loan_id:
                return e
        return None

    def buscar_por_usuario(lista_emprestimos, usuario_id):
        """Busca todos os empréstimos de um usuário."""
        return [e for e in lista_emprestimos if e.usuario.id == usuario_id]

    def buscar_por_livro(lista_emprestimos, livro_id):
        """Busca todos os empréstimos de um livro."""
        return [e for e in lista_emprestimos if e.livro.id == livro_id]


class RelatorioController:

    def __init__(self, usuarios: List[u.Usuario], livros: List[l.Livro], emprestimos: List[e.Emprestimo]):
        self.relatorio = r.Relatorio(usuarios, livros, emprestimos)

    def carregar_dados(self, usuarios: List[u.Usuario], livros: List[l.Livro], emprestimos: List[e.Emprestimo]):
        """Atualiza os dados do relatório"""
        self.relatorio.set_usuarios(usuarios)
        self.relatorio.set_livros(livros)
        self.relatorio.set_emprestimos(emprestimos)

    def livros_mais_emprestados(self, limite=10):
        """Retorna os livros mais emprestados"""
        return self.relatorio.livros_mais_emprestados(limite)

    def usuarios_mais_ativos(self, limite=10):
        """Retorna os usuários mais ativos"""
        return self.relatorio.usuarios_mais_ativos(limite)

    def taxa_ocupacao(self):
        """Retorna a taxa de ocupação do acervo"""
        return self.relatorio.taxa_ocupacao()

    def emprestimos_por_periodo(self, data_inicio, data_fim):
        """Filtra empréstimos por período"""
        return self.relatorio.emprestimos_por_periodo(data_inicio, data_fim)

    def total_emprestimos_ativos(self):
        """Retorna total de empréstimos ativos"""
        return self.relatorio.total_emprestimos_ativos()

    def emprestimos_em_atraso(self):
        """Retorna empréstimos atrasados"""
        return self.relatorio.emprestimos_em_atraso()

    def estatisticas_gerais(self):
        """Retorna estatísticas gerais do sistema"""
        return self.relatorio.estatisticas_gerais()

    def relatorio_completo(self):
        """Gera relatório completo"""
        return self.relatorio.relatorio_completo()