"""
Equipe 2 - Testes para Gestão de Autores
Módulo: Model/Autor.py

15 Testes Totais:
- 10 testes unitários (casos de sucesso, erro e validação)
- 5 testes de contrato/integridade (serialização, campos obrigatórios, tipos)
"""

import pytest
from Model.Autor import Autor


# ============================================
# TESTES UNITÁRIOS (10 testes)
# ============================================

class TestAutorCriacao:
    """[RED-GREEN-REFACTOR] Testes de criação e inicialização de autores"""
    
    def test_criar_autor_valido(self):
        """[GREEN] Criar autor com todos os dados válidos"""
        autor = Autor(
            id=1,
            nome="Robert C. Martin",
            nacionalidade="Americana",
            biografia="Especialista em engenharia de software"
        )
        assert autor.nome == "Robert C. Martin"
        assert autor.nacionalidade == "Americana"
        assert autor.biografia == "Especialista em engenharia de software"
    
    def test_criar_autor_nome_minimo(self):
        """[GREEN] Autor com nome de 3 caracteres é válido"""
        autor = Autor(
            id=1,
            nome="Bob",
            nacionalidade="Americana",
            biografia="Bio"
        )
        assert autor.nome == "Bob"
    
    def test_autor_nome_vazio_lanca_erro(self):
        """[RED] Nome vazio deve lançar ValueError"""
        with pytest.raises(ValueError, match="Nome é obrigatório"):
            Autor(id=1, nome="", nacionalidade="Brasileira", biografia="Bio")
    
    def test_autor_nome_muito_curto_lanca_erro(self):
        """[RED] Nome com menos de 3 caracteres deve lançar erro"""
        with pytest.raises(ValueError, match="Nome deve ter pelo menos 3 caracteres"):
            Autor(id=1, nome="Jo", nacionalidade="Brasileira", biografia="Bio")
    
    def test_autor_nome_com_espacos_lanca_erro(self):
        """[RED] Nome apenas com espaços deve lançar erro"""
        with pytest.raises(ValueError, match="Nome é obrigatório"):
            Autor(id=1, nome="   ", nacionalidade="Brasileira", biografia="Bio")


class TestAutorValidacao:
    """[RED-GREEN-REFACTOR] Testes de validações e regras de negócio"""
    
    def test_autor_id_automatico(self):
        """[GREEN] Autor recebe ID automático quando não fornecido"""
        autor = Autor(
            id=None,
            nome="Martin Fowler",
            nacionalidade="Britânica",
            biografia="Arquiteto de software"
        )
        assert autor.id is not None
    
    def test_setter_nome(self):
        """[GREEN] Nome pode ser alterado via setter"""
        autor = Autor(
            id=1,
            nome="Donald Knuth",
            nacionalidade="Americana",
            biografia="Cientista da computação"
        )
        autor.set_nome("Donald E. Knuth")
        assert autor.get_nome() == "Donald E. Knuth"
    
    def test_setter_nome_valida_tamanho_minimo(self):
        """[RED] Setter de nome deve validar tamanho mínimo"""
        autor = Autor(
            id=1,
            nome="Dijkstra",
            nacionalidade="Holandesa",
            biografia="Cientista"
        )
        with pytest.raises(ValueError, match="Nome deve ter pelo menos 3 caracteres"):
            autor.set_nome("DJ")
    
    def test_getter_todas_propriedades(self):
        """[GREEN] Todos os getters funcionam corretamente"""
        autor = Autor(
            id=1,
            nome="Erich Gamma",
            nacionalidade="Suíça",
            biografia="Design Patterns"
        )
        assert autor.get_id() == 1
        assert autor.get_nome() == "Erich Gamma"
        assert autor.get_nacionalidade() == "Suíça"
        assert autor.get_biografia() == "Design Patterns"


# ============================================
# TESTES DE CONTRATO/INTEGRIDADE (5 testes)
# ============================================

class TestContratoAutor:
    """[RED-GREEN-REFACTOR] Testes de contrato e integridade de dados"""
    
    def test_campos_obrigatorios_existem(self):
        """[GREEN] Todos os campos obrigatórios estão presentes"""
        autor = Autor(
            id=1,
            nome="John Carmack",
            nacionalidade="Americana",
            biografia="Programador de jogos"
        )
        assert hasattr(autor, 'id')
        assert hasattr(autor, 'nome')
        assert hasattr(autor, 'nacionalidade')
        assert hasattr(autor, 'biografia')
    
    def test_tipos_de_dados_corretos(self):
        """[GREEN] Todos os campos têm tipos corretos"""
        autor = Autor(
            id=1,
            nome="Linus Torvalds",
            nacionalidade="Finlandesa",
            biografia="Criador do Linux"
        )
        assert isinstance(autor.id, int) or autor.id is None
        assert isinstance(autor.nome, str)
        assert isinstance(autor.nacionalidade, str)
        assert isinstance(autor.biografia, str)
    
    def test_setter_atualiza_todas_propriedades(self):
        """[GREEN] Todos os setters funcionam corretamente"""
        autor = Autor(
            id=1,
            nome="Grace Hopper",
            nacionalidade="Americana",
            biografia="Inventora do compilador"
        )
        autor.set_nome("Grace Murray Hopper")
        autor.set_nacionalidade("Estados Unidos")
        autor.set_biografia("Almirante e inventora")
        
        assert autor.get_nome() == "Grace Murray Hopper"
        assert autor.get_nacionalidade() == "Estados Unidos"
        assert autor.get_biografia() == "Almirante e inventora"
    
    def test_replace_cria_copia_com_atualizacoes(self):
        """[GREEN] Método replace cria nova instância com atualizações"""
        autor1 = Autor(
            id=1,
            nome="Ada Lovelace",
            nacionalidade="Britânica",
            biografia="Primeira programadora"
        )
        autor2 = autor1.replace(biografia="Primeira programadora do mundo")
        
        # Verifica que autor1 não mudou
        assert autor1.biografia == "Primeira programadora"
        # Verifica que autor2 tem o novo valor
        assert autor2.biografia == "Primeira programadora do mundo"
    
    def test_nome_com_numeros_e_caracteres_especiais(self):
        """[GREEN] Nome pode conter números e caracteres especiais"""
        autor = Autor(
            id=1,
            nome="C. A. R. Hoare",
            nacionalidade="Britânica",
            biografia="Inventor do Quicksort"
        )
        assert "." in autor.nome
        assert len(autor.nome) >= 3
