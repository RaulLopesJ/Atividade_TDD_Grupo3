"""
Módulo de gerenciamento de livros - Catálogo da Biblioteca
Equipe 2 - Sistema de Gestão de Biblioteca Universitária (SGBU)

Este módulo fornece funcionalidades completas de CRUD para o catálogo de livros,
incluindo validações, controle de status e persistência em memória.
"""

from typing import List, Optional


# ==================== Constantes ====================

STATUS_DISPONIVEL = "disponivel"
STATUS_EMPRESTADO = "emprestado"


# ==================== Banco de Dados (Memória) ====================

_db_livros: List['Livro'] = []


def _limpar_db() -> None:
    """
    Limpa toda a base de dados de livros.
    
    Nota: Função interna utilizada principalmente para testes.
    """
    _db_livros.clear()


# ==================== Classe Livro ====================

class Livro:
    """
    Representa um livro no catálogo da biblioteca.
    
    Attributes:
        titulo (str): Título do livro
        autor (str): Nome do autor
        isbn (str): Código ISBN do livro
        status (str): Status atual do livro ('disponivel' ou 'emprestado')
    
    Raises:
        ValueError: Se algum campo obrigatório estiver vazio
    """
    
    def __init__(self, id, titulo: str, autor: str, isbn: str) -> None:
        """
        Inicializa um novo livro com validações.
        
        Args:
            titulo: Título do livro (obrigatório)
            autor: Nome do autor (obrigatório)
            isbn: Código ISBN (obrigatório)
        
        Raises:
            ValueError: Se titulo, autor ou isbn estiverem vazios
        """
        self._validar_campo(titulo, "Título")
        self._validar_campo(autor, "Autor")
        self._validar_campo(isbn, "ISBN")
        
        self.id = id  
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.status = STATUS_DISPONIVEL
    
    @staticmethod
    def _validar_campo(valor: str, nome_campo: str) -> None:
        """
        Valida se um campo não está vazio.
        
        Args:
            valor: Valor a ser validado
            nome_campo: Nome do campo para mensagem de erro
        
        Raises:
            ValueError: Se o valor estiver vazio
        """
        if not valor or not valor.strip():
            raise ValueError(f"{nome_campo} é obrigatório")
    
    def emprestar(self) -> None:
        """
        Marca o livro como emprestado.
        """
        self.status = STATUS_EMPRESTADO
    
    def devolver(self) -> None:
        """
        Marca o livro como disponível (devolução).
        """
        self.status = STATUS_DISPONIVEL
    
    def esta_disponivel(self) -> bool:
        """
        Verifica se o livro está disponível para empréstimo.
        
        Returns:
            bool: True se disponível, False caso contrário
        """
        return self.status == STATUS_DISPONIVEL
    
    def __repr__(self) -> str:
        """
        Representação legível do objeto Livro.
        
        Returns:
            str: Representação formatada do livro
        """
        return f"Livro(id='{self.id}', titulo='{self.titulo}', autor='{self.autor}', isbn='{self.isbn}', status='{self.status}')"
