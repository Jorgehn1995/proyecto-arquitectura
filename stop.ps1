#!/usr/bin/env pwsh
# Script para detener todos los servicios

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Deteniendo servicios...              " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Preguntar si se deben eliminar los volúmenes
Write-Host "¿Deseas eliminar también los volúmenes (base de datos)? (S/N)" -ForegroundColor Yellow
Write-Host "⚠️  Esto eliminará todos los datos de la base de datos" -ForegroundColor Red
$deleteVolumes = Read-Host

Write-Host ""
Write-Host "Deteniendo contenedores..." -ForegroundColor Yellow

if ($deleteVolumes -eq "S" -or $deleteVolumes -eq "s") {
    docker-compose down -v
    Write-Host "✓ Servicios detenidos y volúmenes eliminados" -ForegroundColor Green
} else {
    docker-compose down
    Write-Host "✓ Servicios detenidos (volúmenes preservados)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Estado actual:" -ForegroundColor Cyan
docker-compose ps
