#!/usr/bin/env pwsh
# Script de inicio rápido para levantar el proyecto completo

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Proyecto 2 - Arquitectura Software  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Docker está corriendo
Write-Host "Verificando Docker..." -ForegroundColor Yellow
$dockerRunning = docker info 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: Docker no está corriendo. Por favor, inicia Docker Desktop." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Docker está corriendo" -ForegroundColor Green
Write-Host ""

# Verificar si existe el archivo .env
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  No se encontró el archivo .env" -ForegroundColor Yellow
    Write-Host "Creando archivo .env desde .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Archivo .env creado. Revisa y ajusta las configuraciones si es necesario." -ForegroundColor Green
    Write-Host ""
}

# Preguntar modo de ejecución
Write-Host "Selecciona el modo de ejecución:" -ForegroundColor Cyan
Write-Host "1) Desarrollo (con hot-reload)" -ForegroundColor White
Write-Host "2) Producción (build optimizado)" -ForegroundColor White
Write-Host ""
$mode = Read-Host "Opción (1 o 2)"

$composeFile = "docker-compose.yml"
$modeName = "Desarrollo"

if ($mode -eq "2") {
    $composeFile = "docker-compose.prod.yml"
    $modeName = "Producción"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Iniciando en modo: $modeName" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Detener contenedores existentes
Write-Host "Deteniendo contenedores existentes..." -ForegroundColor Yellow
docker-compose down 2>&1 | Out-Null

# Construir imágenes
Write-Host "Construyendo imágenes Docker..." -ForegroundColor Yellow
Write-Host "(Esto puede tomar varios minutos la primera vez)" -ForegroundColor Gray
docker-compose -f $composeFile build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al construir las imágenes." -ForegroundColor Red
    exit 1
}

# Levantar servicios
Write-Host ""
Write-Host "Levantando servicios..." -ForegroundColor Yellow
docker-compose -f $composeFile up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al levantar los servicios." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Servicios iniciados correctamente!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Mostrar información de acceso
Write-Host "📍 URLs de acceso:" -ForegroundColor Cyan
Write-Host "   Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   Database:  localhost:5432" -ForegroundColor White
Write-Host ""

Write-Host "📊 Ver logs:" -ForegroundColor Cyan
Write-Host "   docker-compose -f $composeFile logs -f" -ForegroundColor Gray
Write-Host ""

Write-Host "🛑 Detener servicios:" -ForegroundColor Cyan
Write-Host "   docker-compose -f $composeFile down" -ForegroundColor Gray
Write-Host ""

# Esperar a que los servicios estén listos
Write-Host "Esperando a que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verificar estado de los servicios
Write-Host ""
Write-Host "Estado de los servicios:" -ForegroundColor Cyan
docker-compose -f $composeFile ps

Write-Host ""
Write-Host "¿Deseas ver los logs en tiempo real? (S/N)" -ForegroundColor Yellow
$showLogs = Read-Host

if ($showLogs -eq "S" -or $showLogs -eq "s") {
    Write-Host ""
    Write-Host "Mostrando logs... (Presiona Ctrl+C para salir)" -ForegroundColor Gray
    docker-compose -f $composeFile logs -f
}
