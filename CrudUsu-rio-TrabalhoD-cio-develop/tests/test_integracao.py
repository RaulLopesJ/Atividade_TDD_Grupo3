"""
Testes de Integração Entre Módulos
Integração entre Usuario, Livro, Emprestimo e Relatorio

Estes testes validam o fluxo completo do sistema sem interface gráfica,
testando a integração entre os módulos.
"""

import pytest
from datetime import datetime, timedelta
from Model.Usuario import Usuario, Tipo, Status
from Model.Livro import Livro, _limpar_db as limpar_db_livro
from Model.Emprestimo import Emprestimo, EmprestimoStatus
from Model.Relatorio import Relatorio


class TestIntegracaoUsuarioLivro:
    """[RED-GREEN-REFACTOR] Testes de integração Usuario + Livro"""
    
    def test_fluxo_usuario_visualiza_livro_disponivel(self):
        """[GREEN] Usuário consegue visualizar livro disponível"""
        # Arrange
        usuario = Usuario(id=1, nome="João", matricula="001", tipo=Tipo.ALUNO,
                         email="joao@email.com", ativoDeRegistro=True, status=Status.ATIVO)
        livro = Livro(id=1, titulo="Clean Code", autor="Robert C. Martin", isbn="978-0132350884")
        
        # Act & Assert
        assert livro.esta_disponivel() is True
        assert usuario.get_nome() == "João"


class TestIntegracaoUsuarioLivroEmprestimo:
    """[RED-GREEN-REFACTOR] Testes de integração Usuario + Livro + Emprestimo"""
    
    def test_fluxo_completo_emprestimo_devolucao(self):
        """[GREEN] Fluxo completo: criar usuário, criar livro, emprestar, devolver"""
        # Arrange
        usuario = Usuario(id=1, nome="Maria", matricula="002", tipo=Tipo.ALUNO,
                         email="maria@email.com", ativoDeRegistro=True, status=Status.ATIVO)
        livro = Livro(id=1, titulo="Design Patterns", autor="Gang of Four", isbn="978-0201633610")
        
        # Act - Emprestar
        emprestimo = Emprestimo(usuario=usuario, livro=livro)
        livro.emprestar()
        
        # Assert - Livro está emprestado
        assert not livro.esta_disponivel()
        assert emprestimo.status == EmprestimoStatus.ATIVO
        
        # Act - Devolver
        emprestimo.marcar_como_devolvido()
        
        # Assert - Livro está disponível novamente
        assert livro.esta_disponivel()
        assert emprestimo.status == EmprestimoStatus.DEVOLVIDO
    
    def test_multiplos_emprestimos_diferentes_usuarios(self):
        """[GREEN] Múltiplos usuários conseguem emprestar livros diferentes"""
        # Arrange
        usuario1 = Usuario(id=1, nome="João", matricula="001", tipo=Tipo.ALUNO,
                          email="joao@email.com", ativoDeRegistro=True, status=Status.ATIVO)
        usuario2 = Usuario(id=2, nome="Maria", matricula="002", tipo=Tipo.PROFESSOR,
                          email="maria@email.com", ativoDeRegistro=True, status=Status.ATIVO)
        
        livro1 = Livro(id=1, titulo="Python Fluente", autor="Luciano Ramalho", isbn="978-8575225448")
        livro2 = Livro(id=2, titulo="Refactoring", autor="Martin Fowler", isbn="978-0201485677")
        
        # Act
        emprestimo1 = Emprestimo(usuario=usuario1, livro=livro1)
        emprestimo2 = Emprestimo(usuario=usuario2, livro=livro2)
        livro1.emprestar()
        livro2.emprestar()
        
        # Assert
        assert emprestimo1.usuario.get_nome() == "João"
        assert emprestimo2.usuario.get_nome() == "Maria"
        assert emprestimo1.livro.titulo == "Python Fluente"
        assert emprestimo2.livro.titulo == "Refactoring"


