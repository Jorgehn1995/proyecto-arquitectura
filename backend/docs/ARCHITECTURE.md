# 📐 Arquitectura del Proyecto

## 🏗️ Stack Tecnológico

```
┌─────────────────────────────────────────────────────┐
│                    Frontend                          │
│              (Opcional - No incluido)                │
│                  http://localhost                    │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│                Flask REST API                        │
│              http://localhost:8000                   │
│  ┌───────────────────────────────────────────────┐  │
│  │  Flask + Flask-Smorest + Swagger UI           │  │
│  │  - Authentication & Validation                │  │
│  │  - Pydantic schemas                           │  │
│  │  - OpenAPI documentation                      │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              SQLAlchemy ORM Layer                    │
│  - Models & Relationships                            │
│  - Query Builder                                     │
│  - Database Session Management                       │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              PostgreSQL Database                     │
│              postgres://localhost:5432               │
│  - Users, Reads, Pumps, Sensors, Fans, Access       │
│  - Managed by Alembic migrations                     │
└─────────────────────────────────────────────────────┘
```

## 📊 Modelo de Datos (ERD)

```
┌─────────────┐
│    Users    │
├─────────────┤
│ id (PK)     │◄───────────────┐
│ first_name  │                │
│ last_name   │                │
│ email       │                │
│ rfid_tag    │                │
│ created_at  │                │
└─────────────┘                │
       ▲                       │
       │ 1                     │
       │                       │
       │ N                     │
┌─────────────┐         ┌──────────────┐
│   Reads     │         │   Access     │
├─────────────┤         ├──────────────┤
│ id (PK)     │         │ id (PK)      │
│ name        │         │ user_id (FK) │
│ timestamp   │         │ timestamp    │
│ user_id(FK) │         └──────────────┘
│ created_at  │
└─────────────┘
       ║ 1
       ║
       ║ 1:1
    ┌──╨──┬──────┬──────┐
    │     │      │      │
┌───▼────┐│  ┌───▼────┐ │ ┌───▼────┐
│ Pumps  ││  │Sensors │ │ │  Fans  │
├────────┤│  ├────────┤ │ ├────────┤
│id (PK) ││  │id (PK) │ │ │id (PK) │
│read_id ││  │read_id │ │ │read_id │
│name    ││  │name    │ │ │name    │
│status  ││  │humidity│ │ │status  │
└────────┘│  │temp    │ │ └────────┘
          │  └────────┘ │
          └─────────────┘
```

## 🔄 Flujo de Peticiones

### Ejemplo: Crear un Read con entidades anidadas

```
1. Cliente HTTP (Browser/Postman/curl)
        ↓
   POST /reads
   {
     "name": "Read 1",
     "user_id": 1,
     "pump": {...},
     "sensor": {...},
     "fan": {...}
   }
        ↓
2. Flask Router (Flask-Smorest)
        ↓
3. Validación Pydantic (ReadCreate schema)
        ↓
4. API Handler (app/api/reads.py)
        ↓
5. SQLAlchemy ORM
   - Create Read instance
   - Create Pump instance
   - Create Sensor instance
   - Create Fan instance
        ↓
6. Database Transaction
   - BEGIN
   - INSERT into reads
   - INSERT into pumps
   - INSERT into sensors
   - INSERT into fans
   - COMMIT
        ↓
7. Response (ReadResponse schema)
   {
     "id": 123,
     "name": "Read 1",
     "pump": {...},
     "sensor": {...},
     "fan": {...}
   }
        ↓
8. Cliente recibe respuesta (201 Created)
```

## 🗂️ Estructura de Directorios

```
backend/
│
├── 📁 app/                      # Aplicación Flask
│   ├── __init__.py              # Factory de la app + registro de blueprints
│   ├── config.py                # Configuración (DB, Swagger, etc.)
│   ├── db.py                    # Inicialización de SQLAlchemy
│   ├── models.py                # Modelos ORM (User, Read, Pump, etc.)
│   ├── schemas.py               # Esquemas Pydantic para validación
│   ├── seeds.py                 # Datos de prueba
│   │
│   └── 📁 api/                  # Endpoints REST
│       ├── __init__.py
│       ├── users.py             # CRUD de usuarios
│       ├── reads.py             # CRUD de lecturas
│       ├── access.py            # CRUD de accesos
│       └── tags.py              # Verificación de RFID
│
├── 📁 alembic/                  # Migraciones de base de datos
│   ├── env.py                   # Configuración de Alembic
│   ├── script.py.mako           # Template para migraciones
│   └── 📁 versions/             # Archivos de migración
│       └── 001_initial_migration.py
│
├── 📁 docker/                   # Scripts de Docker
│   └── wait-for-db.sh           # Espera a que PostgreSQL esté listo
│
├── 📄 .env                      # Variables de entorno
├── 📄 .env.example              # Ejemplo de variables
├── 📄 .gitignore                # Archivos ignorados por Git
├── 📄 alembic.ini               # Configuración de Alembic
├── 📄 docker-compose.yml        # Orquestación de servicios
├── 📄 Dockerfile                # Imagen de Docker
├── 📄 manage.py                 # Scripts de gestión (seeds, etc.)
├── 📄 requirements.txt          # Dependencias Python
│
├── 📄 README.md                 # Documentación completa
├── 📄 QUICKSTART.md             # Guía de inicio rápido
├── 📄 CHECKLIST.md              # Lista de verificación
├── 📄 WINDOWS_GUIDE.md          # Guía para Windows PowerShell
├── 📄 ARCHITECTURE.md           # Este archivo
│
├── 📄 test_api.sh               # Tests (Bash)
└── 📄 test_api.ps1              # Tests (PowerShell)
```

