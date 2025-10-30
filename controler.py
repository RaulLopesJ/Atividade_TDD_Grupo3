from flask import Flask, render_template, request, jsonify
import os

import modulo_emprestimo
import mock_usuarios
import mock_catalogo

app = Flask(__name__, template_folder='View_and_Interface')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/emprestimos', methods=['GET'])
def get_emprestimos():
    emprestimos = modulo_emprestimo._load_db()
    return jsonify(emprestimos)

@app.route('/api/registrar_emprestimo', methods=['POST'])
def api_registrar_emprestimo():
    data = request.json
    try:
        user_id = int(data.get('userId'))
        book_id = int(data.get('bookId'))
        resultado = modulo_emprestimo.registrar_emprestimo(user_id, book_id)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"sucesso": False, "erro": f"Erro no servidor: {str(e)}"})

@app.route('/api/registrar_devolucao', methods=['POST'])
def api_registrar_devolucao():
    data = request.json
    try:
        loan_id = int(data.get('loanId'))
        resultado = modulo_emprestimo.registrar_devolucao(loan_id)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"sucesso": False, "erro": f"Erro no servidor: {str(e)}"})

@app.route('/api/verificar_livro/<int:book_id>', methods=['GET'])
def api_verificar_livro(book_id):
    try:
        resultado = modulo_emprestimo.verificar_disponibilidade(book_id)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"sucesso": False, "erro": f"Erro no servidor: {str(e)}"})


if __name__ == '__main__':
    if not os.path.exists(modulo_emprestimo.DB_FILE):
        modulo_emprestimo._save_db([])
    
    app.run(debug=True, port=5000)