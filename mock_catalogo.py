# mock_catalogo.py
# Simula o CRUD de livros da Equipe 2 

# Dados falsos para teste
_catalogo_db = {
    1: {"bookId": 1, "titulo": "Engenharia de Software", "status": "disponivel"},
    2: {"bookId": 2, "titulo": "Banco de Dados", "status": "emprestado"},
    3: {"bookId": 3, "titulo": "IA", "status": "disponivel"},
}

def get_livro(book_id):
    """Simula a busca de um livro."""
    return _catalogo_db.get(book_id, None)

def update_status_livro(book_id, novo_status):
    """Simula a atualização do status de um livro."""
    if book_id in _catalogo_db:
        _catalogo_db[book_id]["status"] = novo_status
        # print(f"[Mock Catalogo] Status do livro {book_id} atualizado para {novo_status}")
        return True
    return False
    