# Posterizador

Aplicativo Windows para dividir uma imagem em folhas A4 e gerar um PDF de pôster mosaico, com margens ajustadas para a Epson L3250.

## Criar o instalador localmente

Requisitos: Python 3.11 ou superior, Inno Setup 6 e as dependências Python do projeto.

```powershell
python -m pip install -r requirements.txt pyinstaller
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\build_installer.ps1 -Version 1.0.0
```

O instalador será criado em `dist\Posterizador-Setup.exe`. O instalador é por usuário (não exige privilégios de administrador) e oferece atalhos no menu Iniciar e, opcionalmente, na área de trabalho.

## Publicar uma versão

Ao enviar uma tag `v*` para o GitHub, a automação compila o aplicativo, cria o instalador e publica o arquivo em uma GitHub Release. Por exemplo:

```powershell
git tag v1.0.0
git push origin v1.0.0
```

Depois que a release for publicada, gere o manifesto do WinGet com a URL direta do instalador:

```powershell
wingetcreate new https://github.com/reginaldo-builds/posterizador.py/releases/download/v1.0.0/Posterizador-Setup.exe
```

Troque `v1.0.0` pela versão publicada. O `wingetcreate new` é interativo; revise os dados e o hash que ele detectar antes de submeter o manifesto.
