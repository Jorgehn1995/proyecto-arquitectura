# 📡 API Reference - Documentación de Endpoints

## 🌐 URL Base

```
http://localhost:8000
```

## 📋 Tabla de Contenidos

- [Autenticación](#autenticación)
- [Endpoints Generales](#endpoints-generales)
- [Users API](#users-api)
- [Reads API](#reads-api)
- [Access API](#access-api)
- [Tags API](#tags-api)
- [Thresholds API](#thresholds-api)
- [Códigos de Estado](#códigos-de-estado)
- [Modelos de Datos](#modelos-de-datos)

---

## 🔐 Autenticación

**Actualmente:** Sin autenticación (versión de desarrollo)

**Futuro:** JWT tokens o API keys

---

## 🏠 Endpoints Generales

### GET / - Información de la API

Devuelve información básica sobre la API.

**Request:**
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "message": "Flask API with Swagger",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### GET /health - Health Check

Verifica que la API está funcionando correctamente.

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "status": "ok"
}
```

**Códigos de estado:**
- `200 OK` - API funcionando correctamente

---

### GET /docs - Swagger UI

Documentación interactiva de la API (OpenAPI/Swagger).

**URL:** http://localhost:8000/docs

---

## 👥 Users API

### GET /users - Listar Usuarios

Obtiene una lista de todos los usuarios.

**Request:**
```http
GET /users HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
[
  {
    "id": 1,
    "first_name": "Jorge",
    "last_name": "Hernández",
    "email": "jorge@example.com",
    "rfid_tag": "ABC123",
    "created_at": "2025-11-07T12:00:00"
  },
  {
    "id": 2,
    "first_name": "Ana",
    "last_name": "Pérez",
    "email": "ana@example.com",
    "rfid_tag": null,
    "created_at": "2025-11-07T12:00:00"
  }
]
```

**Códigos de estado:**
- `200 OK` - Lista devuelta correctamente

---

### GET /users/{id} - Obtener Usuario

Obtiene un usuario específico por su ID.

**Request:**
```http
GET /users/1 HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "id": 1,
  "first_name": "Jorge",
  "last_name": "Hernández",
  "email": "jorge@example.com",
  "rfid_tag": "ABC123",
  "created_at": "2025-11-07T12:00:00"
}
```

**Códigos de estado:**
- `200 OK` - Usuario encontrado
- `404 Not Found` - Usuario no existe

---

### POST /users - Crear Usuario

Crea un nuevo usuario.

**Request:**
```http
POST /users HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "first_name": "María",
  "last_name": "González",
  "email": "maria@example.com",
  "rfid_tag": "MG456"
}
```

**Campos:**
- `first_name` (string, requerido): Nombre
- `last_name` (string, requerido): Apellido
- `email` (string, requerido): Email válido, único
- `rfid_tag` (string, opcional): Tag RFID único

**Response:**
```json
{
  "id": 4,
  "first_name": "María",
  "last_name": "González",
  "email": "maria@example.com",
  "rfid_tag": "MG456",
  "created_at": "2025-11-07T13:00:00"
}
```

**Códigos de estado:**
- `201 Created` - Usuario creado exitosamente
- `400 Bad Request` - Email o RFID tag duplicado
- `422 Unprocessable Entity` - Validación fallida

**Errores comunes:**
```json
{
  "message": "Email already exists"
}
```

---

### PUT /users/{id} - Actualizar Usuario

Actualiza un usuario existente.

**Request:**
```http
PUT /users/1 HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "first_name": "Jorge Luis",
  "rfid_tag": "ABC456"
}
```

**Campos (todos opcionales):**
- `first_name` (string): Nombre
- `last_name` (string): Apellido
- `email` (string): Email válido, único
- `rfid_tag` (string): Tag RFID único

**Response:**
```json
{
  "id": 1,
  "first_name": "Jorge Luis",
  "last_name": "Hernández",
  "email": "jorge@example.com",
  "rfid_tag": "ABC456",
  "created_at": "2025-11-07T12:00:00"
}
```

**Códigos de estado:**
- `200 OK` - Usuario actualizado
- `400 Bad Request` - Email o RFID tag duplicado
- `404 Not Found` - Usuario no existe
- `422 Unprocessable Entity` - Validación fallida

---

### DELETE /users/{id} - Eliminar Usuario

Elimina un usuario.

**Request:**
```http
DELETE /users/1 HTTP/1.1
Host: localhost:8000
```

**Response:**
```
(Sin contenido)
```

**Códigos de estado:**
- `204 No Content` - Usuario eliminado
- `404 Not Found` - Usuario no existe

---

## 📊 Reads API

### GET /reads - Listar Lecturas

Obtiene todas las lecturas con sus entidades relacionadas.

**Request:**
```http
GET /reads HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Read 1",
    "user_id": 1,
    "timestamp": "2025-11-07T12:00:00",
    "created_at": "2025-11-07T12:00:00",
    "pump": {
      "id": 1,
      "read_id": 1,
      "status": true
    },
    "sensor": {
      "id": 1,
      "read_id": 1,
      "humidity": 45.5,
      "temperature": 24.1
    },
    "fan": {
      "id": 1,
      "read_id": 1,
      "status": false
    },
    "smoke": {
      "id": 1,
      "read_id": 1,
      "status": false
    }
  }
]
```

**Códigos de estado:**
- `200 OK` - Lista devuelta correctamente

---

### GET /reads/{id} - Obtener Lectura

Obtiene una lectura específica.

**Request:**
```http
GET /reads/1 HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "id": 1,
  "name": "Read 1",
  "user_id": 1,
  "timestamp": "2025-11-07T12:00:00",
  "created_at": "2025-11-07T12:00:00",
  "pump": {
    "id": 1,
    "read_id": 1,
    "status": true
  },
  "sensor": {
    "id": 1,
    "read_id": 1,
    "humidity": 45.5,
    "temperature": 24.1
  },
  "fan": {
    "id": 1,
    "read_id": 1,
    "status": false
  },
  "smoke": {
    "id": 1,
    "read_id": 1,
    "status": false
  }
}
```

**Códigos de estado:**
- `200 OK` - Lectura encontrada
- `404 Not Found` - Lectura no existe

---

### POST /reads - Crear Lectura

Crea una nueva lectura con entidades anidadas opcionales.

**Request:**
```http
POST /reads HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "name": "Lectura Sensor Principal",
  "user_id": 1,
  "pump": {
    "status": true
  },
  "sensor": {
    "humidity": 65.5,
    "temperature": 23.8
  },
  "fan": {
    "status": false
  },
  "smoke": {
    "status": false
  }
}
```

**Campos:**
- `name` (string, requerido): Nombre de la lectura
- `user_id` (int, opcional): ID del usuario asociado
- `pump` (objeto, opcional):
  - `status` (boolean, requerido): Estado (encendido/apagado)
- `sensor` (objeto, opcional):
  - `humidity` (float, requerido): Humedad (0-100)
  - `temperature` (float, requerido): Temperatura
- `fan` (objeto, opcional):
  - `status` (boolean, requerido): Estado (encendido/apagado)
- `smoke` (objeto, opcional):
  - `status` (boolean, requerido): Estado (detectado/no detectado)

**Response:**
```json
{
  "id": 3,
  "name": "Lectura Sensor Principal",
  "user_id": 1,
  "timestamp": "2025-11-07T13:00:00",
  "created_at": "2025-11-07T13:00:00",
  "pump": {
    "id": 3,
    "read_id": 3,
    "status": true
  },
  "sensor": {
    "id": 3,
    "read_id": 3,
    "humidity": 65.5,
    "temperature": 23.8
  },
  "fan": {
    "id": 3,
    "read_id": 3,
    "status": false
  },
  "smoke": {
    "id": 3,
    "read_id": 3,
    "status": false
  }
}
```

**Códigos de estado:**
- `201 Created` - Lectura creada exitosamente
- `422 Unprocessable Entity` - Validación fallida

---

### PUT /reads/{id} - Actualizar Lectura

Actualiza solo los campos principales de una lectura (no actualiza pump, sensor, fan).

**Request:**
```http
PUT /reads/1 HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "name": "Read 1 - Actualizado",
  "user_id": 2
}
```

**Campos (todos opcionales):**
- `name` (string): Nombre de la lectura
- `user_id` (int): ID del usuario asociado

**Response:**
```json
{
  "id": 1,
  "name": "Read 1 - Actualizado",
  "user_id": 2,
  "timestamp": "2025-11-07T12:00:00",
  "created_at": "2025-11-07T12:00:00",
  "pump": {...},
  "sensor": {...},
  "fan": {...}
}
```

**Códigos de estado:**
- `200 OK` - Lectura actualizada
- `404 Not Found` - Lectura no existe

---

### DELETE /reads/{id} - Eliminar Lectura

Elimina una lectura y todas sus entidades relacionadas (cascada).

**Request:**
```http
DELETE /reads/1 HTTP/1.1
Host: localhost:8000
```

**Response:**
```
(Sin contenido)
```

**Códigos de estado:**
- `204 No Content` - Lectura eliminada
- `404 Not Found` - Lectura no existe

---

## 🚪 Access API

### GET /access - Listar Accesos

Obtiene todos los registros de acceso.

**Request:**
```http
GET /access HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "timestamp": "2025-11-07T12:00:00"
  },
  {
    "id": 2,
    "user_id": 3,
    "timestamp": "2025-11-07T12:05:00"
  }
]
```

**Códigos de estado:**
- `200 OK` - Lista devuelta correctamente

---

### GET /access/{id} - Obtener Acceso

Obtiene un registro de acceso específico.

**Request:**
```http
GET /access/1 HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "timestamp": "2025-11-07T12:00:00"
}
```

**Códigos de estado:**
- `200 OK` - Acceso encontrado
- `404 Not Found` - Acceso no existe

---

### POST /access - Crear Registro de Acceso

Registra un nuevo acceso para un usuario.

**Request:**
```http
POST /access HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "user_id": 1
}
```

**Campos:**
- `user_id` (int, requerido): ID del usuario que accede

**Response:**
```json
{
  "id": 3,
  "user_id": 1,
  "timestamp": "2025-11-07T13:00:00"
}
```

**Códigos de estado:**
- `201 Created` - Acceso registrado
- `404 Not Found` - Usuario no existe
- `422 Unprocessable Entity` - Validación fallida

---

### DELETE /access/{id} - Eliminar Registro de Acceso

Elimina un registro de acceso.

**Request:**
```http
DELETE /access/1 HTTP/1.1
Host: localhost:8000
```

**Response:**
```
(Sin contenido)
```

**Códigos de estado:**
- `204 No Content` - Acceso eliminado
- `404 Not Found` - Acceso no existe

---

## 🏷️ Tags API

### GET /tags/{tag}/check - Verificar Tag RFID

Verifica si un tag RFID está registrado y devuelve el usuario asociado.

**Request:**
```http
GET /tags/ABC123/check HTTP/1.1
Host: localhost:8000
```

**Response (Tag encontrado):**
```json
{
  "id": 1,
  "first_name": "Jorge",
  "last_name": "Hernández",
  "email": "jorge@example.com",
  "rfid_tag": "ABC123",
  "created_at": "2025-11-07T12:00:00"
}
```

**Response (Tag no encontrado):**
```json
{
  "message": "Tag not found"
}
```

**Códigos de estado:**
- `200 OK` - Tag encontrado, usuario devuelto
- `404 Not Found` - Tag no está registrado

**Casos de uso:**
- Control de acceso con RFID
- Verificación de tarjetas
- Sistemas de asistencia

---

## 🌡️ Thresholds API

### GET /thresholds - Obtener Umbrales

Obtiene los umbrales configurados de humedad y temperatura (solo existe 1 registro).

**Request:**
```http
GET /thresholds HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "id": 1,
  "min_humidity": 30.0,
  "max_humidity": 70.0,
  "min_temperature": 18.0,
  "max_temperature": 28.0,
  "created_at": "2025-11-07T12:00:00",
  "updated_at": "2025-11-07T12:00:00"
}
```

**Códigos de estado:**
- `200 OK` - Umbrales encontrados
- `404 Not Found` - No hay umbrales configurados

---

### GET /thresholds/{id} - Obtener Umbral por ID

Obtiene un umbral específico por su ID.

**Request:**
```http
GET /thresholds/1 HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "id": 1,
  "min_humidity": 30.0,
  "max_humidity": 70.0,
  "min_temperature": 18.0,
  "max_temperature": 28.0,
  "created_at": "2025-11-07T12:00:00",
  "updated_at": "2025-11-07T12:00:00"
}
```

**Códigos de estado:**
- `200 OK` - Umbral encontrado
- `404 Not Found` - Umbral no existe

---

### POST /thresholds - Crear/Actualizar Umbrales

Crea o actualiza los umbrales de humedad y temperatura. Solo puede existir un registro de umbrales.

**Request:**
```http
POST /thresholds HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "min_humidity": 35.0,
  "max_humidity": 65.0,
  "min_temperature": 20.0,
  "max_temperature": 26.0
}
```

**Campos:**
- `min_humidity` (float, requerido): Humedad mínima (0-100)
- `max_humidity` (float, requerido): Humedad máxima (0-100)
- `min_temperature` (float, requerido): Temperatura mínima
- `max_temperature` (float, requerido): Temperatura máxima

**Validaciones:**
- `min_humidity` ≤ `max_humidity`
- `min_temperature` ≤ `max_temperature`

**Response:**
```json
{
  "id": 1,
  "min_humidity": 35.0,
  "max_humidity": 65.0,
  "min_temperature": 20.0,
  "max_temperature": 26.0,
  "created_at": "2025-11-07T12:00:00",
  "updated_at": "2025-11-07T13:00:00"
}
```

**Códigos de estado:**
- `201 Created` - Umbrales creados/actualizados exitosamente
- `400 Bad Request` - Validación de rangos fallida
- `422 Unprocessable Entity` - Validación de datos fallida

---

### PUT /thresholds/{id} - Actualizar Umbrales

Actualiza parcialmente los umbrales existentes.

**Request:**
```http
PUT /thresholds/1 HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "max_humidity": 75.0,
  "max_temperature": 30.0
}
```

**Campos (todos opcionales):**
- `min_humidity` (float): Humedad mínima (0-100)
- `max_humidity` (float): Humedad máxima (0-100)
- `min_temperature` (float): Temperatura mínima
- `max_temperature` (float): Temperatura máxima

**Response:**
```json
{
  "id": 1,
  "min_humidity": 35.0,
  "max_humidity": 75.0,
  "min_temperature": 20.0,
  "max_temperature": 30.0,
  "created_at": "2025-11-07T12:00:00",
  "updated_at": "2025-11-07T13:30:00"
}
```

**Códigos de estado:**
- `200 OK` - Umbrales actualizados
- `400 Bad Request` - Validación de rangos fallida
- `404 Not Found` - Umbral no existe
- `422 Unprocessable Entity` - Validación de datos fallida

---

### DELETE /thresholds/{id} - Eliminar Umbrales

Elimina la configuración de umbrales.

**Request:**
```http
DELETE /thresholds/1 HTTP/1.1
Host: localhost:8000
```

**Response:**
```
(Sin contenido)
```

**Códigos de estado:**
- `204 No Content` - Umbrales eliminados
- `404 Not Found` - Umbral no existe

---

### POST /thresholds/validate - Validar Lecturas

Valida si las lecturas de humedad y temperatura están dentro de los umbrales configurados.

**Request:**
```http
POST /thresholds/validate HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "humidity": 55.5,
  "temperature": 23.2
}
```

**Campos:**
- `humidity` (float, requerido): Valor de humedad (0-100)
- `temperature` (float, requerido): Valor de temperatura

**Response (dentro de umbrales):**
```json
{
  "status": "ok",
  "message": "Sensor readings are within thresholds",
  "humidity": 55.5,
  "temperature": 23.2,
  "thresholds": {
    "min_humidity": 30.0,
    "max_humidity": 70.0,
    "min_temperature": 18.0,
    "max_temperature": 28.0
  }
}
```

**Response (fuera de umbrales):**
```json
{
  "status": "outside_thresholds",
  "message": "Sensor readings are outside configured thresholds",
  "errors": [
    "Humidity 85.5 is above maximum threshold 70.0"
  ],
  "humidity": 85.5,
  "temperature": 23.2,
  "thresholds": {
    "min_humidity": 30.0,
    "max_humidity": 70.0,
    "min_temperature": 18.0,
    "max_temperature": 28.0
  }
}
```

**Códigos de estado:**
- `200 OK` - Lecturas dentro de umbrales
- `400 Bad Request` - Lecturas fuera de umbrales
- `404 Not Found` - No hay umbrales configurados
- `422 Unprocessable Entity` - Validación de datos fallida

**Casos de uso:**
- Monitoreo de condiciones ambientales
- Alertas automáticas por condiciones fuera de rango
- Control de sistemas de climatización
- Validación en tiempo real de sensores IoT

---

## 📊 Códigos de Estado HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Solicitud exitosa |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Solicitud exitosa sin contenido de respuesta |
| 400 | Bad Request | Solicitud mal formada o datos duplicados |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Validación de datos fallida |
| 500 | Internal Server Error | Error del servidor |

---

## 📦 Modelos de Datos

### User

```typescript
{
  id: integer
  first_name: string (1-100 chars, requerido)
  last_name: string (1-100 chars, requerido)
  email: string (email válido, único, requerido)
  rfid_tag: string | null (único, opcional)
  created_at: datetime
}
```

### Read

```typescript
{
  id: integer
  name: string (1-200 chars, requerido)
  timestamp: datetime
  user_id: integer | null (FK a users.id)
  created_at: datetime
  pump: Pump | null
  sensor: Sensor | null
  fan: Fan | null
  smoke: Smoke | null
}
```

### Pump

```typescript
{
  id: integer
  read_id: integer (FK a reads.id, único)
  status: boolean (requerido)
}
```

### Sensor

```typescript
{
  id: integer
  read_id: integer (FK a reads.id, único)
  humidity: float (0-100, requerido)
  temperature: float (requerido)
}
```

### Fan

```typescript
{
  id: integer
  read_id: integer (FK a reads.id, único)
  status: boolean (requerido)
}
```

### Smoke

```typescript
{
  id: integer
  read_id: integer (FK a reads.id, único)
  status: boolean (requerido)
}
```

### Access

```typescript
{
  id: integer
  user_id: integer (FK a users.id, requerido)
  timestamp: datetime
}
```

### Threshold

```typescript
{
  id: integer
  min_humidity: float (0-100, requerido)
  max_humidity: float (0-100, requerido)
  min_temperature: float (requerido)
  max_temperature: float (requerido)
  created_at: datetime
  updated_at: datetime
}
```

**Nota:** Solo puede existir un registro de umbrales en el sistema.

---

## 🧪 Ejemplos con PowerShell

### Crear Usuario y Verificar Tag

```powershell
# Crear usuario con tag
$user = @{
    first_name = "Carlos"
    last_name = "Méndez"
    email = "carlos@example.com"
    rfid_tag = "CM789"
} | ConvertTo-Json

