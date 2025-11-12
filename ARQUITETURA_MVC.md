# 🏗️ ARQUITETURA MVC - DIAGRAMA E EXPLICAÇÃO

## 📊 Diagrama da Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAMADA DE APRESENTAÇÃO (VIEW)                   │
│                      View_and_Interface/view.py                        │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ HTTP REQUESTS & RESPONSES                                      │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │                                                                │   │
│  │  GET /emprestimos              →  render_emprestimos()        │   │
│  │  GET /emprestimos/novo         →  render_form_emprestimo()    │   │
│  │  POST /emprestimos/salvar      →  processar_emprestimo()      │   │
│  │                                                                │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                        ↓                                │
│                        Chama métodos do Controller                     │
└─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        │ import
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     CAMADA DE CONTROLE (CONTROLLER)                    │
│                            controler.py                                │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ CLASSE CONTROLLER (Fina e sem estado)                         │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │                                                                │   │
│  │  def verificar_disponibilidade(book_id):                       │   │
│  │      return modulo_emprestimo.verificar_disponibilidade(...)  │   │
│  │                                                                │   │
│  │  def registrar_emprestimo(user_id, book_id):                  │   │
│  │      return modulo_emprestimo.adicionar_emprestimo(...)       │   │
│  │                                                                │   │
│  │  def registrar_devolucao(loan_id):                            │   │
│  │      return modulo_emprestimo.registrar_devolucao(...)        │   │
│  │                                                                │   │
│  │  def get_emprestimos():                                        │   │
│  │      return modulo_emprestimo.get_emprestimos()               │   │
│  │                                                                │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ✅ Sem estado interno (sem _emprestimos)                             │
│  ✅ Sem lógica de negócio (sem _calcular_due_date)                    │
│  ✅ Apenas DELEGA para o Modelo                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        │ import
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       CAMADA DE LÓGICA (MODEL)                         │
│                      modulo_emprestimo.py                              │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ CLASSE EMPRESTIMO                                             │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │  def __init__():                                               │   │
│  │  def to_dict()        → Serializa para dict                   │   │
│  │  def get_loan_id()                                             │   │
│  │  def get_status()                                              │   │
│  │  def set_status()                                              │   │
│  │  def set_return_date()                                         │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ FUNÇÕES DE NEGÓCIO                                            │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │                                                                │   │
│  │  _calcular_due_date(data, tipo_usuario):                      │   │
│  │      ├─ if tipo_usuario == "professor" → +30 dias            │   │
│  │      └─ else → +14 dias                                       │   │
│  │                                                                │   │
│  │  verificar_disponibilidade(book_id):                          │   │
│  │      └─ return mock_catalogo.get_livro(book_id)              │   │
│  │                                                                │   │
│  │  adicionar_emprestimo(user_id, book_id):                      │   │
│  │      ├─ Valida usuário (mock_usuarios)                        │   │
│  │      ├─ Valida livro (mock_catalogo)                          │   │
│  │      ├─ Valida disponibilidade                                │   │
│  │      ├─ Calcula due_date                                      │   │
│  │      ├─ Cria objeto Emprestimo                                │   │
│  │      ├─ Adiciona à lista global                               │   │
│  │      ├─ Atualiza status no catálogo                           │   │
│  │      └─ return resultado                                      │   │
│  │                                                                │   │
│  │  registrar_devolucao(loan_id):                                │   │
│  │      ├─ Busca empréstimo                                      │   │
│  │      ├─ Valida se ainda não foi devolvido                     │   │
│  │      ├─ Atualiza status para "RETURNED"                       │   │
│  │      ├─ Registra data da devolução                            │   │
│  │      ├─ Atualiza livro como "disponível"                      │   │
│  │      └─ return resultado                                      │   │
│  │                                                                │   │
│  │  get_emprestimos():                                            │   │
│  │      └─ return [emp.to_dict() for emp in emprestimos]         │   │
│  │                                                                │   │
│  │  get_emprestimo_by_id(loan_id):                               │   │
│  │      └─ return emp.to_dict() or None                          │   │
│  │                                                                │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ✅ TODA lógica de negócio aqui                                       │
│  ✅ Validações centralizadas                                          │
│  ✅ Cálculos de negócio aqui                                          │
│  ✅ Estado global mantido aqui                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
┌──────────────────────────┐  ┌──────────────────────┐  ┌─────────────────┐
│  mock_usuarios.py        │  │  mock_catalogo.py    │  │ ESTADO GLOBAL   │
│  (Usuários)              │  │  (Livros)            │  │ (emprestimos[]) │
│                          │  │                      │  │                 │
│  _usuarios_db = {        │  │ _catalogo_db = {     │  │ next_loan_id    │
│    1: {...},             │  │   1: {...},          │  │                 │
│    2: {...},             │  │   2: {...},          │  │ emprestimos = [ │
│    3: {...}              │  │   3: {...}           │  │   Emprestimo(), │
│  }                       │  │ }                    │  │   Emprestimo()  │
│                          │  │                      │  │ ]               │
│  get_usuario()           │  │ get_livro()          │  └─────────────────┘
│  listar_usuarios()       │  │ update_status_livro()│
│  + helpers               │  │ listar_livros()      │
│                          │  │ + helpers            │
└──────────────────────────┘  └──────────────────────┘
```

---

## 🔄 FLUXO DE DADOS - CRIAR EMPRÉSTIMO

```
USUÁRIO NO NAVEGADOR
        │
        ▼
