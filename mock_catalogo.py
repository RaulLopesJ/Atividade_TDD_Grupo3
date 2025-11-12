"""Mock de catálogo - simula um banco de dados de livros."""

# Base de dados simulada de livros
_catalogo_db = {
    1: {"bookId": 1, "titulo": "Engenharia de Software", "autor": "Sommerville", "status": "disponivel"},
    2: {"bookId": 2, "titulo": "Banco de Dados", "autor": "Date", "status": "disponivel"},
    3: {"bookId": 3, "titulo": "IA Moderna", "autor": "Russell", "status": "disponivel"},
}


def get_livro(book_id):
    """
    Retorna os dados do livro ou None se não encontrado.
    
    Args:
        book_id: ID do livro a buscar
        
    Returns:
        dict com dados do livro ou None
    """
    return _catalogo_db.get(book_id)


def livro_existe(book_id):
    """
    Verifica se um livro existe.
    
    Args:
        book_id: ID do livro
        
    Returns:
        True se existe, False caso contrário
    """
    return book_id in _catalogo_db


def update_status_livro(book_id, novo_status):
    """
    Atualiza o status de um livro (disponivel ou emprestado).
    
    Args:
        book_id: ID do livro
        novo_status: novo status ('disponivel' ou 'emprestado')
        
    Returns:
        True se atualizado com sucesso, False se livro não existe
    """
    if book_id in _catalogo_db:
        _catalogo_db[book_id]["status"] = novo_status
        return True
    return False


def adicionar_livro(book_id, titulo, autor, status="disponivel"):
    """
    Adiciona um novo livro ao catálogo.
    
    Args:
        book_id: ID do livro
        titulo: Título do livro
        autor: Autor do livro
        status: status inicial (padrão: 'disponivel')
    """
    _catalogo_db[book_id] = {
        "bookId": book_id,
        "titulo": titulo,
        "autor": autor,
        "status": status
    }


def listar_livros():
    """Retorna lista de todos os livros."""
    return list(_catalogo_db.values())


def listar_livros_disponiveis():
    """Retorna apenas livros disponíveis."""
    return [l for l in _catalogo_db.values() if l["status"] == "disponivel"]


def limpar_catalogo():
    """Limpa todo o catálogo (útil para testes)."""
    _catalogo_db.clear()