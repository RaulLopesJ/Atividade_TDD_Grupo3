"""
README - Testes E2E com Selenium
Pasta: tests_selenium/

Este diretório contém testes end-to-end usando Selenium para validar
a interface gráfica completa do Sistema de Gerenciamento de Biblioteca Universitária (SGBU).

## 📋 Estrutura

```
tests_selenium/
├── __init__.py
├── test_selenium.py       # Testes E2E com Selenium
└── README.md              # Este arquivo
```

## 🧪 Testes Implementados

### TestCadastroUsuarios (3 testes)
- [x] test_acessar_pagina_cadastro - Acessa página de cadastro
- [x] test_formulario_cadastro_existe - Valida presença de campos
- [x] test_criar_usuario_valido - Cria usuário via interface

### TestCatalogoLivros (3 testes)
- [x] test_acessar_pagina_livros - Acessa catálogo
- [x] test_tabela_livros_existe - Valida tabela
- [x] test_formulario_novo_livro_existe - Valida formulário

### TestFluxoEmprestimo (3 testes)
- [x] test_acessar_pagina_emprestimos - Acessa página
- [x] test_formulario_emprestimo_existe - Valida formulário
- [x] test_listar_emprestimos - Lista empréstimos

### TestFluxoDevolucao (3 testes)
- [x] test_acessar_emprestimos - Acessa empréstimos
- [x] test_botoes_devolucao_existem - Valida botões
- [x] test_status_emprestimo_visivel - Valida status

### TestRelatorios (3 testes)
- [x] test_acessar_pagina_relatorios - Acessa relatórios
- [x] test_pagina_relatorios_carrega - Carrega página
- [x] test_estatisticas_visiveis - Valida estatísticas

### TestNavegacao (3 testes)
- [x] test_homepage_carrega - Homepage funciona
- [x] test_titulo_pagina_existe - Título presente
- [x] test_links_navegacao_existem - Links presentes

### TestValidacoes (2 testes)
- [x] test_email_invalido_validado - Email validado
- [x] test_campo_obrigatorio_vazio_lanca_erro - Validação requerida

### TestResponsividade (2 testes)
- [x] test_pagina_carrega_sem_erros_javascript - Sem erros JS
- [x] test_tabelas_visiveis_em_desktop - Layout desktop

**Total: 22 testes E2E**

## 📦 Instalação de Dependências

```bash
pip install selenium==4.15.2 webdriver-manager==4.0.1
```

## 🚀 Como Rodar

### 1. Iniciar o Servidor
```bash
# Terminal 1
python main.py
```

O servidor será iniciado em `http://localhost:8000`

### 2. Rodar os Testes
```bash
# Terminal 2
pytest tests_selenium/ -v
```

### 3. Rodar teste específico
```bash
pytest tests_selenium/test_selenium.py::TestCadastroUsuarios::test_criar_usuario_valido -v
```

### 4. Rodar com modo headless (sem janela)
Descomente a linha `options.add_argument('--headless')` em `driver()` fixture

```bash
pytest tests_selenium/ -v -s
```

## 🔍 Detalhes Técnicos

### Fixtures Disponíveis
- `driver`: Instância do WebDriver Chrome
- `base_url`: URL base (http://localhost:8000)

### Helpers Disponíveis
- `wait_for_element()`: Aguarda elemento estar visível
- `wait_for_element_clickable()`: Aguarda elemento ser clicável

### Configurações do Driver
```python
options = webdriver.ChromeOptions()
options.add_argument('--headless')        # Sem janela (descomente)
options.add_argument('--no-sandbox')      # Sandbox desabilitado
options.add_argument('--disable-dev-shm-usage')  # Memória compartilhada
```

## ⚠️ Pré-requisitos

1. **Python 3.8+** instalado
2. **Google Chrome** instalado
3. **Servidor rodando** em `http://localhost:8000`
4. **Dependências instaladas**: `pip install -r requirements-test.txt`

## 🧩 Padrão TDD

Todos os testes seguem o padrão Red-Green-Refactor:

```python
class TestCadastroUsuarios:
    """[RED-GREEN-REFACTOR] Testes da página de cadastro"""
    
    def test_acessar_pagina_cadastro(self, driver, base_url):
        """[GREEN] Conseguir acessar página de cadastro"""
        # Arrange
        driver.get(f"{base_url}/cadastro")
        
        # Act & Assert
        assert "cadastro" in driver.current_url.lower()
```

## 📊 Cobertura de Testes

```
Páginas Testadas:
├── /cadastro         ✅ 3 testes
├── /livros           ✅ 3 testes
├── /emprestimos      ✅ 3 testes
├── /relatorios       ✅ 3 testes
├── /               ✅ 3 testes
└── Geral             ✅ 7 testes

Total de Testes: 22
Cobertura: Todas as páginas e funcionalidades principais
```

## 🔧 Troubleshooting

### ChromeDriver não encontrado
```bash
# Reinstale webdriver-manager
pip install --upgrade webdriver-manager
```

### Timeout esperando elemento
Aumentar timeout na fixture `driver()`:
```python
driver.set_page_load_timeout(20)  # Aumentar para 20s
```

### Servidor não responde
Verificar se servidor está rodando:
```bash
curl http://localhost:8000
```

### Porta 8000 já em uso
```bash
# Mudar porta em main.py ou config
python main.py --port 8001
```

## 📝 Relatório de Cobertura

Gerar relatório HTML:
```bash
pytest tests_selenium/ --cov=View_and_Interface --cov-report=html
open htmlcov/index.html
```

## 🎯 Checklist de Testes

- [x] Navegação entre páginas
- [x] Preenchimento de formulários
- [x] Validação de entrada
- [x] Visualização de tabelas
- [x] Resposta do servidor
- [x] Mensagens de erro
- [x] Responsividade
- [x] Sem erros de JavaScript

## 📚 Recursos

- [Selenium Documentation](https://selenium.dev/documentation/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver-manager)
- [Pytest Documentation](https://docs.pytest.org/)
- [Wait Conditions](https://selenium.dev/documentation/webdriver/waits/)

## 📞 Suporte

Para problemas ou dúvidas:
1. Verificar Servidor rodando
2. Verificar dependências instaladas
3. Verificar Chrome instalado
4. Consultar logs do pytest: `pytest -v -s`

---

**Desenvolvido com TDD - Test Driven Development** 🚀
