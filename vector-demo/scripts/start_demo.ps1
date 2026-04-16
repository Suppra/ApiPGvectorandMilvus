# SCRIPT DE INICIO PARA EXPOSICIÓN
# Ejecuta: .\scripts\start_demo.ps1

param(
    [switch]$API,
    [switch]$Containers,
    [switch]$Demo,
    [switch]$All
)

$ErrorActionPreference = "Continue"
$WarningPreference = "Continue"

function Write-Success { Write-Host "✓ $args" -ForegroundColor Green }
function Write-Error { Write-Host "✗ $args" -ForegroundColor Red }
function Write-Info { Write-Host "ℹ $args" -ForegroundColor Cyan }
function Write-Header { Write-Host "`n$('='*70)`n  $args`n$('='*70)`n" -ForegroundColor Yellow }

function Start-Containers {
    Write-Header "Iniciando contenedores Docker"
    
    Write-Info "PGVector + PostgreSQL..."
    docker-compose -f docker-compose.pgvector.yml up -d 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "PGVector iniciado"
    } else {
        Write-Error "Error iniciando PGVector"
        return $false
    }
    
    Write-Info "Esperando 5 segundos..."
    Start-Sleep -Seconds 5
    
    Write-Info "Milvus..."
    docker-compose -f docker-compose.milvus.yml up -d 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Milvus iniciado"
    } else {
        Write-Error "Error iniciando Milvus"
        return $false
    }
    
    Write-Info "Esperando 15 segundos para que Milvus se inicialice..."
    Start-Sleep -Seconds 15
    
    Write-Success "Contenedores iniciados exitosamente"
    return $true
}

function Start-API {
    Write-Header "Iniciando API FastAPI"
    
    Write-Info "API en http://127.0.0.1:8000"
    Write-Info "Swagger en http://127.0.0.1:8000/docs"
    Write-Info "Presiona Ctrl+C para detener"
    
    & python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
}

function Start-Demo {
    Write-Header "Iniciando DEMO interactiva"
    
    Write-Info "Demo en: python scripts/demo_comparison.py"
    & python scripts/demo_comparison.py
}

# Verificar que estamos en la carpeta correcta
if (-not (Test-Path "docker-compose.pgvector.yml")) {
    Write-Error "Por favor, ejecuta este script desde la carpeta vector-demo"
    exit 1
}

# Si no hay parámetros, mostrar menú
if (-not $API -and -not $Containers -and -not $Demo -and -not $All) {
    Write-Header "DEMO: Comparación PGVector vs Milvus"
    
    Write-Host "     [A] - Iniciar TODO (Contenedores + API + Demo)"
    Write-Host "     [C] - Solo Contenedores"
    Write-Host "     [I] - Solo API"
    Write-Host "     [D] - Solo Demo"
    Write-Host "     [E] - Salir"
    
    $choice = Read-Host "`nSelecciona"
    
    switch ($choice.ToUpper()) {
        "A" { $All = $true }
        "C" { $Containers = $true }
        "I" { $API = $true }
        "D" { $Demo = $true }
        "E" { exit }
        default { Write-Error "Opción inválida"; exit 1 }
    }
}

# Ejecutar
if ($Containers -or $All) {
    Start-Containers
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

if ($API -or $All) {
    Start-API
}

if ($Demo -or $All) {
    Start-Demo
}

Write-Success "Demostración completada"
