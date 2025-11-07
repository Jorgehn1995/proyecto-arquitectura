#!/usr/bin/env pwsh
# Script para ver logs de los servicios

param(
    [string]$Service = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Logs del proyecto                    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($Service -eq "") {
    Write-Host "Selecciona el servicio:" -ForegroundColor Yellow
    Write-Host "1) Todos los servicios" -ForegroundColor White
    Write-Host "2) Frontend" -ForegroundColor White
    Write-Host "3) Backend" -ForegroundColor White
    Write-Host "4) Database" -ForegroundColor White
    Write-Host ""
    $option = Read-Host "Opción (1-4)"

    switch ($option) {
        "1" { $Service = "" }
        "2" { $Service = "frontend" }
        "3" { $Service = "backend" }
        "4" { $Service = "db" }
        default { 
            Write-Host "Opción inválida" -ForegroundColor Red
            exit 1
        }
    }
}

Write-Host ""
Write-Host "Mostrando logs... (Presiona Ctrl+C para salir)" -ForegroundColor Gray
Write-Host ""

if ($Service -eq "") {
    docker-compose logs -f
} else {
    docker-compose logs -f $Service
}