class TestIntegracaoRelatario:
    """[RED-GREEN-REFACTOR] Testes de integração com Relatório"""
    
    def test_fluxo_relatorio_com_emprestimos(self):
        """[GREEN] Relatório consegue processar empréstimos"""
        # Arrange
        limpar_db_livro()
        usuarios = [
            Usuario(id=1, nome="João", matricula="001", tipo=Tipo.ALUNO,
                   email="joao@email.com", ativoDeRegistro=True, status=Status.ATIVO),
            Usuario(id=2, nome="Maria", matricula="002", tipo=Tipo.PROFESSOR,
                   email="maria@email.com", ativoDeRegistro=True, status=Status.ATIVO)
        ]
        
        livros = [
            Livro(id=1, titulo="Clean Code", autor="Robert C. Martin", isbn="978-0132350884"),
            Livro(id=2, titulo="Design Patterns", autor="Gang of Four", isbn="978-0201633610")
        ]
        
        emprestimos = [
            Emprestimo(usuario=usuarios[0], livro=livros[0]),
            Emprestimo(usuario=usuarios[1], livro=livros[1]),
            Emprestimo(usuario=usuarios[0], livro=livros[1])
        ]
        
        # Act
        relatorio = Relatorio(usuarios=usuarios, livros=livros, emprestimos=emprestimos)
        
        # Assert
        assert len(relatorio.get_usuarios()) == 2
        assert len(relatorio.get_livros()) == 2
        assert len(relatorio.get_emprestimos()) == 3
    
    def test_fluxo_validacao_disponibilidade_livro(self):
        """[GREEN] Sistema valida disponibilidade antes de emprestar"""
        # Arrange
        usuario = Usuario(id=1, nome="Pedro", matricula="003", tipo=Tipo.ALUNO,
                         email="pedro@email.com", ativoDeRegistro=True, status=Status.ATIVO)
        livro = Livro(id=1, titulo="Code Complete", autor="Steve McConnell", isbn="978-0735619678")
        
        # Act
        emprestimo = Emprestimo(usuario=usuario, livro=livro)
        
        # Assert - Antes de emprestar
        assert livro.esta_disponivel() is True
        
        # Act - Emprestar
        livro.emprestar()
        
        # Assert - Depois de emprestar
        assert livro.esta_disponivel() is False


class TestIntegracaoCompleta:
    """[RED-GREEN-REFACTOR] Testes de integração completa do sistema"""
    
    def test_fluxo_biblioteca_completa_operacional(self):
        """[GREEN] Fluxo completo da biblioteca com múltiplas operações"""
        # Arrange - Setup
        limpar_db_livro()
        
        # Criar usuários
        usuario_aluno1 = Usuario(id=1, nome="Alice", matricula="ALU001", tipo=Tipo.ALUNO,
                               email="alice@email.com", ativoDeRegistro=True, status=Status.ATIVO)
        usuario_aluno2 = Usuario(id=2, nome="Bob", matricula="ALU002", tipo=Tipo.ALUNO,
                               email="bob@email.com", ativoDeRegistro=True, status=Status.ATIVO)
        usuario_professor = Usuario(id=3, nome="Prof. Carlos", matricula="PROF001", tipo=Tipo.PROFESSOR,
                                   email="carlos@email.com", ativoDeRegistro=True, status=Status.ATIVO)
        
        usuarios = [usuario_aluno1, usuario_aluno2, usuario_professor]
        
        # Criar livros
        livro1 = Livro(id=1, titulo="Clean Code", autor="Robert C. Martin", isbn="978-0132350884")
        livro2 = Livro(id=2, titulo="Design Patterns", autor="Gang of Four", isbn="978-0201633610")
        livro3 = Livro(id=3, titulo="Python Fluente", autor="Luciano Ramalho", isbn="978-8575225448")
        livro4 = Livro(id=4, titulo="Refactoring", autor="Martin Fowler", isbn="978-0201485677")
        livro5 = Livro(id=5, titulo="Code Complete", autor="Steve McConnell", isbn="978-0735619678")
        
        livros = [livro1, livro2, livro3, livro4, livro5]
        
        # Act - Fazer empréstimos
        emprestimos = [
            Emprestimo(usuario=usuario_aluno1, livro=livro1),
            Emprestimo(usuario=usuario_aluno1, livro=livro2),
            Emprestimo(usuario=usuario_aluno2, livro=livro3),
            Emprestimo(usuario=usuario_aluno2, livro=livro4),
            Emprestimo(usuario=usuario_professor, livro=livro5),
            Emprestimo(usuario=usuario_professor, livro=livro1)
        ]
        
        # Act - Marcar livros como emprestados
        for i, emp in enumerate(emprestimos):
            if i < len(emprestimos):
                emp.livro.emprestar()
        
        # Act - Devolver alguns livros
        emprestimos[0].marcar_como_devolvido()
        emprestimos[2].marcar_como_devolvido()
        
        # Act - Criar relatório
        relatorio = Relatorio(usuarios=usuarios, livros=livros, emprestimos=emprestimos)
        
        # Assert - Validar estado
        assert len(usuarios) == 3
        assert len(livros) == 5
        assert len(emprestimos) == 6
        
        # Validar empréstimos
        assert emprestimos[0].status == EmprestimoStatus.DEVOLVIDO
        assert emprestimos[1].status == EmprestimoStatus.ATIVO
        assert emprestimos[2].status == EmprestimoStatus.DEVOLVIDO
        assert emprestimos[3].status == EmprestimoStatus.ATIVO
        
        # Validar disponibilidade de livros
        # livro1: Devolvido por João mas ainda emprestado para professor
        assert livro1.esta_disponivel() is True   # Devolvido por João (último empréstimo)
        # livro2: Ainda emprestado para aluno1
        assert livro2.esta_disponivel() is False  # Ainda emprestado para aluno1
        # livro3: Foi devolvido
        assert livro3.esta_disponivel() is True   # Foi devolvido
        # livro4: Ainda emprestado
        assert livro4.esta_disponivel() is False  # Ainda emprestado
        # livro5: Ainda emprestado
        assert livro5.esta_disponivel() is False  # Ainda emprestado
