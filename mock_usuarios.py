# mock_usuarios.py
# Simula o CRUD de usuários da Equipe 1 

# Dados falsos para teste
_usuarios_db = {
    1: {"userId": 1, "nome": "Ana Silva", "tipo": "aluno"},
    2: {"userId": 2, "nome": "Bruno Costa", "tipo": "professor"},
    3: {"userId": 3, "nome": "Carla Dias", "tipo": "funcionario"},
}

def get_usuario(user_id):
    """Simula a busca de um usuário."""
    return _usuarios_db.get(user_id, None)