## 🔌 Endpoints API

```
┌─────────────────────────────────────────────┐
│          API Endpoints Structure             │
└─────────────────────────────────────────────┘

📍 Root & Health
├─ GET  /                   → API info
├─ GET  /health             → Health check
└─ GET  /docs               → Swagger UI

📍 Users (/users)
├─ GET    /users            → List all users
├─ POST   /users            → Create user
├─ GET    /users/{id}       → Get user by ID
├─ PUT    /users/{id}       → Update user
└─ DELETE /users/{id}       → Delete user

📍 Reads (/reads)
├─ GET    /reads            → List all reads
├─ POST   /reads            → Create read (+ pump, sensor, fan)
├─ GET    /reads/{id}       → Get read by ID
├─ PUT    /reads/{id}       → Update read
└─ DELETE /reads/{id}       → Delete read

📍 Access (/access)
├─ GET    /access           → List all access logs
├─ POST   /access           → Create access log
├─ GET    /access/{id}      → Get access by ID
└─ DELETE /access/{id}      → Delete access log

📍 Tags (/tags)
└─ GET    /tags/{tag}/check → Verify RFID tag
```

## 🐳 Docker Compose Services

```
┌────────────────────────────────────────────┐
│         Docker Compose Stack                │
└────────────────────────────────────────────┘

🐘 db (PostgreSQL)
   ├─ Image: postgres:15
   ├─ Port: 5432
   ├─ Volume: pgdata
   └─ Health check: pg_isready

🌐 web (Flask API)
   ├─ Build: Dockerfile
   ├─ Port: 8000
   ├─ Depends on: db
   ├─ Wait for DB → Run migrations → Seed data → Start Gunicorn
   └─ Workers: 4

📦 volumes
   └─ pgdata → Persistencia de PostgreSQL
```

## 🔐 Flujo de Seguridad (RFID Tag Check)

```
Cliente envía petición:
GET /tags/ABC123/check
        ↓
Flask Router
        ↓
TagCheck Handler (app/api/tags.py)
        ↓
Query database:
SELECT * FROM users WHERE rfid_tag = 'ABC123'
        ↓
     ┌──────┴──────┐
     │             │
  Encontrado   No encontrado
     │             │
     ↓             ↓
  200 OK        404 Not Found
  + User data   + Error message
```

## 🔄 Ciclo de Vida de la Aplicación

```
1. docker-compose up
        ↓
2. PostgreSQL inicia
        ↓
3. wait-for-db.sh espera
        ↓
4. alembic upgrade head (crea tablas)
        ↓
5. python manage.py seed (inserta datos)
        ↓
6. gunicorn inicia Flask app
        ↓
7. API lista en http://localhost:8000
        ↓
8. Swagger UI disponible en /docs
```

## 🧪 Testing Flow

```
Script de tests (test_api.ps1)
        ↓
1. Health Check
2. API Info
3. List Users
4. Get User by ID
5. Create User
6. Check Valid RFID Tag
7. Check Invalid RFID Tag
8. Create Read with nested entities
9. List Reads
10. Create Access Log
11. List Access Logs
        ↓
Resultados en consola
```

## 📈 Escalabilidad Futura

```
Actual:
┌─────────┐     ┌──────┐
│ Flask   │────▶│ PG   │
│ (1 inst)│     │ (1)  │
└─────────┘     └──────┘

Escalado horizontal:
┌──────────┐
│  Nginx   │
│ (Load    │
│ Balancer)│
└────┬─────┘
     │
  ┌──┴──┬──────┬──────┐
  ▼     ▼      ▼      ▼
┌────┐┌────┐┌────┐┌────┐
│API1││API2││API3││API4│
└──┬─┘└──┬─┘└──┬─┘└──┬─┘
   └─────┴─────┴─────┘
          ▼
     ┌─────────┐
     │PostgreSQL│
     │(Primary)│
     └────┬────┘
          ▼
     ┌─────────┐
     │PostgreSQL│
     │(Replica)│
     └─────────┘
```

## 🎯 Patrones de Diseño Utilizados

1. **Factory Pattern**: `create_app()` en `app/__init__.py`
2. **Repository Pattern**: SQLAlchemy como abstracción de datos
3. **DTO Pattern**: Pydantic schemas para transferencia de datos
4. **Blueprint Pattern**: Organización modular de endpoints
5. **Dependency Injection**: Flask context y SQLAlchemy session

## 🔧 Tecnologías y Librerías

| Componente | Tecnología | Versión | Propósito |
|-----------|-----------|---------|-----------|
| Backend Framework | Flask | 3.0 | API REST |
| API Documentation | Flask-Smorest | 0.44 | OpenAPI/Swagger |
| ORM | SQLAlchemy | 2.0 | Abstracción de BD |
| Migrations | Alembic | 1.13 | Versionado de esquemas |
| Validation | Pydantic | 2.5 | Validación de datos |
| Database | PostgreSQL | 15 | Persistencia |
| WSGI Server | Gunicorn | 21.2 | Servidor de producción |
| Containerization | Docker | - | Despliegue |
| Orchestration | Docker Compose | - | Multi-container |

---

## 📚 Referencias

- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/
- Alembic: https://alembic.sqlalchemy.org/
- PostgreSQL: https://www.postgresql.org/
- Docker: https://docs.docker.com/