┌─────────────────────────────────────────┐
│ Clica em "+ Novo Empréstimo"           │
└─────────────────────────────────────────┘
        │
        ▼ GET /emprestimos/novo
┌─────────────────────────────────────────┐
│ VIEW: render_form_emprestimo()          │
│ ├─ Carrega usuários                     │
│ │  └─ mock_usuarios.listar_usuarios()   │
│ ├─ Carrega livros disponíveis           │
│ │  └─ mock_catalogo.listar_livros_dispon()
│ └─ Renderiza formulário HTML            │
└─────────────────────────────────────────┘
        │
        ▼ (usuário preenche e clica "Registrar")
┌─────────────────────────────────────────┐
│ POST /emprestimos/salvar                │
│ user_id=1&book_id=3                     │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ VIEW: processar_emprestimo(data)        │
│ ├─ Extrai user_id e book_id             │
│ ├─ Chama controller.registrar_emprestimo│
│ │  └─ controller.registrar_emprestimo(1,3)
│ └─ Aguarda resultado                    │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ CONTROLLER: registrar_emprestimo()      │
│ └─ Delega para modelo                   │
│    └─ modulo.adicionar_emprestimo(1, 3)│
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ MODEL: adicionar_emprestimo(1, 3)       │
│ ├─ Valida: usuario_existe(1)?           │
│ │  └─ mock_usuarios.get_usuario(1) → OK │
│ ├─ Valida: livro_existe(3)?             │
│ │  └─ mock_catalogo.get_livro(3) → OK   │
│ ├─ Valida: status_livro == "disponivel" │
│ │  └─ yes                                │
│ ├─ Calcula due_date:                    │
│ │  ├─ usuario tipo = "aluno"             │
│ │  ├─ data_atual + 14 dias               │
│ │  └─ due_date = "2025-11-26"            │
│ ├─ Cria Emprestimo(                     │
│ │    user_id=1, book_id=3,              │
│ │    loan_id=1, status="ACTIVE",        │
│ │    due_date="2025-11-26"              │
│ │  )                                     │
│ ├─ Adiciona à lista: emprestimos.append │
│ ├─ Atualiza livro:                      │
│ │  └─ mock_catalogo.update_status_livro │
│ │     (3, "emprestado")                  │
│ ├─ Incrementa: next_loan_id = 2         │
│ └─ return {                             │
│    "sucesso": True,                     │
│    "loan": {...}                        │
│   }                                      │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ CONTROLLER: Retorna resultado           │
│ └─ return resultado                     │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ VIEW: processar_emprestimo()            │
│ ├─ Recebe resultado                     │
│ ├─ if sucesso:                          │
│ │  └─ Renderiza página de sucesso       │
│ │     ├─ Empréstimo #{1} criado!        │
│ │     ├─ Usuário: 1                     │
│ │     ├─ Livro: 3                       │
│ │     ├─ Data de devolução: 2025-11-26  │
│ │     └─ Status: ACTIVE                 │
│ └─ else: Renderiza erro                 │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ NAVEGADOR: Exibe página HTML            │
│ ├─ Título: ✅ Empréstimo registrado     │
│ ├─ Dados do empréstimo                  │
│ └─ Link "Voltar para lista"             │
└─────────────────────────────────────────┘
```

---

## 🧩 PADRÃO DE DELEGAÇÃO

### Antes (Errado - Fat Controller)
```python
# controler.py
class Controller:
    def __init__(self):
        self._emprestimos = []  # ❌ Estado local
        self._next_loan_id = 1
    
    def registrar_emprestimo(self, user_id, book_id):
        # ❌ DUPLICA lógica do modelo
        usuario = mock_usuarios.get_usuario(user_id)
        if not usuario:
            return {"sucesso": False, "erro": "..."}
        
        livro = mock_catalogo.get_livro(book_id)
        if not livro:
            return {"sucesso": False, "erro": "..."}
        
        # ❌ Reimplementa cálculos
        agora = datetime.now()
        if usuario["tipo"] == "professor":
            due_date = agora + timedelta(days=30)
        else:
            due_date = agora + timedelta(days=14)
        
        # ❌ Gerencia próprio estado
        novo_emp = {...}
        self._emprestimos.append(novo_emp)
        self._next_loan_id += 1
        
        # ❌ Duplica atualização de status
        mock_catalogo.update_status_livro(book_id, "emprestado")
        
        return {"sucesso": True, "loan": novo_emp}
