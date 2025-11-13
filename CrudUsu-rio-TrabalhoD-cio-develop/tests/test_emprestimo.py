"""
Equipe 3 - Testes para Empréstimo e Devolução
Módulo: Model/Emprestimo.py

15 Testes Totais:
- 10 testes unitários (casos de sucesso, erro e validação)
- 5 testes de contrato/integridade (serialização, campos obrigatórios, tipos)

⚠️ IMPORTANTE: Este módulo depende dos módulos Usuario e Livro!
"""

import pytest
from datetime import datetime, timedelta
from Model.Emprestimo import Emprestimo, EmprestimoStatus
from Model.Usuario import Usuario, Tipo, Status
from Model.Livro import Livro


# ============================================
# FIXTURES (Dados compartilhados)
# ============================================

@pytest.fixture
def usuario_aluno():
    """Cria um usuário aluno para testes"""
    return Usuario(
        id=1,
        nome="João Silva",
        matricula="ALUNO001",
        tipo=Tipo.ALUNO,
        email="joao@email.com",
        ativoDeRegistro=True,
        status=Status.ATIVO
    )


@pytest.fixture
def livro_clean_code():
    """Cria um livro para testes"""
    return Livro(
        id=1,
        titulo="Clean Code",
        autor="Robert C. Martin",
        isbn="978-0132350884"
    )


# ============================================
# TESTES UNITÁRIOS (10 testes)
# ============================================

class TestEmprestimoCriacao:
    """[RED-GREEN-REFACTOR] Testes de criação e inicialização de empréstimos"""
    
    def test_criar_emprestimo_valido(self, usuario_aluno, livro_clean_code):
        """[GREEN] Criar empréstimo com usuario e livro válidos"""
        emprestimo = Emprestimo(
            usuario=usuario_aluno,
            livro=livro_clean_code
        )
        assert emprestimo.usuario == usuario_aluno
        assert emprestimo.livro == livro_clean_code
        assert emprestimo.status == EmprestimoStatus.ATIVO
    
    def test_emprestimo_sem_usuario_lanca_erro(self, livro_clean_code):
        """[RED] Empréstimo sem usuário deve lançar ValueError"""
        with pytest.raises(ValueError, match="Usuário e Livro são obrigatórios"):
            Emprestimo(usuario=None, livro=livro_clean_code)
    
    def test_emprestimo_sem_livro_lanca_erro(self, usuario_aluno):
        """[RED] Empréstimo sem livro deve lançar ValueError"""
        with pytest.raises(ValueError, match="Usuário e Livro são obrigatórios"):
            Emprestimo(usuario=usuario_aluno, livro=None)
    
    def test_emprestimo_recebe_id_automatico(self, usuario_aluno, livro_clean_code):
        """[GREEN] Empréstimo recebe ID automático"""
        emprestimo = Emprestimo(usuario=usuario_aluno, livro=livro_clean_code)
        assert emprestimo.loan_id is not None
    
    def test_emprestimo_data_padrao(self, usuario_aluno, livro_clean_code):
        """[GREEN] Data de empréstimo é definida automaticamente"""
        emprestimo = Emprestimo(usuario=usuario_aluno, livro=livro_clean_code)
        assert emprestimo.loan_date is not None
        assert isinstance(emprestimo.loan_date, datetime)


