"""Mock de usuários - simula um banco de dados de usuários."""

# Base de dados simulada de usuários
_usuarios_db = {
    1: {"userId": 1, "nome": "Ana Silva", "tipo": "aluno", "email": "ana@escola.com"},
    2: {"userId": 2, "nome": "Bruno Costa", "tipo": "professor", "email": "bruno@escola.com"},
    3: {"userId": 3, "nome": "Carla Dias", "tipo": "aluno", "email": "carla@escola.com"},
}


def get_usuario(user_id):
    """
    Retorna os dados do usuário ou None se não encontrado.
    
    Args:
        user_id: ID do usuário a buscar
        
    Returns:
        dict com dados do usuário ou None
    """
    return _usuarios_db.get(user_id)


def usuario_existe(user_id):
    """
    Verifica se um usuário existe.
    
    Args:
        user_id: ID do usuário
        
    Returns:
        True se existe, False caso contrário
    """
    return user_id in _usuarios_db


def adicionar_usuario(user_id, nome, tipo, email):
    """
    Adiciona um novo usuário ao banco simulado.
    
    Args:
        user_id: ID do usuário
        nome: Nome completo
        tipo: 'aluno' ou 'professor'
        email: Email do usuário
    """
    _usuarios_db[user_id] = {
        "userId": user_id,
        "nome": nome,
        "tipo": tipo,
        "email": email
    }


def listar_usuarios():
    """Retorna lista de todos os usuários."""
    return list(_usuarios_db.values())


def limpar_usuarios():
    """Limpa todos os usuários (útil para testes)."""
    _usuarios_db.clear()