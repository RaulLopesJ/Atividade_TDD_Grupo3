@echo off
REM ============================================================================
REM SCRIPT: rodar_testes_selenium.bat
REM DESCRICAO: Executa testes Selenium E2E automaticamente
REM AUTOR: SGBU - Sistema de Gerenciamento de Biblioteca Universitaria
REM DATA: 13 de Novembro de 2025
REM ============================================================================

setlocal enabledelayedexpansion
chcp 65001 >nul
cls

REM Cores (usando caracteres ANSI)
set "RESET=[0m"
set "VERDE=[92m"
set "VERMELHO=[91m"
set "AMARELO=[93m"
set "AZUL=[94m"
set "CYAN=[96m"

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                            ║
echo ║         %AZUL%🧪 TESTE SELENIUM E2E - SGBU%RESET%                                         ║
echo ║                                                                            ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

REM ============================================================================
REM VALIDAÇÃO 1: Verificar Python
REM ============================================================================

echo %CYAN%[1/5] Validando Python...%RESET%
python --version >nul 2>&1
if errorlevel 1 (
    echo %VERMELHO%❌ Python não encontrado%RESET%
    echo.
    echo 📝 Como instalar:
    echo    1. Acesse: https://www.python.org/downloads/
    echo    2. Baixe Python 3.9+
    echo    3. Durante instalação, marque "Add Python to PATH"
    echo    4. Reinicie este script
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo %VERDE%✅ %PYTHON_VERSION% encontrado%RESET%
echo.

REM ============================================================================
REM VALIDAÇÃO 2: Verificar pytest
REM ============================================================================

echo %CYAN%[2/5] Validando pytest...%RESET%
python -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo %VERMELHO%❌ pytest não instalado%RESET%
    echo.
    echo 📦 Instalando dependências...
    python -m pip install -r requirements-test.txt -q
    if errorlevel 1 (
        echo %VERMELHO%❌ Erro ao instalar pytest%RESET%
        pause
        exit /b 1
    )
)
for /f "tokens=*" %%i in ('python -m pytest --version 2^>^&1') do set "PYTEST_VERSION=%%i"
echo %VERDE%✅ %PYTEST_VERSION% encontrado%RESET%
echo.

REM ============================================================================
REM VALIDAÇÃO 3: Verificar Selenium
REM ============================================================================

echo %CYAN%[3/5] Validando Selenium...%RESET%
python -c "import selenium; print('OK')" >nul 2>&1
if errorlevel 1 (
    echo %VERMELHO%❌ Selenium não instalado%RESET%
    echo.
    echo 📦 Instalando Selenium...
    python -m pip install -r requirements-selenium.txt -q
    if errorlevel 1 (
        echo %VERMELHO%❌ Erro ao instalar Selenium%RESET%
        pause
        exit /b 1
    )
)
python -c "import selenium; print(selenium.__version__)" >nul 2>&1
for /f "tokens=*" %%i in ('python -c "import selenium; print(selenium.__version__)" 2^>^&1') do set "SELENIUM_VERSION=%%i"
echo %VERDE%✅ Selenium !SELENIUM_VERSION! encontrado%RESET%
echo.

REM ============================================================================
REM VALIDAÇÃO 4: Verificar Chrome
REM ============================================================================

echo %CYAN%[4/5] Validando Chrome...%RESET%
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
if errorlevel 1 (
    echo %AMARELO%⚠️  Chrome não encontrado no PATH%RESET%
    echo.
    echo 💡 SOLUÇÃO: Instale Google Chrome
    echo.
    echo 1. Acesse: https://www.google.com/chrome/
    echo 2. Baixe e execute o instalador
    echo 3. Siga as instruções na tela
    echo 4. Reinicie este script após instalar
    echo.
    echo 🔄 Tentando encontrar Chrome em caminhos padrões...
    
    set "CHROME_FOUND=0"
    
    REM Verificar caminhos comuns
    if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
        set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
        set "CHROME_FOUND=1"
    )
    if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
        set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        set "CHROME_FOUND=1"
    )
    
    if !CHROME_FOUND! equ 0 (
        echo %VERMELHO%❌ Chrome não encontrado em caminhos conhecidos%RESET%
        echo.
        pause
        exit /b 1
    ) else (
        echo %VERDE%✅ Chrome encontrado: !CHROME_PATH!%RESET%
    )
) else (
    echo %VERDE%✅ Chrome encontrado no PATH%RESET%
)
echo.

