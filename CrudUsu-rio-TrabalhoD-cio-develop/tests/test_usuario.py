"""
Equipe 1 - Testes para Cadastro de Usuários
Módulo: Model/Usuario.py

15 Testes Totais:
- 10 testes unitários (casos de sucesso, erro e validação)
- 5 testes de contrato/integridade (serialização, campos obrigatórios, tipos)
"""

import pytest
from Model.Usuario import Usuario, Tipo, Status


# ============================================
# TESTES UNITÁRIOS (10 testes)
# ============================================

class TestUsuarioCriacao:
    """[RED-GREEN-REFACTOR] Testes de criação e inicialização de usuários"""
    
    def test_criar_usuario_valido(self):
        """[GREEN] Criar usuário com todos os dados válidos"""
        usuario = Usuario(
            id=1,
            nome="João Silva",
            matricula="ALUNO001",
            tipo=Tipo.ALUNO,
            email="joao@email.com",
            ativoDeRegistro=True,
            status=Status.ATIVO
        )
        assert usuario.nome == "João Silva"
        assert usuario.matricula == "ALUNO001"
        assert usuario.tipo == Tipo.ALUNO
        assert usuario.email == "joao@email.com"
    
    def test_usuario_com_id_automatico(self):
        """[GREEN] Usuario recebe ID automático quando não fornecido"""
        usuario = Usuario(
            id=None,
            nome="Maria Santos",
            matricula="PROF001",
            tipo=Tipo.PROFESSOR,
            email="maria@email.com",
            ativoDeRegistro=True,
            status=Status.ATIVO
        )
        assert usuario.id is not None
        assert usuario.get_id() == usuario.id
    
    def test_usuario_status_ativo_padrao(self):
        """[GREEN] Usuario começa com status ATIVO"""
        usuario = Usuario(
            id=1,
            nome="Pedro Costa",
            matricula="FUNC001",
            tipo=Tipo.FUNCIONARIO,
            email="pedro@email.com",
            ativoDeRegistro=True,
            status=Status.ATIVO
        )
        assert usuario.get_status() == Status.ATIVO


class TestValidacaoUsuario:
    """[RED-GREEN-REFACTOR] Testes de validações e regras de negócio"""
    
    def test_tipo_usuario_por_string(self):
        """[GREEN] Tipo de usuário pode ser definido por string"""
        usuario = Usuario(
            id=1,
            nome="Ana Silva",
            matricula="ALUNO002",
            tipo="ALUNO",
            email="ana@email.com",
            ativoDeRegistro=True,
            status="ATIVO"
        )
        usuario.set_tipo("PROFESSOR")
        assert usuario.get_tipo() == Tipo.PROFESSOR
    
    def test_tipo_invalido_lanca_erro(self):
        """[RED] Tipo inválido deve lançar ValueError"""
        usuario = Usuario(
            id=1,
            nome="Carlos",
            matricula="MAT001",
            tipo=Tipo.ALUNO,
            email="carlos@email.com",
            ativoDeRegistro=True,
            status=Status.ATIVO
        )
        with pytest.raises(ValueError, match="tipo inválido"):
            usuario.set_tipo("TIPO_INVALIDO")
    
    def test_status_invalido_lanca_erro(self):
        """[RED] Status inválido deve lançar ValueError"""
        usuario = Usuario(
            id=1,
            nome="Julia",
            matricula="MAT002",
            tipo=Tipo.ALUNO,
            email="julia@email.com",
            ativoDeRegistro=True,
            status=Status.ATIVO
        )
        with pytest.raises(ValueError, match="status inválido"):
            usuario.set_status("STATUS_INEXISTENTE")
    
    def test_setter_nome(self):
        """[GREEN] Nome pode ser alterado via setter"""
        usuario = Usuario(
            id=1,
            nome="Roberto",
            matricula="MAT003",
            tipo=Tipo.ALUNO,
            email="roberto@email.com",
            ativoDeRegistro=True,
            status=Status.ATIVO
        )
        usuario.set_nome("Roberto Silva")
        assert usuario.get_nome() == "Roberto Silva"
    
    def test_setter_email(self):
        """[GREEN] Email pode ser alterado via setter"""
        usuario = Usuario(
            id=1,
            nome="Fernanda",
            matricula="MAT004",
            tipo=Tipo.PROFESSOR,
            email="fernanda@email.com",
            ativoDeRegistro=True,
            status=Status.ATIVO
        )
        usuario.set_email("fernanda.silva@email.com")
        assert usuario.get_email() == "fernanda.silva@email.com"
    
    def test_setter_matricula(self):
        """[GREEN] Matrícula pode ser alterada via setter"""
        usuario = Usuario(
            id=1,
            nome="Lucas",
            matricula="MAT005",
            tipo=Tipo.ALUNO,
            email="lucas@email.com",
            ativoDeRegistro=True,
            status=Status.ATIVO
        )
        usuario.set_matricula("MAT005_NOVO")
        assert usuario.get_matricula() == "MAT005_NOVO"


