# test_emprestimos.py
import unittest
import os
import json
from datetime import datetime, timedelta
import modulo_emprestimo
# Importa os MÓDULOS das outras equipes (neste caso, nossos mocks)
import mock_usuarios
import mock_catalogo

# Define um "banco de dados" SÓ PARA TESTES
TEST_DB_FILE = 'test_emprestimos.json'

class TestEmprestimos(unittest.TestCase):

    def setUp(self):
        """ Executado ANTES de CADA teste. """
        modulo_emprestimo.DB_FILE = TEST_DB_FILE
        self.clear_db()

    def tearDown(self):
        """ Executado DEPOIS de CADA teste. """
        self.clear_db()

    def clear_db(self):
        """Função auxiliar para limpar o DB de teste."""
        if os.path.exists(TEST_DB_FILE):
            os.remove(TEST_DB_FILE)
        with open(TEST_DB_FILE, 'w') as f:
            json.dump([], f)

    # ================================================
    # TESTES UNITÁRIOS (10)
    # ================================================

    # --- Testes de verificar_disponibilidade ---
    def test_unit_verificar_disponibilidade_disponivel(self):
        resultado = modulo_emprestimo.verificar_disponibilidade(1)
        self.assertEqual(resultado, {"bookId": 1, "titulo": "Engenharia de Software", "status": "disponivel"})

    def test_unit_verificar_disponibilidade_emprestado(self):
        resultado = modulo_emprestimo.verificar_disponibilidade(2)
        self.assertEqual(resultado, {"bookId": 2, "titulo": "Banco de Dados", "status": "emprestado"})

    def test_unit_verificar_disponibilidade_inexistente(self):
        resultado = modulo_emprestimo.verificar_disponibilidade(999)
        self.assertEqual(resultado, {"erro": "Livro não encontrado"})

    # --- Testes de registrar_emprestimo (Falha) ---
    def test_unit_registrar_emprestimo_usuario_inexistente(self):
        res = modulo_emprestimo.registrar_emprestimo(user_id=999, book_id=1)
        self.assertFalse(res["sucesso"])
        self.assertEqual(res["erro"], "Usuário não encontrado")
        
    def test_unit_registrar_emprestimo_livro_inexistente(self):
        res = modulo_emprestimo.registrar_emprestimo(user_id=1, book_id=999)
        self.assertFalse(res["sucesso"])
        self.assertEqual(res["erro"], "Livro não encontrado")

    def test_unit_registrar_emprestimo_livro_indisponivel(self):
        res = modulo_emprestimo.registrar_emprestimo(user_id=1, book_id=2)
        self.assertFalse(res["sucesso"])
        self.assertEqual(res["erro"], "Livro indisponível")

    # --- Teste de registrar_emprestimo (Sucesso) ---
    def test_unit_registrar_emprestimo_sucesso(self):
        res = modulo_emprestimo.registrar_emprestimo(user_id=1, book_id=1)
        self.assertTrue(res["sucesso"])
        self.assertEqual(res["loan"]["userId"], 1)
        self.assertEqual(res["loan"]["bookId"], 1)
        self.assertEqual(res["loan"]["status"], "ACTIVE")
        db = modulo_emprestimo._load_db()
        self.assertEqual(len(db), 1)
        self.assertEqual(db[0]["status"], "ACTIVE")

    # --- Testes de registrar_devolucao ---
    def test_unit_registrar_devolucao_inexistente(self):
        res = modulo_emprestimo.registrar_devolucao(loan_id=999)
        self.assertFalse(res["sucesso"])
        self.assertEqual(res["erro"], "Empréstimo não encontrado")

    def test_unit_registrar_devolucao_ja_devolvido(self):
        db_fake = [{"loanId": 100, "status": "RETURNED"}]
        modulo_emprestimo._save_db(db_fake)
        res = modulo_emprestimo.registrar_devolucao(loan_id=100)
        self.assertFalse(res["sucesso"])
        self.assertEqual(res["erro"], "Empréstimo já devolvido")

    def test_unit_registrar_devolucao_sucesso(self):
        db_fake = [{"loanId": 101, "userId": 1, "bookId": 1, "status": "ACTIVE"}]
        modulo_emprestimo._save_db(db_fake)
        res = modulo_emprestimo.registrar_devolucao(loan_id=101)
        self.assertTrue(res["sucesso"])
        self.assertEqual(res["loan"]["status"], "RETURNED")
        self.assertIsNotNone(res["loan"]["returnDate"])
        db = modulo_emprestimo._load_db()
        self.assertEqual(db[0]["status"], "RETURNED")

    # ================================================
    # TESTES DE CONTRATO / INTEGRIDADE (5)
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