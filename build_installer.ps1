param(
    [ValidatePattern('^\d+\.\d+\.\d+([.-][0-9A-Za-z.-]+)?$')]
    [string]$Version = "1.0.0"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$distDirectory = Join-Path $projectRoot "dist"
$buildDirectory = Join-Path $projectRoot "build"
$mainScript = Join-Path $projectRoot "main.py"
$installerScript = Join-Path $projectRoot "installer\Posterizador.iss"

$compiler = Get-Command ISCC.exe -ErrorAction SilentlyContinue
if ($compiler) {
    $compilerPath = $compiler.Source
}
else {
    $compilerCandidates = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 6\ISCC.exe"),
        (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe"),
        (Join-Path $env:ProgramFiles "Inno Setup 6\ISCC.exe")
    )
    $compilerPath = $compilerCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}

if (-not $compilerPath) {
    throw "Inno Setup 6 nao foi encontrado. Instale-o ou adicione ISCC.exe ao PATH."
}

& python -m PyInstaller --noconfirm --clean --windowed --name Posterizador `
    --distpath $distDirectory --workpath $buildDirectory --specpath $buildDirectory `
    $mainScript
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao empacotar o aplicativo com PyInstaller."
}

& $compilerPath "/DMyAppVersion=$Version" $installerScript
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao criar o instalador com Inno Setup."
}

Write-Host "Instalador criado em: $(Join-Path $distDirectory 'Posterizador-Setup.exe')"
