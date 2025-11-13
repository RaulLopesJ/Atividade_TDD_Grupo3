# SGBU - Sistema de Gerenciamento de Biblioteca Universitária

**TecLearn Tabajara - Projeto de Teste de Integração**

---

## Sobre o Projeto

Este é o projeto base para a disciplina de **Implementação e Teste de Software**. O objetivo é desenvolver um sistema de gerenciamento de biblioteca usando **TDD (Test Driven Development)** e realizar testes de integração entre os módulos.

### Objetivos de Aprendizagem

- Aplicar metodologia TDD (Red-Green-Refactor)
- Criar testes unitários com pytest
- Realizar testes de integração entre módulos
- Trabalhar com padrão MVC
- Integrar diferentes módulos de uma aplicação

---

## Estrutura do Projeto

```
SGBU_TecLearn/
├── main.py                      # Arquivo principal para rodar o servidor
├── controler.py                 # [IMPLEMENTAR] Controlador de integração
├── README.md                    # Este arquivo
│
├── Model/                       # [IMPLEMENTAR] Camada de modelo/negócio
│   ├── Usuario.py              # Módulo 1 - Cadastro de usuários
│   ├── Livro.py                # Módulo 2 - Catálogo de livros
│   ├── Autor.py                # Módulo 2 - Gestão de autores
│   ├── Emprestimo.py           # Módulo 3 - Empréstimos e devoluções
│   └── Relatorio.py            # Módulo 4 - Relatórios e estatísticas
│
└── View_and_Interface/          # [PRONTO] Camada de visualização
    ├── view.py                  # Servidor HTTP com APIs REST
    ├── cadastro.html            # Tela de cadastro de usuários
    ├── crud_livros.html         # Tela de catálogo de livros
    ├── emprestimos.html         # Tela de empréstimos
    └── relatorios.html          # Tela de relatórios
```

---

## Como Executar o Projeto

### Instalar Python

Certifique-se de ter Python 3.8+ instalado:

```bash
python --version
```

### Instalar Dependências (para testes)

```bash
pip install pytest pytest-cov
```

### Executar o Servidor

```bash
python main.py
```

O servidor será iniciado em: **http://localhost:8000**

### Acessar as Telas

- **Cadastro de Usuários**: http://localhost:8000/cadastro
- **Catálogo de Livros**: http://localhost:8000/livros
- **Empréstimos**: http://localhost:8000/emprestimos
- **Relatórios**: http://localhost:8000/relatorios

---

## Divisão dos Módulos (Por Equipe)

### 🔵 **Equipe 1 - Cadastro de Usuários**

**Arquivo**: `Model/Usuario.py`

**Responsabilidades**:
- CRUD de usuários (criar, editar, remover, listar)
- Validações de matrícula, nome, tipo, email
- Tipos de usuário: aluno, professor, funcionário

**Testes Mínimos**:
- ✅ 10 testes unitários
- ✅ 5 testes de contrato/integridade

---

### 🟢 **Equipe 2 - Catálogo de Livros**

**Arquivos**: `Model/Livro.py` e `Model/Autor.py`

**Responsabilidades**:
- CRUD de livros (título, autor, ISBN, estoque, status)
- CRUD de autores
- Controle de disponibilidade
- Gestão de estoque

**Testes Mínimos**:
- ✅ 10 testes unitários
- ✅ 5 testes de contrato/integridade

---

### 🟡 **Equipe 3 - Empréstimo e Devolução**

**Arquivo**: `Model/Emprestimo.py`

**Responsabilidades**:
- Registrar empréstimos
- Registrar devoluções
- Verificar disponibilidade de livros
- Calcular atrasos
- Controlar prazos

**Testes Mínimos**:
- ✅ 10 testes unitários
- ✅ 5 testes de contrato/integridade

**⚠️ IMPORTANTE**: Este módulo **depende** dos módulos 1 e 2!

---

### 🟣 **Equipe 4 - Relatórios**

