#!/bin/bash
# API Testing Examples

BASE_URL="http://localhost:8000"

echo "==================================="
echo "🧪 Testing Flask API"
echo "==================================="
echo ""

# Test 1: Health Check
echo "1️⃣  Health Check"
echo "GET $BASE_URL/health"
curl -X GET "$BASE_URL/health"
echo -e "\n"

# Test 2: API Info
echo "2️⃣  API Information"
echo "GET $BASE_URL/"
curl -X GET "$BASE_URL/"
echo -e "\n"

# Test 3: List Users
echo "3️⃣  List All Users"
echo "GET $BASE_URL/users"
curl -X GET "$BASE_URL/users"
echo -e "\n"

# Test 4: Get User by ID
echo "4️⃣  Get User by ID"
echo "GET $BASE_URL/users/1"
curl -X GET "$BASE_URL/users/1"
echo -e "\n"

# Test 5: Create User
echo "5️⃣  Create New User"
echo "POST $BASE_URL/users"
curl -X POST "$BASE_URL/users" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "María",
    "last_name": "González",
    "email": "maria@example.com",
    "rfid_tag": "MG456"
  }'
echo -e "\n"

# Test 6: Check RFID Tag (Valid)
echo "6️⃣  Check Valid RFID Tag"
echo "GET $BASE_URL/tags/ABC123/check"
curl -X GET "$BASE_URL/tags/ABC123/check"
echo -e "\n"

# Test 7: Check RFID Tag (Invalid)
echo "7️⃣  Check Invalid RFID Tag (should return 404)"
echo "GET $BASE_URL/tags/INVALID/check"
curl -X GET "$BASE_URL/tags/INVALID/check"
echo -e "\n"

# Test 8: Create Read with nested entities
echo "8️⃣  Create Read with Pump, Sensor, and Fan"
echo "POST $BASE_URL/reads"
curl -X POST "$BASE_URL/reads" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lectura de Prueba",
    "user_id": 1,
    "pump": {
      "name": "Bomba de Prueba",
      "status": true
    },
    "sensor": {
      "name": "DHT11 Prueba",
      "humidity": 50.0,
      "temperature": 25.0
    },
    "fan": {
      "name": "Ventilador de Prueba",
      "status": false
    }
  }'
echo -e "\n"

# Test 9: List Reads
echo "9️⃣  List All Reads"
echo "GET $BASE_URL/reads"
curl -X GET "$BASE_URL/reads"
echo -e "\n"

# Test 10: Create Access Log
echo "🔟 Create Access Log"
echo "POST $BASE_URL/access"
curl -X POST "$BASE_URL/access" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1
  }'
echo -e "\n"

# Test 11: List Access Logs
echo "1️⃣1️⃣  List All Access Logs"
echo "GET $BASE_URL/access"
curl -X GET "$BASE_URL/access"
echo -e "\n"

echo "==================================="
echo "✅ Tests Completed!"
echo "==================================="
echo ""
echo "📚 For interactive testing, visit:"
echo "   $BASE_URL/docs"
echo ""
