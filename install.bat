@echo off
echo ============================================
echo  Instalador - Webcam MCP para Claude Desktop
echo ============================================
echo.

:: Verifica se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado.
    echo Instale Python 3.10 ou superior em: https://python.org/downloads
    echo Marque a opcao "Add Python to PATH" durante a instalacao!
    pause
    exit /b 1
)

echo [OK] Python encontrado.
echo.

:: Instala dependencias
echo Instalando dependencias (opencv + mcp)...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERRO ao instalar dependencias.
    pause
    exit /b 1
)

echo.
echo [OK] Dependencias instaladas.
echo.

:: Descobre o caminho absoluto do server.py
set SCRIPT_DIR=%~dp0
set SERVER_PATH=%SCRIPT_DIR%server.py
set SERVER_PATH=%SERVER_PATH:\=\\%

:: Descobre o caminho do Python
for /f "tokens=*" %%i in ('where python') do set PYTHON_PATH=%%i
set PYTHON_PATH=%PYTHON_PATH:\=\\%

echo ============================================
echo  ULTIMO PASSO: Configurar o Claude Desktop
echo ============================================
echo.
echo 1. Abra o Claude Desktop
echo 2. Clique em File ^> Settings ^> Developer
echo 3. Clique em "Edit Config" (abre o arquivo claude_desktop_config.json)
echo 4. Substitua o conteudo pelo bloco abaixo:
echo.
echo {
echo   "mcpServers": {
echo     "webcam": {
echo       "command": "%PYTHON_PATH%",
echo       "args": ["%SERVER_PATH%"]
echo     }
echo   }
echo }
echo.
echo 5. Salve o arquivo e REINICIE o Claude Desktop
echo 6. Procure o icone de martelo (ferramentas) na janela de chat
echo    Se aparecer, o MCP esta funcionando!
echo.
echo ============================================
pause