**Arquivo**: `Model/Relatorio.py`

**Responsabilidades**:
- Livros mais emprestados
- Usuários mais ativos
- Taxa de ocupação
- Empréstimos por período
- Estatísticas gerais

**Testes Mínimos**:
- ✅ 10 testes unitários
- ✅ 5 testes de contrato/integridade

**⚠️ IMPORTANTE**: Este módulo **depende** de todos os outros!

---

## 🧪 Metodologia TDD

### Ciclo Red-Green-Refactor

1. **🔴 RED**: Escreva um teste que falha
2. **🟢 GREEN**: Escreva o código mínimo para passar
3. **🔵 REFACTOR**: Melhore o código mantendo os testes passando

### Formato de Commits (OBRIGATÓRIO)

```bash
[TDD red] test_criar_usuario_valido
[TDD green] test_criar_usuario_valido
[TDD refactor] melhoria na validacao de usuario
```

### Exemplo de Fluxo TDD

```python
# 1. RED - Escrever teste que falha
def test_criar_usuario_valido():
    usuario = Usuario("2021001", "João Silva", "aluno")
    assert usuario.nome == "João Silva"
    # Commit: [TDD red] test_criar_usuario_valido

# 2. GREEN - Código mínimo que passa
class Usuario:
    def __init__(self, matricula, nome, tipo):
        self.matricula = matricula
        self.nome = nome
        self.tipo = tipo
    # Commit: [TDD green] test_criar_usuario_valido

# 3. REFACTOR - Melhorias
class Usuario:
    def __init__(self, matricula, nome, tipo):
        self._validar_matricula(matricula)
        self.matricula = matricula
        self.nome = nome
        self.tipo = tipo
    
    def _validar_matricula(self, matricula):
        if not matricula:
            raise ValueError("Matrícula é obrigatória")
    # Commit: [TDD refactor] adiciona validacao de matricula
```

---

## 🔌 APIs REST Disponíveis

### Usuários

```
GET    /api/usuarios           # Listar todos
POST   /api/usuarios           # Criar novo
PUT    /api/usuarios/{id}      # Atualizar
DELETE /api/usuarios/{id}      # Remover
```

### Livros

```
GET    /api/livros             # Listar todos
POST   /api/livros             # Criar novo
PUT    /api/livros/{id}        # Atualizar
DELETE /api/livros/{id}        # Remover
```

### Autores

```
GET    /api/autores            # Listar todos
POST   /api/autores            # Criar novo
PUT    /api/autores/{id}       # Atualizar
DELETE /api/autores/{id}       # Remover
```

### Empréstimos

```
GET    /api/emprestimos                    # Listar todos
POST   /api/emprestimos                    # Criar novo
POST   /api/emprestimos/{id}/devolver      # Registrar devolução
```

---

## 📊 Exemplos de Testes

### Teste Unitário

```python
import pytest
from Model.Usuario import Usuario

def test_criar_usuario_valido():
    """Testa criação de usuário válido"""
    usuario = Usuario("2021001", "João Silva", "aluno", "joao@email.com")
    assert usuario.matricula == "2021001"
    assert usuario.nome == "João Silva"
    assert usuario.tipo == "aluno"

def test_usuario_sem_matricula():
    """Testa validação de matrícula obrigatória"""
    with pytest.raises(ValueError, match="Matrícula é obrigatória"):
        Usuario("", "João Silva", "aluno")

def test_nome_muito_curto():
    """Testa validação de tamanho mínimo do nome"""
    with pytest.raises(ValueError, match="Nome deve ter pelo menos 3 caracteres"):
        Usuario("2021001", "Jo", "aluno")
```

### Teste de Integração

