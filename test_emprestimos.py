# test_emprestimos.py
import unittest
from datetime import datetime, timedelta
import modulo_emprestimo
import mock_usuarios
import mock_catalogo
import controler

class TestEmprestimos(unittest.TestCase):
    def setUp(self):
        """Executado ANTES de CADA teste."""
        # Reseta o estado global do módulo
        modulo_emprestimo.emprestimos = []
        modulo_emprestimo.next_loan_id = 1
        self.controller = controler.Controller()
        
        # Reseta o estado do mock do catálogo
        mock_catalogo._catalogo_db = {
            1: {"bookId": 1, "titulo": "Engenharia de Software", "status": "disponivel"},
            2: {"bookId": 2, "titulo": "Banco de Dados", "status": "emprestado"},
            3: {"bookId": 3, "titulo": "IA", "status": "disponivel"},
        }

    def tearDown(self):
        """Executado DEPOIS de CADA teste."""
        # Limpa os empréstimos após cada teste
        modulo_emprestimo.emprestimos = []

    # ================================================
    # TESTES UNITÁRIOS
    # ================================================

    # --- Testes do Modelo ---
    def test_unit_criar_emprestimo(self):
        """Testa a criação de um objeto Emprestimo"""
        agora = datetime.now()
        emprestimo = modulo_emprestimo.Emprestimo(
            user_id=1,
            book_id=1,
            loan_id=1,
            loan_date=agora,
            due_date=agora + timedelta(days=14)
        )
        
        self.assertEqual(emprestimo.get_user_id(), 1)
        self.assertEqual(emprestimo.get_book_id(), 1)
        self.assertEqual(emprestimo.get_status(), "ACTIVE")

    # --- Testes de verificar_disponibilidade ---
    def test_unit_verificar_disponibilidade_disponivel(self):
        resultado = self.controller.verificar_disponibilidade(1)
        self.assertEqual(resultado, {"bookId": 1, "titulo": "Engenharia de Software", "status": "disponivel"})

    def test_unit_verificar_disponibilidade_emprestado(self):
        resultado = self.controller.verificar_disponibilidade(2)
        self.assertEqual(resultado, {"bookId": 2, "titulo": "Banco de Dados", "status": "emprestado"})

    def test_unit_verificar_disponibilidade_inexistente(self):
        resultado = self.controller.verificar_disponibilidade(999)
        self.assertEqual(resultado, {"erro": "Livro não encontrado"})

    # --- Testes de registrar_emprestimo (Falha) ---
    def test_unit_registrar_emprestimo_usuario_inexistente(self):
        res = self.controller.registrar_emprestimo(user_id=999, book_id=1)
        self.assertFalse(res["sucesso"])
        self.assertEqual(res["erro"], "Usuário não encontrado")
        
    def test_unit_registrar_emprestimo_livro_inexistente(self):
        res = self.controller.registrar_emprestimo(user_id=1, book_id=999)
        self.assertFalse(res["sucesso"])
        self.assertEqual(res["erro"], "Livro não encontrado")

    def test_unit_registrar_emprestimo_livro_indisponivel(self):
        res = self.controller.registrar_emprestimo(user_id=1, book_id=2)
        self.assertFalse(res["sucesso"])
        self.assertEqual(res["erro"], "Livro indisponível")

    # --- Teste de registrar_emprestimo (Sucesso) ---
    def test_unit_registrar_emprestimo_sucesso(self):
        # Verifica o estado inicial do livro
        livro_antes = mock_catalogo.get_livro(3)  # Usa o livro 3 que sabemos que está disponível
        self.assertEqual(livro_antes["status"], "disponivel")
        
        # Tenta registrar o empréstimo
        res = self.controller.registrar_emprestimo(user_id=1, book_id=3)
        
        # Verifica o sucesso da operação
        self.assertTrue(res["sucesso"], "O empréstimo deveria ter sido bem-sucedido")
        
        # Verifica os dados do empréstimo
        loan = res["loan"]
        self.assertEqual(loan["userId"], 1)
        self.assertEqual(loan["bookId"], 3)
        self.assertEqual(loan["status"], "ACTIVE")
        
        # Verifica se o empréstimo foi adicionado à lista
        emprestimos = self.controller.get_emprestimos()
        self.assertEqual(len(emprestimos), 1)
        self.assertEqual(emprestimos[0]["status"], "ACTIVE")
        
        # Verifica se o status do livro foi atualizado
        livro_depois = mock_catalogo.get_livro(3)
        self.assertEqual(livro_depois["status"], "emprestado")

    # --- Testes de registrar_devolucao ---
    def test_unit_registrar_devolucao_inexistente(self):
        res = self.controller.registrar_devolucao(loan_id=999)
        self.assertFalse(res["sucesso"])
        self.assertEqual(res["erro"], "Empréstimo não encontrado")

    def test_unit_registrar_devolucao_ja_devolvido(self):
        # Primeiro registra um empréstimo
        res_emp = self.controller.registrar_emprestimo(user_id=1, book_id=1)
        loan_id = res_emp["loan"]["loanId"]
        
        # Devolve uma vez
        self.controller.registrar_devolucao(loan_id)
        
        # Tenta devolver novamente
        res = self.controller.registrar_devolucao(loan_id)
        self.assertFalse(res["sucesso"])
        self.assertEqual(res["erro"], "Empréstimo já devolvido")

    def test_unit_registrar_devolucao_sucesso(self):
        # Primeiro registra um empréstimo
        res_emp = self.controller.registrar_emprestimo(user_id=1, book_id=3)  # Usa o livro 3 que está disponível
        self.assertTrue(res_emp["sucesso"], "Falha ao registrar empréstimo inicial")
        loan_id = res_emp["loan"]["loanId"]
        
        # Então tenta devolver
        res = self.controller.registrar_devolucao(loan_id)
        self.assertTrue(res["sucesso"], "Falha ao registrar devolução")
        self.assertEqual(res["loan"]["status"], "RETURNED")
        self.assertIsNotNone(res["loan"]["returnDate"])

    # ================================================
    # TESTES DE INTEGRAÇÃO
    # ================================================

    def test_integracao_fluxo_emprestimo_completo(self):
        """Testa o fluxo completo de empréstimo e devolução"""
        # 1. Verifica disponibilidade do livro
        resultado = self.controller.verificar_disponibilidade(1)
        self.assertEqual(resultado["status"], "disponivel")

        # 2. Registra o empréstimo
        res_emp = self.controller.registrar_emprestimo(user_id=1, book_id=1)
        self.assertTrue(res_emp["sucesso"])
        loan_id = res_emp["loan"]["loanId"]

        # 3. Verifica se o livro agora está emprestado
        resultado = self.controller.verificar_disponibilidade(1)
        self.assertEqual(resultado["status"], "emprestado")

        # 4. Registra a devolução
        res_dev = self.controller.registrar_devolucao(loan_id)
        self.assertTrue(res_dev["sucesso"])

        # 5. Verifica se o livro voltou a ficar disponível
        resultado = self.controller.verificar_disponibilidade(1)
        self.assertEqual(resultado["status"], "disponivel")

    def test_integracao_verificacao_usuario(self):
        """Testa a integração com o módulo de usuários"""
        # Tenta emprestar com usuário válido
        res1 = self.controller.registrar_emprestimo(user_id=1, book_id=3)  # Usa o livro 3 que está disponível
        self.assertTrue(res1["sucesso"])

        # Tenta emprestar com usuário inválido
        res2 = self.controller.registrar_emprestimo(user_id=999, book_id=1)
        self.assertFalse(res2["sucesso"])
        self.assertEqual(res2["erro"], "Usuário não encontrado")

    def test_integracao_verificacao_livro(self):
        """Testa a integração com o módulo de catálogo"""
        # Tenta emprestar livro disponível
        res1 = self.controller.registrar_emprestimo(user_id=1, book_id=3)  # Usa o livro 3 que está disponível
        self.assertTrue(res1["sucesso"])

        # Tenta emprestar livro já emprestado
        res2 = self.controller.registrar_emprestimo(user_id=2, book_id=2)  # Usa o livro 2 que já está emprestado
        self.assertFalse(res2["sucesso"])
        self.assertEqual(res2["erro"], "Livro indisponível")

        # Tenta emprestar livro inexistente
        res3 = self.controller.registrar_emprestimo(user_id=1, book_id=999)
        self.assertFalse(res3["sucesso"])
        self.assertEqual(res3["erro"], "Livro não encontrado")

