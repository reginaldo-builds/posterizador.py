@echo off
chcp 65001 > nul

:: 1. Verifica se os arquivos essenciais existem
if not exist "main.py" exit

:: 2. DETECÇÃO DE VENV EXISTENTE
if exist "venv\Scripts\activate.bat" (
    set "NOME_ENV=venv"
    goto iniciar_programa
)

if exist "venv\Scripts\activate.bat" (
    set "NOME_ENV=venv"
    goto iniciar_programa
)

:: 3. CRIAÇÃO DA VENV (Caso não exista nenhuma)
python -m venv venv
set "NOME_ENV=venv"
call %NOME_ENV%\Scripts\activate
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1

:iniciar_programa
call %NOME_ENV%\Scripts\activate

:: O comando pythonw inicia o script em background, sumindo instantaneamente com o terminal
start "" %NOME_ENV%\Scripts\pythonw.exe main.py

call %NOME_ENV%\Scripts\deactivate
exit