```

### Depois (Correto - Thin Controller)
```python
# controler.py
class Controller:
    def __init__(self):
        pass  # ✅ Sem estado
    
    def registrar_emprestimo(self, user_id, book_id):
        # ✅ APENAS delega
        return modulo_emprestimo.adicionar_emprestimo(user_id, book_id)

# modulo_emprestimo.py
def adicionar_emprestimo(user_id, book_id):
    # ✅ TODA lógica aqui
    usuario = mock_usuarios.get_usuario(user_id)
    if not usuario:
        return {"sucesso": False, "erro": "Usuário não encontrado"}
    
    livro = mock_catalogo.get_livro(book_id)
    if not livro:
        return {"sucesso": False, "erro": "Livro não encontrado"}
    
    if livro["status"] != "disponivel":
        return {"sucesso": False, "erro": "Livro indisponível"}
    
    agora = datetime.now()
    due_date = _calcular_due_date(agora, usuario["tipo"])
    
    emp = Emprestimo(...)
    emprestimos.append(emp)
    next_loan_id += 1
    mock_catalogo.update_status_livro(book_id, "emprestado")
    
    return {"sucesso": True, "loan": emp.to_dict()}
```

**Benefícios:**
- ✅ Código não duplicado
- ✅ Fácil de testar
- ✅ Fácil de manter
- ✅ Fácil de reutilizar
- ✅ Responsabilidades claras

---

## 🎯 RESPONSABILIDADES POR CAMADA

| Camada | Responsabilidade | O que FIZER | O que NÃO FIZER |
|--------|-----------------|------------|-----------------|
| **View** | Apresentação | Renderizar HTML, receber requisições, exibir dados | Validações complexas, cálculos de negócio, gerenciar estado |
| **Controller** | Orquestração | Chamar métodos do modelo, passar dados | Implementar lógica de negócio, gerenciar estado |
| **Model** | Lógica | Validações, cálculos, estado, regras de negócio | Renderizar HTML, conhecer HTTP, conhecer banco |

---

## 🧪 COMO TESTAR CADA CAMADA

### Testar Model (Unitário)
```python
def test_calcular_due_date_aluno():
    # Testa lógica pura
    resultado = modulo_emprestimo._calcular_due_date(
        datetime(2025, 11, 12), 
        "aluno"
    )
    assert resultado == datetime(2025, 11, 26)
```

### Testar Controller (Integração)
```python
def test_controller_registrar_emprestimo():
    # Testa delegação
    resultado = controller.registrar_emprestimo(user_id=1, book_id=3)
    assert resultado["sucesso"] == True
    assert resultado["loan"]["userId"] == 1
```

### Testar View (E2E)
```python
# Testa fluxo completo
# GET /emprestimos → deve retornar lista
# POST /emprestimos/salvar → deve criar e redirecionar
```

---

## 📈 ESCALABILIDADE

```
Com a arquitetura MVC correta, é fácil escalar:

1. Trocar mock pelo BD real
   ├─ Apenas mude mock_usuarios.py e mock_catalogo.py
   └─ Modelo e Controller continuam iguais

2. Adicionar nova funcionalidade
   ├─ Adicione função no Modelo
   ├─ Adicione método no Controller
   └─ Adicione view na View

3. Mudar interface (CLI → Web → Mobile)
   ├─ Mude View
   ├─ Model e Controller reutilizáveis
   └─ Lógica é a mesma
```

---

## ✅ CHECKLIST DE QUALIDADE

- [x] Separação clara de responsabilidades
- [x] Sem duplicação de código
- [x] Sem estado onde não deveria estar
- [x] Fácil de testar
- [x] Fácil de manter
- [x] Fácil de estender
- [x] Código limpo e legível
- [x] Documentação completa

---

**Versão:** 1.0  
**Data:** 12 de novembro de 2025

