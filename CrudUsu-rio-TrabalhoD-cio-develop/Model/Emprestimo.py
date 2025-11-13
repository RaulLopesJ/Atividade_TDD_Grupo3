from datetime import datetime, timedelta
import uuid


class EmprestimoStatus:
    """Enum simples para status de empréstimo."""
    ATIVO = "ATIVO"
    DEVOLVIDO = "DEVOLVIDO"
    ATRASADO = "ATRASADO"


class Emprestimo:
    """
    Model que representa o empréstimo de um Livro por um Usuário.
    
    Atributos:
        loan_id (str): Identificador único do empréstimo
        usuario (Usuario): Usuário que realizou o empréstimo
        livro (Livro): Livro emprestado
        loan_date (datetime): Data de empréstimo
        due_date (datetime): Data prevista de devolução
        return_date (datetime | None): Data real de devolução
        status (str): Estado do empréstimo
        fine (float): Multa, se houver
    """

    def __init__(self, usuario, livro, loan_date=None, due_date=None, return_date=None, status=None, fine=0.0, loan_id=None):
        if usuario is None or livro is None:
            raise ValueError("Usuário e Livro são obrigatórios para criar um empréstimo.")

        self.loan_id = loan_id or str(uuid.uuid4())
        self.usuario = usuario
        self.livro = livro
        self.loan_date = loan_date or datetime.now()
        self.due_date = due_date or (self.loan_date + timedelta(days=7))
        self.return_date = return_date
        self.status = status or EmprestimoStatus.ATIVO
        self.fine = fine

    # ----------------------------------------------
    # Regras de negócio
    # ----------------------------------------------

    def marcar_como_devolvido(self):
        """Finaliza o empréstimo e atualiza o status do livro."""
        self.return_date = datetime.now()
        self.status = EmprestimoStatus.DEVOLVIDO
        self.livro.status = "disponivel"
        return self

    def esta_em_atraso(self):
        """Verifica se o empréstimo está atrasado."""
        if self.status != EmprestimoStatus.ATIVO:
            return False
        return datetime.now() > self.due_date

    def calcular_multa(self, valor_por_dia=2.0):
        """Calcula multa com base nos dias de atraso."""
        if not self.esta_em_atraso():
            self.fine = 0.0
        else:
            dias_atraso = (datetime.now() - self.due_date).days
            self.fine = dias_atraso * valor_por_dia
        return self.fine

    # ----------------------------------------------
    # Serialização
    # ----------------------------------------------

    def to_dict(self):
        """Serializa o empréstimo para dicionário."""
        return {
            "loanId": self.loan_id,
            "userId": str(self.usuario.id),
            "bookId": str(self.livro.id),
            "loanDate": self.loan_date.isoformat(),
            "dueDate": self.due_date.isoformat(),
            "returnDate": self.return_date.isoformat() if self.return_date else None,
            "status": self.status,
            "fine": self.fine
        }