class TestEmprestimoOperacoes:
    """[RED-GREEN-REFACTOR] Testes de operações e mudança de estado"""
    
    def test_marcar_como_devolvido(self, usuario_aluno, livro_clean_code):
        """[GREEN] Marcar empréstimo como devolvido"""
        emprestimo = Emprestimo(usuario=usuario_aluno, livro=livro_clean_code)
        livro_clean_code.emprestar()
        
        resultado = emprestimo.marcar_como_devolvido()
        
        assert emprestimo.status == EmprestimoStatus.DEVOLVIDO
        assert emprestimo.return_date is not None
        assert livro_clean_code.status == "disponivel"
    
    def test_esta_em_atraso_livro_no_prazo(self, usuario_aluno, livro_clean_code):
        """[GREEN] Empréstimo no prazo não está atrasado"""
        emprestimo = Emprestimo(
            usuario=usuario_aluno,
            livro=livro_clean_code,
            loan_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=5)
        )
        assert emprestimo.esta_em_atraso() is False
    
    def test_esta_em_atraso_livro_atrasado(self, usuario_aluno, livro_clean_code):
        """[GREEN] Empréstimo atrasado é detectado"""
        emprestimo = Emprestimo(
            usuario=usuario_aluno,
            livro=livro_clean_code,
            loan_date=datetime.now() - timedelta(days=10),
            due_date=datetime.now() - timedelta(days=3)
        )
        assert emprestimo.esta_em_atraso() is True
    
    def test_calcular_multa_sem_atraso(self, usuario_aluno, livro_clean_code):
        """[GREEN] Sem atraso, multa é zero"""
        emprestimo = Emprestimo(
            usuario=usuario_aluno,
            livro=livro_clean_code,
            loan_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=7)
        )
        multa = emprestimo.calcular_multa()
        assert multa == 0.0


# ============================================
# TESTES DE CONTRATO/INTEGRIDADE (5 testes)
# ============================================

class TestContratoEmprestimo:
    """[RED-GREEN-REFACTOR] Testes de contrato e integridade de dados"""
    
    def test_campos_obrigatorios_existem(self, usuario_aluno, livro_clean_code):
        """[GREEN] Todos os campos obrigatórios estão presentes"""
        emprestimo = Emprestimo(usuario=usuario_aluno, livro=livro_clean_code)
        assert hasattr(emprestimo, 'loan_id')
        assert hasattr(emprestimo, 'usuario')
        assert hasattr(emprestimo, 'livro')
        assert hasattr(emprestimo, 'loan_date')
        assert hasattr(emprestimo, 'due_date')
        assert hasattr(emprestimo, 'return_date')
        assert hasattr(emprestimo, 'status')
        assert hasattr(emprestimo, 'fine')
    
    def test_tipos_de_dados_corretos(self, usuario_aluno, livro_clean_code):
        """[GREEN] Todos os campos têm tipos corretos"""
        emprestimo = Emprestimo(usuario=usuario_aluno, livro=livro_clean_code)
        assert isinstance(emprestimo.loan_id, str)
        assert emprestimo.usuario is not None
        assert emprestimo.livro is not None
        assert isinstance(emprestimo.loan_date, datetime)
        assert isinstance(emprestimo.due_date, datetime)
        assert isinstance(emprestimo.status, str)
        assert isinstance(emprestimo.fine, (int, float))
    
    def test_to_dict_serializa_corretamente(self, usuario_aluno, livro_clean_code):
        """[GREEN] Serialização para dict funciona"""
        emprestimo = Emprestimo(usuario=usuario_aluno, livro=livro_clean_code)
        dados = emprestimo.to_dict()
        
        assert "loanId" in dados
        assert "userId" in dados
        assert "bookId" in dados
        assert "loanDate" in dados
        assert "dueDate" in dados
        assert "status" in dados
        assert "fine" in dados
    
    def test_status_enum_valores_validos(self):
        """[GREEN] Status enum contém todos os valores esperados"""
        assert EmprestimoStatus.ATIVO == "ATIVO"
        assert EmprestimoStatus.DEVOLVIDO == "DEVOLVIDO"
        assert EmprestimoStatus.ATRASADO == "ATRASADO"
    
    def test_emprestimo_datas_consistentes(self, usuario_aluno, livro_clean_code):
        """[GREEN] Datas mantêm consistência lógica"""
        emprestimo = Emprestimo(usuario=usuario_aluno, livro=livro_clean_code)
        
        # Data de empréstimo deve ser antes da data de devolução esperada
        assert emprestimo.loan_date <= emprestimo.due_date
        
        # Return date deve ser None antes da devolução
        assert emprestimo.return_date is None
        
        # Multa inicial deve ser zero ou positiva
        assert emprestimo.fine >= 0