```python
def test_fluxo_completo_emprestimo():
    """Testa integração entre Usuario, Livro e Emprestimo"""
    # Arrange
    usuario = Usuario("2021001", "João Silva", "aluno")
    livro = Livro("978-0132350884", "Clean Code", estoque=5)
    
    # Act
    emprestimo = Emprestimo(usuario.id, livro.id, data_emprestimo="2025-11-01")
    
    # Assert
    assert emprestimo.status == "ativo"
    assert livro.estoque == 4  # Estoque foi decrementado
    assert emprestimo.prazo_devolucao == "2025-11-15"  # 14 dias depois
```

---

## 🧩 Testes de Contrato/Integridade

Exemplos de testes de contrato:

```python
def test_serializacao_usuario():
    """Verifica se Usuario pode ser serializado para JSON"""
    usuario = Usuario("2021001", "João Silva", "aluno")
    dados = usuario.to_dict()
    
    assert "id" in dados
    assert "matricula" in dados
    assert "nome" in dados
    assert "tipo" in dados

def test_campos_obrigatorios_livro():
    """Verifica que todos os campos obrigatórios estão presentes"""
    livro = Livro("978-0132350884", "Clean Code")
    
    assert hasattr(livro, 'isbn')
    assert hasattr(livro, 'titulo')
    assert hasattr(livro, 'estoque')
    assert hasattr(livro, 'status')
```

---

## 🎯 Critérios de Avaliação

### Cada equipe deve entregar:

✅ **10 testes unitários** cobrindo:
- Casos de sucesso
- Casos de erro
- Validações
- Casos de borda

✅ **5 testes de contrato/integridade**:
- Serialização
- Campos obrigatórios
- Tipos de dados
- Formato de resposta

✅ **Commits no formato TDD**:
- [TDD red] para testes falhando
- [TDD green] para testes passando
- [TDD refactor] para melhorias

✅ **Cobertura de testes**:
- Mínimo de 80% de cobertura

---

## 📦 Executar Testes

### Rodar todos os testes

```bash
pytest
```

### Rodar testes com cobertura

```bash
pytest --cov=Model --cov-report=html
```

### Rodar testes de um módulo específico

```bash
pytest tests/test_usuario.py
```

### Rodar um teste específico

```bash
pytest tests/test_usuario.py::test_criar_usuario_valido
```

---

## 📚 Estrutura de Testes Recomendada

```
tests/
├── __init__.py
├── test_usuario.py          # Testes da Equipe 1
├── test_livro.py            # Testes da Equipe 2
├── test_autor.py            # Testes da Equipe 2
├── test_emprestimo.py       # Testes da Equipe 3
├── test_relatorio.py        # Testes da Equipe 4
└── test_integracao.py       # Testes de integração entre módulos
```

---

## 🆘 Dicas para os Alunos

### 1. **Comece pelos testes mais simples**
```python
# ✅ Começar assim
def test_criar_usuario():
    usuario = Usuario("2021001", "João", "aluno")
    assert usuario.nome == "João"

# ❌ Não começar assim
def test_sistema_completo_emprestimo_com_validacoes():
    # Teste muito complexo para começar
```

### 2. **Um teste por vez**
- Escreva um teste
- Faça passar
- Commit
- Refatore se necessário
- Próximo teste

### 3. **Teste casos de erro**
```python
def test_emprestimo_livro_indisponivel():
    with pytest.raises(ValueError, match="Livro indisponível"):
        Emprestimo(usuario_id=1, livro_id=999)
```

### 4. **Use fixtures do pytest**
```python
@pytest.fixture
def usuario_padrao():
    return Usuario("2021001", "João Silva", "aluno")

def test_com_fixture(usuario_padrao):
    assert usuario_padrao.nome == "João Silva"
```

---

## 📞 Contato e Suporte

- **Professor**: Dacio Machado
- **Disciplina**: Implementação e Teste de Software
- **Curso**: ESOFT-6-N

---

## ✨ Recursos Adicionais

- [Documentação pytest](https://docs.pytest.org/)
- [TDD com Python](https://www.obeythetestinggoat.com/)
- [Clean Code - Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

---

**Bom trabalho e bons testes! 🚀**
