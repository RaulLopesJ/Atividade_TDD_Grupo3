"""Controller refatorado: delega a lógica para o módulo de modelo `modulo_emprestimo`.

O Controller mantém a interface esperada pela View e pelos testes, mas não
reimplementa regras de negócio. Isso evita duplicação e mantém o modelo como
fonte única da verdade.
"""

import modulo_emprestimo


class Controller:
    def __init__(self):
        # Não mantemos estado local de empréstimos aqui. O estado é mantido
        # em `modulo_emprestimo`.
        pass

    def verificar_disponibilidade(self, book_id):
        """Retorna informações do livro (ou dicionário de erro) delegando ao model."""
        return modulo_emprestimo.verificar_disponibilidade(book_id)

    def registrar_emprestimo(self, user_id, book_id):
        """Tenta criar um empréstimo delegando ao model."""
        return modulo_emprestimo.adicionar_emprestimo(user_id, book_id)

    def registrar_devolucao(self, loan_id):
        """Registra devolução delegando ao model."""
        return modulo_emprestimo.registrar_devolucao(loan_id)

    def get_emprestimos(self):
        """Retorna a lista de empréstimos (representada pelo model)."""
        return modulo_emprestimo.get_emprestimos()

    def run(self, debug=True, port=5000):
        # Método de conveniência para compatibilidade com a API anterior.
        # Se a aplicação Web usar Flask/Outra lib, aqui seria o ponto de integração.
        if hasattr(self, 'app'):
            self.app.run(debug=debug, port=port)


# Instância global do controller (compatibilidade)
controller = Controller()
