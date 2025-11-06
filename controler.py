from datetime import datetime, timedelta
import mock_usuarios
import mock_catalogo

class Controller:
    def __init__(self):
        self._emprestimos = []
        self._next_loan_id = 1

    def verificar_disponibilidade(self, book_id):
        livro = mock_catalogo.get_livro(book_id)
        if not livro:
            return {"erro": "Livro não encontrado"}
        return livro

    def _calcular_due_date(self, data_emprestimo, tipo_usuario):
        if tipo_usuario == "professor":
            return data_emprestimo + timedelta(days=30)
        return data_emprestimo + timedelta(days=14)

    def registrar_emprestimo(self, user_id, book_id):
        usuario = mock_usuarios.get_usuario(user_id)
        if not usuario:
            return {"sucesso": False, "erro": "Usuário não encontrado"}
            
        livro = mock_catalogo.get_livro(book_id)
        if not livro:
            return {"sucesso": False, "erro": "Livro não encontrado"}
            
        if livro["status"] != "disponivel":
            return {"sucesso": False, "erro": "Livro indisponível"}

        agora = datetime.now()
        data_devolucao_prevista = self._calcular_due_date(agora, usuario["tipo"])

        novo_emprestimo = {
            "loanId": self._next_loan_id,
            "userId": user_id,
            "bookId": book_id,
            "loanDate": agora.isoformat(),
            "dueDate": data_devolucao_prevista.isoformat(),
            "returnDate": None,
            "status": "ACTIVE",
            "fine": 0.0
        }

        self._emprestimos.append(novo_emprestimo)
        self._next_loan_id += 1
        mock_catalogo.update_status_livro(book_id, "emprestado")

        return {"sucesso": True, "loan": novo_emprestimo}

    def registrar_devolucao(self, loan_id):
        emprestimo_encontrado = None
        for emp in self._emprestimos:
            if emp["loanId"] == loan_id:
                emprestimo_encontrado = emp
                break

        if not emprestimo_encontrado:
            return {"sucesso": False, "erro": "Empréstimo não encontrado"}

        if emprestimo_encontrado["status"] != "ACTIVE":
            return {"sucesso": False, "erro": "Empréstimo já devolvido"}

        agora = datetime.now()
        emprestimo_encontrado["status"] = "RETURNED"
        emprestimo_encontrado["returnDate"] = agora.isoformat()

        mock_catalogo.update_status_livro(emprestimo_encontrado["bookId"], "disponivel")

        return {"sucesso": True, "loan": emprestimo_encontrado}

    def get_emprestimos(self):
        return self._emprestimos

    def run(self, debug=True, port=5000):
        self.app.run(debug=debug, port=port)

# Instância global do controller
controller = Controller()

if __name__ == '__main__':
    controller.run()