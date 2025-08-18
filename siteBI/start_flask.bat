@echo off
REM Ativa o ambiente virtual se existir
IF EXIST venv (call venv\Scripts\activate)

REM Define a variável de ambiente do Flask
set FLASK_APP=app.py
set FLASK_ENV=development

REM Inicia o servidor Flask na porta 8000
flask run --host=0.0.0.0 --port=8000

pause 