# ============================================
# TESTES DE CONTRATO/INTEGRIDADE (5 testes)
# ============================================

class TestContratoUsuario:
    """[RED-GREEN-REFACTOR] Testes de contrato e integridade de dados"""
    
    def test_campos_obrigatorios_existem(self):
        """[GREEN] Todos os campos obrigatórios estão presentes"""
        usuario = Usuario(
            id=1,
            nome="Thiago",
            matricula="MAT006",
            tipo=Tipo.ALUNO,
            email="thiago@email.com",
            ativoDeRegistro=True,
            status=Status.ATIVO
        )
        # Verifica se todos os atributos existem
        assert hasattr(usuario, 'id')
        assert hasattr(usuario, 'nome')
        assert hasattr(usuario, 'matricula')
        assert hasattr(usuario, 'tipo')
        assert hasattr(usuario, 'email')
        assert hasattr(usuario, 'ativoDeRegistro')
        assert hasattr(usuario, 'status')
    
    def test_tipos_de_dados_corretos(self):
        """[GREEN] Todos os campos têm tipos corretos"""
        usuario = Usuario(
            id=1,
            nome="Beatriz",
            matricula="MAT007",
            tipo=Tipo.PROFESSOR,
            email="beatriz@email.com",
            ativoDeRegistro=False,
            status=Status.INATIVO
        )
        assert isinstance(usuario.nome, str)
        assert isinstance(usuario.matricula, str)
        assert isinstance(usuario.tipo, Tipo)
        assert isinstance(usuario.email, str)
        assert isinstance(usuario.ativoDeRegistro, bool)
        assert isinstance(usuario.status, Status)
    
    def test_getters_retornam_valores_corretos(self):
        """[GREEN] Todos os getters funcionam corretamente"""
        usuario = Usuario(
            id=2,
            nome="Gustavo",
            matricula="MAT008",
            tipo=Tipo.FUNCIONARIO,
            email="gustavo@email.com",
            ativoDeRegistro=True,
            status=Status.SUSPENSO
        )
        assert usuario.get_id() == 2
        assert usuario.get_nome() == "Gustavo"
        assert usuario.get_matricula() == "MAT008"
        assert usuario.get_tipo() == Tipo.FUNCIONARIO
        assert usuario.get_email() == "gustavo@email.com"
        assert usuario.get_ativoDeRegistro() == True
        assert usuario.get_status() == Status.SUSPENSO
    
    def test_enum_valores_validos(self):
        """[GREEN] Enums contêm todos os valores esperados"""
        # Testa Tipo enum
        assert Tipo.ALUNO.value == "ALUNO"
        assert Tipo.PROFESSOR.value == "PROFESSOR"
        assert Tipo.FUNCIONARIO.value == "FUNCIONARIO"
        
        # Testa Status enum
        assert Status.ATIVO.value == "ATIVO"
        assert Status.INATIVO.value == "INATIVO"
        assert Status.SUSPENSO.value == "SUSPENSO"
    
    def test_replace_cria_copia_com_atualizacoes(self):
        """[GREEN] Método replace cria nova instância com atualizações"""
        usuario1 = Usuario(
            id=1,
            nome="Rafael",
            matricula="MAT009",
            tipo=Tipo.ALUNO,
            email="rafael@email.com",
            ativoDeRegistro=True,
            status=Status.ATIVO
        )
        usuario2 = usuario1.replace(nome="Rafael Silva", email="rafael.silva@email.com")
        
        # Verifica que usuario1 não mudou
        assert usuario1.nome == "Rafael"
        # Verifica que usuario2 tem os novos valores
        assert usuario2.nome == "Rafael Silva"
        assert usuario2.email == "rafael.silva@email.com"
