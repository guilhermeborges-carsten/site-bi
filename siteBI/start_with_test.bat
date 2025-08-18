@echo off
echo ========================================
echo    SISTEMA DE BI - INICIALIZACAO
echo ========================================
echo.

REM Ativa o ambiente virtual se existir
IF EXIST venv (
    echo [1/4] Ativando ambiente virtual...
    call venv\Scripts\activate
) ELSE (
    echo [1/4] Ambiente virtual nao encontrado, usando Python global...
)

echo [2/4] Testando conexao com banco MySQL...
python test_db.py
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Falha na conexao com o banco!
    echo Verifique se o MySQL esta rodando e as configuracoes estao corretas.
    echo.
    pause
    exit /b 1
)

echo.
echo [3/4] Conexao OK! Iniciando sistema...
echo.

REM Define a variável de ambiente do Flask
set FLASK_APP=app.py
set FLASK_ENV=development

echo [4/4] Iniciando servidor Flask na porta 8000...
echo.
echo 🌐 Acesse: http://localhost:8000
echo 👤 Login: guilherme.borges@carsten.com.br
echo 🔑 Senha: admin123
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

REM Inicia o servidor Flask
flask run --host=0.0.0.0 --port=8000

pause
