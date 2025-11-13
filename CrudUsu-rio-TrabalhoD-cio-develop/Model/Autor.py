"""
Model: Autor
Módulo 2 - Catálogo de Livros (Autores)

Classe que representa um autor no catálogo de livros.
Implementado com TDD (Test Driven Development).
"""

import uuid


class Autor:
    """
    Classe que representa um autor no catálogo.
    
    Atributos:
        id (int): Identificador único do autor
        nome (str): Nome do autor (obrigatório, mínimo 3 caracteres)
        nacionalidade (str): País/Nacionalidade do autor
        biografia (str): Breve descrição do autor
    """
    
    def __init__(self, id, nome, nacionalidade, biografia):
        """
        Inicializa um novo autor com validações.
        
        Args:
            id: Identificador do autor
            nome: Nome do autor (mínimo 3 caracteres)
            nacionalidade: Nacionalidade do autor
            biografia: Biografia do autor
            
        Raises:
            ValueError: Se nome estiver vazio ou tiver menos de 3 caracteres
        """
        self._validar_nome(nome)
        
        self.id = id if id is not None else uuid.uuid4()
        self.nome = nome
        self.nacionalidade = nacionalidade
        self.biografia = biografia
    
    @staticmethod
    def _validar_nome(nome):
        """Valida se o nome é válido"""
        if not nome or not nome.strip():
            raise ValueError("Nome é obrigatório")
        if len(nome.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
    
    def get_id(self):
        return self.id
    
    def get_nome(self):
        return self.nome
    
    def set_nome(self, nome):
        self._validar_nome(nome)
        self.nome = nome
    
    def get_nacionalidade(self):
        return self.nacionalidade
    
    def set_nacionalidade(self, nacionalidade):
        self.nacionalidade = nacionalidade
    
    def get_biografia(self):
        return self.biografia
    
    def set_biografia(self, biografia):
        self.biografia = biografia
    
    def replace(self, **kwargs):
        """Cria uma nova instância com os campos atualizados"""
        novo_id = kwargs.get('id', self.id)
        novo_nome = kwargs.get('nome', self.nome)
        nova_nacionalidade = kwargs.get('nacionalidade', self.nacionalidade)
        nova_biografia = kwargs.get('biografia', self.biografia)
        
        return Autor(
            id=novo_id,
            nome=novo_nome,
            nacionalidade=nova_nacionalidade,
            biografia=nova_biografia
        )
