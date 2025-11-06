# modulo_emprestimo.py
from datetime import datetime, timedelta
import mock_usuarios
import mock_catalogo

class Emprestimo:
    def __init__(self, user_id, book_id, loan_id, loan_date, due_date, status="ACTIVE", return_date=None, fine=0.0):
        self._user_id = user_id
        self._book_id = book_id
        self._loan_id = loan_id
        self._loan_date = loan_date
        self._due_date = due_date
        self._return_date = return_date
        self._status = status
        self._fine = fine

    def get_loan_id(self):
        return self._loan_id

    def get_user_id(self):
        return self._user_id

    def get_book_id(self):
        return self._book_id

    def get_status(self):
        return self._status

    def set_return_date(self, return_date):
        self._return_date = return_date

    def set_status(self, status):
        self._status = status

    def to_dict(self):
        return {
            "loanId": self._loan_id,
            "userId": self._user_id,
            "bookId": self._book_id,
            "loanDate": self._loan_date.isoformat(),
            "dueDate": self._due_date.isoformat(),
            "returnDate": self._return_date.isoformat() if self._return_date else None,
            "status": self._status,
            "fine": self._fine
        }

# Lista global de empréstimos (similar ao model.py)
emprestimos = []
next_loan_id = 1

# Funções auxiliares
def _calcular_due_date(data_emprestimo, tipo_usuario):
    """
    Calcula a data de devolução prevista com base no tipo de usuário.
    """
    if tipo_usuario == "professor":
        return data_emprestimo + timedelta(days=30)
    return data_emprestimo + timedelta(days=14)

# Funções principais (similar ao model.py)
def verificar_disponibilidade(book_id):
    """
    Verifica a disponibilidade de um livro.
    """
    livro = mock_catalogo.get_livro(book_id)
    if not livro:
        return {"erro": "Livro não encontrado"}
    return livro

def adicionar_emprestimo(user_id, book_id):
    """
    Adiciona um novo empréstimo ao sistema.
    """
    global next_loan_id
    
    # Validações
    usuario = mock_usuarios.get_usuario(user_id)
    if not usuario:
        return {"sucesso": False, "erro": "Usuário não encontrado"}
        
    livro = mock_catalogo.get_livro(book_id)
    if not livro:
        return {"sucesso": False, "erro": "Livro não encontrado"}
        
    if livro["status"] != "disponivel":
        return {"sucesso": False, "erro": "Livro indisponível"}

    # Criação do empréstimo
    agora = datetime.now()
    data_devolucao = _calcular_due_date(agora, usuario["tipo"])
    
    novo_emprestimo = Emprestimo(
        user_id=user_id,
        book_id=book_id,
        loan_id=next_loan_id,
        loan_date=agora,
        due_date=data_devolucao
    )
    
    emprestimos.append(novo_emprestimo)
    next_loan_id += 1
    
    # Atualiza status do livro
    mock_catalogo.update_status_livro(book_id, "emprestado")
    
    return {"sucesso": True, "loan": novo_emprestimo.to_dict()}

def registrar_devolucao(loan_id):
    """
    Registra a devolução de um livro.
    """
    emprestimo = None
    for emp in emprestimos:
        if emp.get_loan_id() == loan_id:
            emprestimo = emp
            break
    
    if not emprestimo:
        return {"sucesso": False, "erro": "Empréstimo não encontrado"}
        
    if emprestimo.get_status() != "ACTIVE":
        return {"sucesso": False, "erro": "Empréstimo já devolvido"}
    
    # Atualiza o empréstimo
    agora = datetime.now()
    emprestimo.set_return_date(agora)
    emprestimo.set_status("RETURNED")
    
    # Atualiza o status do livro
    mock_catalogo.update_status_livro(emprestimo.get_book_id(), "disponivel")
    
    return {"sucesso": True, "loan": emprestimo.to_dict()}

def get_emprestimos():
    """
    Retorna lista de todos os empréstimos.
    """
    return [emp.to_dict() for emp in emprestimos]

def get_emprestimo_by_id(loan_id):
    """
    Busca um empréstimo específico pelo ID.
    """
    for emp in emprestimos:
        if emp.get_loan_id() == loan_id:
            return emp.to_dict()
    return None