$newUser = Invoke-RestMethod -Uri "http://localhost:8000/users" -Method Post -Body $user -ContentType "application/json"

# Verificar el tag
$tagCheck = Invoke-RestMethod -Uri "http://localhost:8000/tags/CM789/check"
Write-Host "Usuario encontrado: $($tagCheck.first_name) $($tagCheck.last_name)"
```

### Crear Lectura Completa

```powershell
$read = @{
    name = "Lectura Completa"
    user_id = 1
    pump = @{
        status = $true
    }
    sensor = @{
        humidity = 58.3
        temperature = 22.7
    }
    fan = @{
        status = $true
    }
    smoke = @{
        status = $false
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:8000/reads" -Method Post -Body $read -ContentType "application/json"
```

### Configurar y Validar Umbrales

```powershell
# Configurar umbrales
$thresholds = @{
    min_humidity = 30.0
    max_humidity = 70.0
    min_temperature = 18.0
    max_temperature = 28.0
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/thresholds" -Method Post -Body $thresholds -ContentType "application/json"

# Validar lecturas de sensores
$reading = @{
    humidity = 55.5
    temperature = 23.2
} | ConvertTo-Json

$validation = Invoke-RestMethod -Uri "http://localhost:8000/thresholds/validate" -Method Post -Body $reading -ContentType "application/json"
Write-Host "Estado: $($validation.status)"

# Obtener umbrales actuales
$currentThresholds = Invoke-RestMethod -Uri "http://localhost:8000/thresholds"
Write-Host "Humedad: $($currentThresholds.min_humidity)% - $($currentThresholds.max_humidity)%"
Write-Host "Temperatura: $($currentThresholds.min_temperature)°C - $($currentThresholds.max_temperature)°C"
```

---

## 📚 Recursos Adicionales

- **Swagger UI:** http://localhost:8000/docs (documentación interactiva)
- **Repositorio:** Ver código fuente en GitHub
- **Testing:** Ver [TESTING.md](./TESTING.md)
- **Troubleshooting:** Ver [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
