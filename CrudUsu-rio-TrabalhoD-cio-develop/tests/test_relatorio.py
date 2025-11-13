"""
Equipe 4 - Testes para Relatórios e Estatísticas
Módulo: Model/Relatorio.py

15 Testes Totais:
- 10 testes unitários (casos de sucesso, erro e validação)
- 5 testes de contrato/integridade (serialização, campos obrigatórios, tipos)

⚠️ IMPORTANTE: Este módulo depende de todos os outros módulos!
"""

import pytest
from datetime import datetime, timedelta
from Model.Relatorio import Relatorio
from Model.Usuario import Usuario, Tipo, Status
from Model.Livro import Livro, _limpar_db as limpar_db_livro
from Model.Emprestimo import Emprestimo


# ============================================
# FIXTURES (Dados compartilhados)
# ============================================

@pytest.fixture
def usuarios_teste():
    """Cria usuários para testes"""
    return [
        Usuario(id=1, nome="João", matricula="001", tipo=Tipo.ALUNO, 
                email="joao@email.com", ativoDeRegistro=True, status=Status.ATIVO),
        Usuario(id=2, nome="Maria", matricula="002", tipo=Tipo.PROFESSOR, 
                email="maria@email.com", ativoDeRegistro=True, status=Status.ATIVO),
        Usuario(id=3, nome="Pedro", matricula="003", tipo=Tipo.ALUNO, 
                email="pedro@email.com", ativoDeRegistro=True, status=Status.ATIVO),
    ]


@pytest.fixture
def livros_teste():
    """Cria livros para testes"""
    limpar_db_livro()
    return [
        Livro(id=1, titulo="Clean Code", autor="Robert C. Martin", isbn="978-0132350884"),
        Livro(id=2, titulo="Design Patterns", autor="Gang of Four", isbn="978-0201633610"),
        Livro(id=3, titulo="Python Fluente", autor="Luciano Ramalho", isbn="978-8575225448"),
        Livro(id=4, titulo="Refactoring", autor="Martin Fowler", isbn="978-0201485677"),
        Livro(id=5, titulo="Code Complete", autor="Steve McConnell", isbn="978-0735619678"),
    ]


@pytest.fixture
def emprestimos_teste(usuarios_teste, livros_teste):
    """Cria empréstimos para testes"""
    return [
        Emprestimo(usuario=usuarios_teste[0], livro=livros_teste[0]),  # João empresta Clean Code
        Emprestimo(usuario=usuarios_teste[0], livro=livros_teste[1]),  # João empresta Design Patterns
        Emprestimo(usuario=usuarios_teste[1], livro=livros_teste[0]),  # Maria empresta Clean Code (2ª vez)
        Emprestimo(usuario=usuarios_teste[2], livro=livros_teste[2]),  # Pedro empresta Python Fluente
        Emprestimo(usuario=usuarios_teste[2], livro=livros_teste[3]),  # Pedro empresta Refactoring
        Emprestimo(usuario=usuarios_teste[0], livro=livros_teste[4]),  # João empresta Code Complete
    ]


# ============================================
# TESTES UNITÁRIOS (10 testes)
# ============================================

class TestRelatorioCriacao:
    """[RED-GREEN-REFACTOR] Testes de criação e inicialização de relatórios"""
    
    def test_criar_relatorio_vazio(self):
        """[GREEN] Criar relatório vazio"""
        relatorio = Relatorio(usuarios=[], livros=[], emprestimos=[])
        assert relatorio.usuarios == []
        assert relatorio.livros == []
        assert relatorio.emprestimos == []
    
    def test_criar_relatorio_com_dados(self, usuarios_teste, livros_teste, emprestimos_teste):
        """[GREEN] Criar relatório com dados"""
        relatorio = Relatorio(
            usuarios=usuarios_teste,
            livros=livros_teste,
            emprestimos=emprestimos_teste
        )
        assert len(relatorio.usuarios) == 3
        assert len(relatorio.livros) == 5
        assert len(relatorio.emprestimos) == 6


class TestRelatorioLeitura:
    """[RED-GREEN-REFACTOR] Testes de leitura de dados"""
    
    def test_get_usuarios(self, usuarios_teste, livros_teste):
        """[GREEN] Getter de usuários funciona"""
        relatorio = Relatorio(usuarios=usuarios_teste, livros=livros_teste, emprestimos=[])
        assert relatorio.get_usuarios() == usuarios_teste
    
    def test_get_livros(self, usuarios_teste, livros_teste):
        """[GREEN] Getter de livros funciona"""
        relatorio = Relatorio(usuarios=usuarios_teste, livros=livros_teste, emprestimos=[])
        assert relatorio.get_livros() == livros_teste
    
    def test_get_emprestimos(self, usuarios_teste, livros_teste, emprestimos_teste):
        """[GREEN] Getter de empréstimos funciona"""
        relatorio = Relatorio(
            usuarios=usuarios_teste,
            livros=livros_teste,
            emprestimos=emprestimos_teste
        )
        assert relatorio.get_emprestimos() == emprestimos_teste


