# API Testing Examples (PowerShell)

$BASE_URL = "http://localhost:8000"

Write-Host "===================================" -ForegroundColor Cyan
Write-Host "🧪 Testing Flask API" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1️⃣  Health Check" -ForegroundColor Yellow
Write-Host "GET $BASE_URL/health"
Invoke-RestMethod -Uri "$BASE_URL/health" -Method Get | ConvertTo-Json
Write-Host ""

# Test 2: API Info
Write-Host "2️⃣  API Information" -ForegroundColor Yellow
Write-Host "GET $BASE_URL/"
Invoke-RestMethod -Uri "$BASE_URL/" -Method Get | ConvertTo-Json
Write-Host ""

# Test 3: List Users
Write-Host "3️⃣  List All Users" -ForegroundColor Yellow
Write-Host "GET $BASE_URL/users"
Invoke-RestMethod -Uri "$BASE_URL/users" -Method Get | ConvertTo-Json
Write-Host ""

# Test 4: Get User by ID
Write-Host "4️⃣  Get User by ID" -ForegroundColor Yellow
Write-Host "GET $BASE_URL/users/1"
Invoke-RestMethod -Uri "$BASE_URL/users/1" -Method Get | ConvertTo-Json
Write-Host ""

# Test 5: Create User
Write-Host "5️⃣  Create New User" -ForegroundColor Yellow
Write-Host "POST $BASE_URL/users"
$newUser = @{
    first_name = "María"
    last_name = "González"
    email = "maria@example.com"
    rfid_tag = "MG456"
} | ConvertTo-Json
Invoke-RestMethod -Uri "$BASE_URL/users" -Method Post -Body $newUser -ContentType "application/json" | ConvertTo-Json
Write-Host ""

# Test 6: Check RFID Tag (Valid)
Write-Host "6️⃣  Check Valid RFID Tag" -ForegroundColor Yellow
Write-Host "GET $BASE_URL/tags/ABC123/check"
Invoke-RestMethod -Uri "$BASE_URL/tags/ABC123/check" -Method Get | ConvertTo-Json
Write-Host ""

# Test 7: Check RFID Tag (Invalid)
Write-Host "7️⃣  Check Invalid RFID Tag (should return 404)" -ForegroundColor Yellow
Write-Host "GET $BASE_URL/tags/INVALID/check"
try {
    Invoke-RestMethod -Uri "$BASE_URL/tags/INVALID/check" -Method Get | ConvertTo-Json
} catch {
    Write-Host "❌ Expected 404 error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 8: Create Read with nested entities
Write-Host "8️⃣  Create Read with Pump, Sensor, and Fan" -ForegroundColor Yellow
Write-Host "POST $BASE_URL/reads"
$newRead = @{
    name = "Lectura de Prueba"
    user_id = 1
    pump = @{
        name = "Bomba de Prueba"
        status = $true
    }
    sensor = @{
        name = "DHT11 Prueba"
        humidity = 50.0
        temperature = 25.0
    }
    fan = @{
        name = "Ventilador de Prueba"
        status = $false
    }
} | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BASE_URL/reads" -Method Post -Body $newRead -ContentType "application/json" | ConvertTo-Json
Write-Host ""

# Test 9: List Reads
Write-Host "9️⃣  List All Reads" -ForegroundColor Yellow
Write-Host "GET $BASE_URL/reads"
Invoke-RestMethod -Uri "$BASE_URL/reads" -Method Get | ConvertTo-Json
Write-Host ""

# Test 10: Create Access Log
Write-Host "🔟 Create Access Log" -ForegroundColor Yellow
Write-Host "POST $BASE_URL/access"
$newAccess = @{
    user_id = 1
} | ConvertTo-Json
Invoke-RestMethod -Uri "$BASE_URL/access" -Method Post -Body $newAccess -ContentType "application/json" | ConvertTo-Json
Write-Host ""

# Test 11: List Access Logs
Write-Host "1️⃣1️⃣  List All Access Logs" -ForegroundColor Yellow
Write-Host "GET $BASE_URL/access"
Invoke-RestMethod -Uri "$BASE_URL/access" -Method Get | ConvertTo-Json
Write-Host ""

Write-Host "===================================" -ForegroundColor Cyan
Write-Host "✅ Tests Completed!" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 For interactive testing, visit:" -ForegroundColor Yellow
Write-Host "   $BASE_URL/docs" -ForegroundColor Green
Write-Host ""
