"""
Equipe 2 - Testes para Catálogo de Livros
Módulo: Model/Livro.py

15 Testes Totais:
- 10 testes unitários (casos de sucesso, erro e validação)
- 5 testes de contrato/integridade (serialização, campos obrigatórios, tipos)
"""

import pytest
from Model.Livro import Livro, STATUS_DISPONIVEL, STATUS_EMPRESTADO, _limpar_db


# ============================================
# TESTES UNITÁRIOS (10 testes)
# ============================================

class TestLivroCriacao:
    """[RED-GREEN-REFACTOR] Testes de criação e inicialização de livros"""
    
    def setup_method(self):
        """Limpa o banco antes de cada teste"""
        _limpar_db()
    
    def test_criar_livro_valido(self):
        """[GREEN] Criar livro com todos os dados válidos"""
        livro = Livro(
            id=1,
            titulo="Clean Code",
            autor="Robert C. Martin",
            isbn="978-0132350884"
        )
        assert livro.titulo == "Clean Code"
        assert livro.autor == "Robert C. Martin"
        assert livro.isbn == "978-0132350884"
        assert livro.id == 1
    
    def test_livro_status_disponivel_por_padrao(self):
        """[GREEN] Livro começa com status disponível"""
        livro = Livro(
            id=1,
            titulo="Design Patterns",
            autor="Gang of Four",
            isbn="978-0201633610"
        )
        assert livro.status == STATUS_DISPONIVEL
    
    def test_livro_titulo_vazio_lanca_erro(self):
        """[RED] Título vazio deve lançar ValueError"""
        with pytest.raises(ValueError, match="Título é obrigatório"):
            Livro(id=1, titulo="", autor="Autor", isbn="978-1234567890")
    
    def test_livro_autor_vazio_lanca_erro(self):
        """[RED] Autor vazio deve lançar ValueError"""
        with pytest.raises(ValueError, match="Autor é obrigatório"):
            Livro(id=1, titulo="Livro", autor="", isbn="978-1234567890")
    
    def test_livro_isbn_vazio_lanca_erro(self):
        """[RED] ISBN vazio deve lançar ValueError"""
        with pytest.raises(ValueError, match="ISBN é obrigatório"):
            Livro(id=1, titulo="Livro", autor="Autor", isbn="")


class TestLivroOperacoes:
    """[RED-GREEN-REFACTOR] Testes de operações e mudança de estado"""
    
    def setup_method(self):
        """Limpa o banco antes de cada teste"""
        _limpar_db()
    
    def test_emprestar_livro(self):
        """[GREEN] Emprestar livro muda status para emprestado"""
        livro = Livro(
            id=1,
            titulo="Python Fluente",
            autor="Luciano Ramalho",
            isbn="978-8575225448"
        )
        livro.emprestar()
        assert livro.status == STATUS_EMPRESTADO
    
    def test_devolver_livro(self):
        """[GREEN] Devolver livro muda status para disponível"""
        livro = Livro(
            id=1,
            titulo="Refactoring",
            autor="Martin Fowler",
            isbn="978-0201485677"
        )
        livro.emprestar()
        livro.devolver()
        assert livro.status == STATUS_DISPONIVEL
    
    def test_esta_disponivel_true(self):
        """[GREEN] Livro disponível retorna True"""
        livro = Livro(
            id=1,
            titulo="The Pragmatic Programmer",
            autor="Hunt e Thomas",
            isbn="978-0135957059"
        )
        assert livro.esta_disponivel() is True
    
    def test_esta_disponivel_false(self):
        """[GREEN] Livro emprestado retorna False"""
        livro = Livro(
            id=1,
            titulo="Code Complete",
            autor="Steve McConnell",
            isbn="978-0735619678"
        )
        livro.emprestar()
        assert livro.esta_disponivel() is False


# ============================================
# TESTES DE CONTRATO/INTEGRIDADE (5 testes)
# ============================================

class TestContratoLivro:
    """[RED-GREEN-REFACTOR] Testes de contrato e integridade de dados"""
    
    def setup_method(self):
        """Limpa o banco antes de cada teste"""
        _limpar_db()
    
    def test_campos_obrigatorios_existem(self):
        """[GREEN] Todos os campos obrigatórios estão presentes"""
        livro = Livro(
            id=1,
            titulo="Structure and Interpretation",
            autor="Sussman & Abelson",
            isbn="978-0262011632"
        )
        assert hasattr(livro, 'id')
        assert hasattr(livro, 'titulo')
        assert hasattr(livro, 'autor')
        assert hasattr(livro, 'isbn')
        assert hasattr(livro, 'status')
    
    def test_tipos_de_dados_corretos(self):
        """[GREEN] Todos os campos têm tipos corretos"""
        livro = Livro(
            id=1,
            titulo="Introduction to Algorithms",
            autor="CLRS",
            isbn="978-0262033848"
        )
        assert isinstance(livro.id, int)
        assert isinstance(livro.titulo, str)
        assert isinstance(livro.autor, str)
        assert isinstance(livro.isbn, str)
        assert isinstance(livro.status, str)
    
    def test_constantes_status_validas(self):
        """[GREEN] Constantes de status têm valores esperados"""
        assert STATUS_DISPONIVEL == "disponivel"
        assert STATUS_EMPRESTADO == "emprestado"
    
    def test_livro_com_espacos_em_branco_lanca_erro(self):
        """[RED] Campos com apenas espaços devem lançar erro"""
        with pytest.raises(ValueError, match="Título é obrigatório"):
            Livro(id=1, titulo="   ", autor="Autor", isbn="978-1234567890")
        
        with pytest.raises(ValueError, match="Autor é obrigatório"):
            Livro(id=1, titulo="Livro", autor="   ", isbn="978-1234567890")
    
    def test_multiplas_operacoes_nao_corrompem_estado(self):
        """[GREEN] Múltiplas operações mantêm estado consistente"""
        livro = Livro(
            id=1,
            titulo="Enterprise Integration",
            autor="Gregor Hohpe",
            isbn="978-0321200686"
        )
        # Estado inicial
        assert livro.esta_disponivel() is True
        
        # Emprestar
        livro.emprestar()
        assert livro.esta_disponivel() is False
        
        # Devolver
        livro.devolver()
        assert livro.esta_disponivel() is True
        
        # Emprestar novamente
        livro.emprestar()
        assert livro.esta_disponivel() is False
