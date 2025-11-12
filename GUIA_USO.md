# 🎬 Guia de Uso - Sistema de Empréstimos

## 📖 Fluxo de Operação

### 1️⃣ **Listar Empréstimos**

#### URL
```
GET http://localhost:8000/emprestimos
```

#### O que acontece:
1. View renderiza a página de empréstimos
2. Controller é chamado via `controller.get_emprestimos()`
3. Retorna lista de todos os empréstimos com:
   - ID do empréstimo
   - ID do usuário
   - ID do livro
   - Datas (empréstimo e devolução)
   - Status (ATIVO ou DEVOLVIDO)

#### Estatísticas Exibidas
- Total de empréstimos ativos
- Total de empréstimos devolvidos
- Total geral

---

### 2️⃣ **Criar Novo Empréstimo**

#### URL
```
GET http://localhost:8000/emprestimos/novo
```

#### Formulário Carregado com Dados Reais
```python
# Usuários carregados de mock_usuarios
- Ana Silva (aluno)       - ID 1
- Bruno Costa (professor) - ID 2
- Carla Dias (aluno)      - ID 3

# Livros disponíveis carregados de mock_catalogo
- Engenharia de Software - ID 1
- Banco de Dados         - ID 2
- IA Moderna             - ID 3
```

#### Submissão do Formulário
```
POST http://localhost:8000/emprestimos/salvar
```

**Dados Enviados:**
```
user_id=1&book_id=3
```

#### Processamento (Código na View)
```python
def processar_emprestimo(self, data):
    user_id = int(data.get('user_id'))
    book_id = int(data.get('book_id'))
    
    # Controller valida e cria empréstimo
    resultado = controller.registrar_emprestimo(user_id=user_id, book_id=book_id)
    
    if resultado.get("sucesso"):
        # Exibe dados do empréstimo criado
        loan = resultado["loan"]
        # Mostra: ID, usuário, livro, datas, status
    else:
        # Exibe erro (usuário inexistente, livro indisponível, etc)
        erro = resultado.get("erro")
```

#### Validações Automáticas (Controller → Model)
```python
# modulo_emprestimo.adicionar_emprestimo() valida:

❌ Usuário não encontrado → "Usuário não encontrado"
❌ Livro não encontrado → "Livro não encontrado"
❌ Livro já emprestado → "Livro indisponível"
✅ Tudo OK → Cria empréstimo com:
   - loanId: auto-incrementado
   - loanDate: data/hora atual
   - dueDate: calculada por tipo de usuário
     • Aluno: 14 dias
     • Professor: 30 dias
   - status: "ACTIVE"
```

#### Exemplo de Resposta de Sucesso
```html
✅ Empréstimo registrado com sucesso!

Detalhes do Empréstimo:
├─ ID do Empréstimo: 1
├─ Usuário ID: 1
├─ Livro ID: 3
├─ Data de Empréstimo: 2025-11-12
├─ Data de Devolução Prevista: 2025-11-26
└─ Status: ACTIVE
```

---

## 🔄 Fluxo Completo de Dados

### Criação de Empréstimo

```
┌─────────────────┐
│  USUÁRIO        │
│  Acessa VIEW    │
└────────┬────────┘
         │
         ▼ (clica em "+ Novo Empréstimo")
┌─────────────────────────────────────────────────┐
│  VIEW - render_form_emprestimo()                 │
│  ├─ mock_usuarios.listar_usuarios()             │
│  ├─ mock_catalogo.listar_livros_disponiveis()   │
│  └─ Renderiza form com dropdowns preenchidos    │
└────────┬────────────────────────────────────────┘
         │
         ▼ (preenche form e submete)
┌─────────────────────────────────────────────────┐
│  VIEW - processar_emprestimo()                   │
│  └─ controller.registrar_emprestimo()           │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│  CONTROLLER - registrar_emprestimo()             │
│  └─ modulo_emprestimo.adicionar_emprestimo()    │
└────────┬────────────────────────────────────────┘
         │
         ▼ (validações e criação)
┌─────────────────────────────────────────────────┐
│  MODEL - adicionar_emprestimo()                  │
│  ├─ Valida usuário (mock_usuarios)              │
│  ├─ Valida livro (mock_catalogo)                │
│  ├─ Valida disponibilidade                      │
│  ├─ Calcula dueDate por tipo de usuário         │
│  ├─ Cria objeto Emprestimo                      │
│  ├─ Adiciona à lista global                     │
│  ├─ Atualiza status do livro                    │
│  └─ Retorna resultado {"sucesso": True/False}   │
└────────┬────────────────────────────────────────┘
         │
         ▼ (retorna resultado)
┌─────────────────────────────────────────────────┐
│  VIEW - processar_emprestimo()                   │
│  ├─ If sucesso: exibe dados do empréstimo      │
│  └─ Else: exibe mensagem de erro                │
└─────────────────────────────────────────────────┘
```

---

## 💾 Estado Gerenciado