REM ============================================================================
REM VALIDAÇÃO 5: Verificar arquivos de teste
REM ============================================================================

echo %CYAN%[5/5] Validando arquivos...%RESET%

if not exist "tests_selenium\test_selenium.py" (
    echo %VERMELHO%❌ Arquivo tests_selenium\test_selenium.py não encontrado%RESET%
    pause
    exit /b 1
)
echo %VERDE%✅ tests_selenium\test_selenium.py encontrado%RESET%

if not exist "main.py" (
    echo %VERMELHO%❌ Arquivo main.py não encontrado%RESET%
    pause
    exit /b 1
)
echo %VERDE%✅ main.py encontrado%RESET%
echo.

REM ============================================================================
REM RESUMO DE VALIDAÇÃO
REM ============================================================================

echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                    %VERDE%✅ TODAS AS VALIDAÇÕES PASSARAM%RESET%                       ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo %VERDE%Ambiente pronto para testes Selenium!%RESET%
echo.
echo Iniciando testes em 3 segundos...
echo.

timeout /t 3 /nobreak

REM ============================================================================
REM INICIAR SERVIDOR
REM ============================================================================

echo %AZUL%╔════════════════════════════════════════════════════════════════════════════╗%RESET%
echo %AZUL%║                        🚀 INICIANDO SERVIDOR                               ║%RESET%
echo %AZUL%╚════════════════════════════════════════════════════════════════════════════╝%RESET%
echo.

REM Matar qualquer processo anterior do Python na porta 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /pid %%a /f >nul 2>&1
)

REM Iniciar servidor em nova janela
echo %CYAN%Iniciando servidor em http://localhost:8000...%RESET%
start "Servidor SGBU" python main.py

REM Aguardar servidor iniciar
echo %CYAN%Aguardando servidor iniciar (5 segundos)...%RESET%
timeout /t 5 /nobreak

REM ============================================================================
REM EXECUTAR TESTES SELENIUM
REM ============================================================================

echo.
echo %AZUL%╔════════════════════════════════════════════════════════════════════════════╗%RESET%
echo %AZUL%║                      🧪 EXECUTANDO TESTES SELENIUM                        ║%RESET%
echo %AZUL%╚════════════════════════════════════════════════════════════════════════════╝%RESET%
echo.

python -m pytest tests_selenium/ -v --tb=short

REM Capturar código de saída
set "EXIT_CODE=%ERRORLEVEL%"

REM ============================================================================
REM RELATÓRIO FINAL
REM ============================================================================

echo.
echo %AZUL%╔════════════════════════════════════════════════════════════════════════════╗%RESET%
echo %AZUL%║                          📊 TESTE CONCLUÍDO                               ║%RESET%
echo %AZUL%╚════════════════════════════════════════════════════════════════════════════╝%RESET%
echo.

if %EXIT_CODE% equ 0 (
    echo %VERDE%✅ TODOS OS TESTES PASSARAM!%RESET%
    echo.
    echo 🎉 Parabéns! Os testes Selenium validam:
    echo    • Navegação entre páginas
    echo    • Formulários funcionando
    echo    • Interações com usuário
    echo    • Fluxos da aplicação
    echo.
) else (
    echo %VERMELHO%❌ ALGUNS TESTES FALHARAM%RESET%
    echo.
    echo 🔍 Possíveis problemas:
    echo    • Servidor não respondeu (verifique main.py)
    echo    • Elementos HTML não encontrados
    echo    • Timeouts na navegação
    echo.
)

REM Fechar servidor
echo %CYAN%Encerrando servidor...%RESET%
taskkill /f /im python.exe >nul 2>&1

echo.
echo %AMARELO%Pressione qualquer tecla para fechar...%RESET%
pause >nul

exit /b %EXIT_CODE%
