import uuid
from enum import Enum

class Tipo(Enum):
    ALUNO = "ALUNO"
    PROFESSOR = "PROFESSOR"
    FUNCIONARIO = "FUNCIONARIO"

class Status(Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    SUSPENSO = "SUSPENSO"

class Usuario:
    def __init__(self, id, nome, matricula, tipo, email, ativoDeRegistro, status):
        self.id = id if id is not None else uuid.uuid4()  # ou str(uuid.uuid4()) para guardar como string
        self.nome = nome
        self.matricula = matricula
        self.tipo = tipo
        self.email = email
        self.ativoDeRegistro = ativoDeRegistro
        self.status = status

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_matricula(self):
        return self.matricula

    def set_matricula(self, matricula):
        self.matricula = matricula

    def get_tipo(self):
        return self.tipo

    def set_tipo(self, tipo):
        # aceita Tipo, ou str (nome ou valor); lança ValueError se inválido
        if isinstance(tipo, Tipo):
            self.tipo = tipo
            return

        if isinstance(tipo, str):
            # tenta pelo nome (Tipo['ALUNO']) então pelo valor (Tipo('ALUNO'))
            try:
                self.tipo = Tipo[tipo]
                return
            except KeyError:
                pass
            try:
                self.tipo = Tipo(tipo)
                return
            except ValueError:
                pass

        raise ValueError(f"tipo inválido: {tipo}. Deve ser um membro de Tipo")

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_ativoDeRegistro(self):
        return self.ativoDeRegistro

    def set_ativoDeRegistro(self, ativoDeRegistro):
        self.ativoDeRegistro = ativoDeRegistro

    def get_status(self):
        return self.status

    def set_status(self, status):
        # aceita Status, ou str (nome ou valor); lança ValueError se inválido
        if isinstance(status, Status):
            self.status = status
            return

        if isinstance(status, str):
            # tenta pelo nome (Status['ATIVO']) então pelo valor (Status('ATIVO'))
            try:
                self.status = Status[status]
                return
            except KeyError:
                pass
            try:
                self.status = Status(status)
                return
            except ValueError:
                pass

        raise ValueError(f"status inválido: {status}. Deve ser um membro de Status")
        
    def replace(self, **kwargs):
        """Cria uma nova instância com os campos atualizados"""
        # Pegando os valores atuais para campos não fornecidos
        id = kwargs.get('id', self.id)
        nome = kwargs.get('nome', self.nome)
        matricula = kwargs.get('matricula', self.matricula)
        tipo = kwargs.get('tipo', self.tipo)
        email = kwargs.get('email', self.email)
        ativoDeRegistro = kwargs.get('ativoDeRegistro', self.ativoDeRegistro)
        status = kwargs.get('status', self.status)

        # Retorna uma nova instância com os valores atualizados
        return Usuario(
            id=id,
            nome=nome,
            matricula=matricula,
            tipo=tipo,
            email=email,
            ativoDeRegistro=ativoDeRegistro,
            status=status
        )
        
    def replace(self, **kwargs):
        """
        Creates a new Usuario instance with updated values.
        Any attribute not specified in kwargs will keep its current value.
        """
        # Get current values for all attributes
        current_values = {
            'id': self.id,
            'nome': self.nome,
            'matricula': self.matricula,
            'tipo': self.tipo,
            'email': self.email,
            'ativoDeRegistro': self.ativoDeRegistro,
            'status': self.status
        }
        
        # Update with new values from kwargs
        current_values.update(kwargs)
        
        # Create new instance with updated values
        return Usuario(
            id=current_values['id'],
            nome=current_values['nome'],
            matricula=current_values['matricula'],
            tipo=current_values['tipo'],
            email=current_values['email'],
            ativoDeRegistro=current_values['ativoDeRegistro'],
            status=current_values['status']
        )

    def to_dict(self):
        """
        Serializa o usuário para um dicionário.
        
        Returns:
            dict: Dicionário com os atributos do usuário
        """
        return {
            "id": str(self.id),
            "nome": self.nome,
            "matricula": self.matricula,
            "tipo": self.tipo.value,
            "email": self.email,
            "ativoDeRegistro": self.ativoDeRegistro,
            "status": self.status.value
        }
        