### Empréstimos (modulo_emprestimo.py)
```python
emprestimos = [
    {
        "loanId": 1,
        "userId": 1,
        "bookId": 3,
        "loanDate": "2025-11-12T10:30:45.123456",
        "dueDate": "2025-11-26T10:30:45.123456",
        "returnDate": None,
        "status": "ACTIVE",
        "fine": 0.0
    }
]

next_loan_id = 2
```

### Usuários (mock_usuarios.py)
```python
_usuarios_db = {
    1: {"userId": 1, "nome": "Ana Silva", "tipo": "aluno", "email": "ana@escola.com"},
    2: {"userId": 2, "nome": "Bruno Costa", "tipo": "professor", "email": "bruno@escola.com"},
    3: {"userId": 3, "nome": "Carla Dias", "tipo": "aluno", "email": "carla@escola.com"}
}
```

### Livros (mock_catalogo.py)
```python
_catalogo_db = {
    1: {"bookId": 1, "titulo": "Engenharia de Software", "autor": "Sommerville", "status": "disponivel"},
    2: {"bookId": 2, "titulo": "Banco de Dados", "autor": "Date", "status": "disponivel"},
    3: {"bookId": 3, "titulo": "IA Moderna", "autor": "Russell", "status": "emprestado"}  # ← Atualizado
}
```

---

## 🧪 Casos de Teste

### ✅ Sucesso
```
user_id = 1 (Ana Silva - aluno)
book_id = 1 (Engenharia de Software - disponível)

Resultado:
├─ Status: sucesso = True
├─ Empréstimo criado com ID = 1
├─ Due date = 2025-11-12 + 14 dias = 2025-11-26
└─ Livro agora marca como "emprestado"
```

### ❌ Erro: Usuário Inexistente
```
user_id = 999 (não existe)
book_id = 1

Resultado:
├─ Status: sucesso = False
└─ erro = "Usuário não encontrado"
```

### ❌ Erro: Livro Inexistente
```
user_id = 1
book_id = 999 (não existe)

Resultado:
├─ Status: sucesso = False
└─ erro = "Livro não encontrado"
```

### ❌ Erro: Livro Indisponível
```
user_id = 2 (Bruno - professor)
book_id = 3 (IA - já emprestado)

Resultado:
├─ Status: sucesso = False
└─ erro = "Livro indisponível"
```

---

## 📊 Integração com Testes

### Test - setUp
```python
def setUp(self):
    # Reseta estado do modelo
    modulo_emprestimo.emprestimos = []
    modulo_emprestimo.next_loan_id = 1
    
    # Cria instância do controller
    self.controller = controler.Controller()
    
    # Reseta catálogo
    mock_catalogo._catalogo_db = {
        1: {...},
        2: {...},
        3: {...}
    }
```

### Test - Execução
```python
def test_unit_registrar_emprestimo_sucesso(self):
    # 1. Prepara dados
    livro_antes = mock_catalogo.get_livro(3)
    assert livro_antes["status"] == "disponivel"
    
    # 2. Executa via controller
    res = self.controller.registrar_emprestimo(user_id=1, book_id=3)
    
    # 3. Valida resultado
    assert res["sucesso"] == True
    assert res["loan"]["userId"] == 1
    assert res["loan"]["bookId"] == 3
    assert res["loan"]["status"] == "ACTIVE"
    
    # 4. Valida estado
    livro_depois = mock_catalogo.get_livro(3)
    assert livro_depois["status"] == "emprestado"
```

---

## 🛠️ Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'controler'"
**Solução:**
```powershell
# Certifique-se de que está no diretório correto
cd c:\Users\Raul\Desktop\Atividade_testes\Atividade_TDD_Grupo3-main

# Verifique se o arquivo existe
ls controler.py
```

### Problema: "Nenhum livro disponível"
**Causas:**
- Todos os livros já foram emprestados
- Banco de dados foi limpo

**Solução:**
```python
# Reinicie o servidor ou
# Execute setUp dos testes para resetar
```

### Problema: Empréstimo criado mas não aparece na lista
**Causa:** Cache do navegador

**Solução:**
```
Ctrl + F5  # Hard refresh no navegador
```

---

## 📝 Exemplos de Código

### Criar empréstimo programaticamente
```python
from controler import controller

resultado = controller.registrar_emprestimo(user_id=1, book_id=3)

if resultado["sucesso"]:
    loan = resultado["loan"]
    print(f"Empréstimo #{loan['loanId']} criado!")
    print(f"Devolução esperada em: {loan['dueDate']}")
else:
    print(f"Erro: {resultado['erro']}")
```

### Listar todos os empréstimos
```python
from controler import controller

emprestimos = controller.get_emprestimos()

for emp in emprestimos:
    print(f"#{emp['loanId']}: User {emp['userId']} → Book {emp['bookId']} ({emp['status']})")
```

### Verificar disponibilidade
```python
from controler import controller

resultado = controller.verificar_disponibilidade(book_id=1)

if "erro" in resultado:
    print(resultado["erro"])
else:
    print(f"{resultado['titulo']} - {resultado['status']}")
```

---

**Última atualização:** 12 de novembro de 2025