class TestRelatorioEscrita:
    """[RED-GREEN-REFACTOR] Testes de escrita de dados"""
    
    def test_set_usuarios(self, usuarios_teste, livros_teste):
        """[GREEN] Setter de usuários funciona"""
        relatorio = Relatorio(usuarios=[], livros=livros_teste, emprestimos=[])
        relatorio.set_usuarios(usuarios_teste)
        assert relatorio.get_usuarios() == usuarios_teste
    
    def test_set_livros(self, usuarios_teste, livros_teste):
        """[GREEN] Setter de livros funciona"""
        relatorio = Relatorio(usuarios=usuarios_teste, livros=[], emprestimos=[])
        relatorio.set_livros(livros_teste)
        assert relatorio.get_livros() == livros_teste
    
    def test_set_emprestimos(self, usuarios_teste, livros_teste, emprestimos_teste):
        """[GREEN] Setter de empréstimos funciona"""
        relatorio = Relatorio(
            usuarios=usuarios_teste,
            livros=livros_teste,
            emprestimos=[]
        )
        relatorio.set_emprestimos(emprestimos_teste)
        assert relatorio.get_emprestimos() == emprestimos_teste


# ============================================
# TESTES DE CONTRATO/INTEGRIDADE (5 testes)
# ============================================

class TestContratoRelatorio:
    """[RED-GREEN-REFACTOR] Testes de contrato e integridade de dados"""
    
    def test_campos_obrigatorios_existem(self, usuarios_teste, livros_teste, emprestimos_teste):
        """[GREEN] Todos os campos obrigatórios estão presentes"""
        relatorio = Relatorio(
            usuarios=usuarios_teste,
            livros=livros_teste,
            emprestimos=emprestimos_teste
        )
        assert hasattr(relatorio, 'usuarios')
        assert hasattr(relatorio, 'livros')
        assert hasattr(relatorio, 'emprestimos')
    
    def test_tipos_de_dados_corretos(self, usuarios_teste, livros_teste, emprestimos_teste):
        """[GREEN] Todos os campos têm tipos corretos"""
        relatorio = Relatorio(
            usuarios=usuarios_teste,
            livros=livros_teste,
            emprestimos=emprestimos_teste
        )
        assert isinstance(relatorio.usuarios, list)
        assert isinstance(relatorio.livros, list)
        assert isinstance(relatorio.emprestimos, list)
    
    def test_relatorio_com_none_usa_lista_vazia(self):
        """[GREEN] None é convertido para lista vazia"""
        relatorio = Relatorio(usuarios=None, livros=None, emprestimos=None)
        assert relatorio.usuarios == []
        assert relatorio.livros == []
        assert relatorio.emprestimos == []
    
    def test_metodos_essenciais_existem(self, usuarios_teste, livros_teste, emprestimos_teste):
        """[GREEN] Todos os métodos essenciais existem"""
        relatorio = Relatorio(
            usuarios=usuarios_teste,
            livros=livros_teste,
            emprestimos=emprestimos_teste
        )
        # Métodos de leitura
        assert hasattr(relatorio, 'get_usuarios')
        assert hasattr(relatorio, 'get_livros')
        assert hasattr(relatorio, 'get_emprestimos')
        
        # Métodos de escrita
        assert hasattr(relatorio, 'set_usuarios')
        assert hasattr(relatorio, 'set_livros')
        assert hasattr(relatorio, 'set_emprestimos')
        
        # Métodos de relatório
        assert hasattr(relatorio, 'livros_mais_emprestados')
        assert hasattr(relatorio, 'usuarios_mais_ativos')
    
    def test_getters_retornam_referencias_corretas(self, usuarios_teste, livros_teste, emprestimos_teste):
        """[GREEN] Getters retornam as listas corretas"""
        relatorio = Relatorio(
            usuarios=usuarios_teste,
            livros=livros_teste,
            emprestimos=emprestimos_teste
        )
        
        usuarios_obtidos = relatorio.get_usuarios()
        livros_obtidos = relatorio.get_livros()
        emprestimos_obtidos = relatorio.get_emprestimos()
        
        assert usuarios_obtidos[0].nome == "João"
        assert livros_obtidos[0].titulo == "Clean Code"
        assert len(emprestimos_obtidos) == 6