if __name__ == '__main__':
    unittest.main()
    # ================================================

    def test_contrato_calcular_due_date_aluno(self):
        data_base = datetime(2025, 10, 1, 10, 0, 0)
        data_esperada = data_base + timedelta(days=14)
        resultado = modulo_emprestimo._calcular_due_date(data_base, "aluno")
        self.assertEqual(resultado, data_esperada)

    def test_contrato_calcular_due_date_professor(self):
        data_base = datetime(2025, 10, 1, 10, 0, 0)
        data_esperada = data_base + timedelta(days=30)
        resultado = modulo_emprestimo._calcular_due_date(data_base, "professor")
        self.assertEqual(resultado, data_esperada)

    def test_contrato_registrar_emprestimo_atualiza_catalogo(self):
        status_antes = mock_catalogo.get_livro(3)["status"]
        self.assertEqual(status_antes, "disponivel")
        modulo_emprestimo.registrar_emprestimo(user_id=1, book_id=3)
        status_depois = mock_catalogo.get_livro(3)["status"]
        self.assertEqual(status_depois, "emprestado")
        
    def test_contrato_registrar_devolucao_atualiza_catalogo(self):
        db_fake = [{"loanId": 102, "userId": 1, "bookId": 2, "status": "ACTIVE"}]
        modulo_emprestimo._save_db(db_fake)
        self.assertEqual(mock_catalogo.get_livro(2)["status"], "emprestado")
        modulo_emprestimo.registrar_devolucao(loan_id=102)
        self.assertEqual(mock_catalogo.get_livro(2)["status"], "disponivel")

    def test_contrato_formato_datas_iso_8601(self):
        modulo_emprestimo.registrar_emprestimo(user_id=1, book_id=1)
        db = modulo_emprestimo._load_db()
        loan = db[0]
        try:
            datetime.fromisoformat(loan["loanDate"])
            datetime.fromisoformat(loan["dueDate"])
        except ValueError:
            self.fail("Datas não estão em formato ISO 8601 válido")
        self.assertIsNone(loan["returnDate"])