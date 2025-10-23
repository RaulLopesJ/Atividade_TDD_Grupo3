# modulo_emprestimo.py
import json
import os
from datetime import datetime, timedelta

# Importa os MÓDULOS das outras equipes (neste caso, nossos mocks)
import mock_usuarios
import mock_catalogo

# Define o arquivo que servirá como nosso banco de dados
DB_FILE = 'emprestimos.json'

# --- Funções de Persistência de Dados (Base) ---

def _load_db():
    """Carrega os dados do nosso "banco de dados" JSON."""
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _save_db(data):
    """Salva os dados no nosso "banco de dados" JSON."""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def _get_next_loan_id():
    """Gera um novo ID auto-incrementado"""
    db = _load_db()
    if not db:
        return 1
    return max(item.get('loanId', 0) for item in db) + 1

# ================================================
# NOSSAS FUNÇÕES (GREEN)
# ================================================

def verificar_disponibilidade(book_id):
    """
    Verifica a disponibilidade de um livro consultando o módulo de Catálogo. 
    """
    livro = mock_catalogo.get_livro(book_id)
    if not livro:
        return {"erro": "Livro não encontrado"}
    return livro

def _calcular_due_date(data_emprestimo, tipo_usuario):
    """
    Calcula a data de devolução prevista com base no tipo de usuário.
    Regras: aluno=14 dias, professor=30 dias, funcionario=14 dias.
    """
    if tipo_usuario == "professor":
        return data_emprestimo + timedelta(days=30)
    
    # "aluno" e "funcionario" (e outros) caem na regra padrão de 14 dias
    return data_emprestimo + timedelta(days=14)

def registrar_emprestimo(user_id, book_id):
    """
    Registra um novo empréstimo, validando com os módulos de Usuário e Catálogo. 
    """
    # 1. Validações (Integração de Leitura)
    usuario = mock_usuarios.get_usuario(user_id)
    if not usuario:
        return {"sucesso": False, "erro": "Usuário não encontrado"}
    livro = mock_catalogo.get_livro(book_id)
    if not livro:
        return {"sucesso": False, "erro": "Livro não encontrado"}
    if livro["status"] != "disponivel":
        return {"sucesso": False, "erro": "Livro indisponível"}
    
    # --- CAMINHO FELIZ ---
    
    # 2. Lógica de Negócio e Dados
    agora = datetime.now()
    data_devolucao_prevista = _calcular_due_date(agora, usuario["tipo"])
    
    novo_emprestimo = {
        "loanId": _get_next_loan_id(),
        "userId": user_id,
        "bookId": book_id,
        "loanDate": agora.isoformat(),
        "dueDate": data_devolucao_prevista.isoformat(),
        "returnDate": None,
        "status": "ACTIVE",
        "fine": 0.0
    }
    
    # 3. Persistência (Salva no nosso JSON)
    db = _load_db()
    db.append(novo_emprestimo)
    _save_db(db)
    
    # 4. Atualiza o Módulo de Catálogo (Integração de Escrita Equipe 3 -> 2)
    mock_catalogo.update_status_livro(book_id, "emprestado")
    
    return {"sucesso": True, "loan": novo_emprestimo}


def registrar_devolucao(loan_id):
    """
    Registra a devolução de um livro. 
    """
    db = _load_db()
    
    emprestimo_encontrado = None
    index_emprestimo = -1
    
    for i, emp in enumerate(db):
        if emp["loanId"] == loan_id:
            emprestimo_encontrado = emp
            index_emprestimo = i
            break
    
    # 1. Valida Empréstimo
    if not emprestimo_encontrado:
        return {"sucesso": False, "erro": "Empréstimo não encontrado"}

    # 2. Valida Status
    if emprestimo_encontrado["status"] != "ACTIVE":
        return {"sucesso": False, "erro": "Empréstimo já devolvido"}

    # --- CAMINHO FELIZ ---
    
    # 3. Lógica de Negócio
    agora = datetime.now()
    emprestimo_encontrado["status"] = "RETURNED"
    emprestimo_encontrado["returnDate"] = agora.isoformat()
    
    # (Lógica de multa 'fine' poderia ser adicionada aqui)
    
    # 4. Persistência
    db[index_emprestimo] = emprestimo_encontrado
    _save_db(db)
    
    # 5. Atualiza o Módulo de Catálogo (Integração de Escrita Equipe 3 -> 2)
    mock_catalogo.update_status_livro(emprestimo_encontrado["bookId"], "disponivel")

    return {"sucesso": True, "loan": emprestimo_encontrado}