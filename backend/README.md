# 🚀 Flask REST API - Proyecto 2## 🚀 INSTRUCCIONES PARA EL PROYECTO



API REST completa construida con **Flask**, **PostgreSQL**, **Docker**, **Alembic** y **Swagger UI**.Crea un proyecto de **API REST completa en Python (Flask)** con las siguientes características y estructura.

El proyecto debe poder ejecutarse en **Docker** con `docker-compose` y quedar accesible en `http://localhost:8000`.

## ✨ CaracterísticasDebe incluir **Swagger UI**, **Alembic**, **SQLAlchemy**, **Pydantic** para validaciones, y **datos de prueba** cargados automáticamente.



- ✅ **CRUD completo** para Users, Reads, Access---

- ✅ **Relaciones complejas** (Read → Pump, Sensor, Fan)

- ✅ **Validación con Pydantic**### 🧩 Requerimientos funcionales

- ✅ **Migraciones con Alembic**

- ✅ **Documentación Swagger UI automática**Endpoints principales:

- ✅ **Docker y Docker Compose**

- ✅ **Endpoint de verificación de tags RFID**1. `/users` — CRUD completo (GET list, GET by id, POST, PUT, DELETE).

- ✅ **Seeds para datos de prueba**2. `/reads` — CRUD completo con relaciones anidadas (detallado más abajo).

3. `/access` — CRUD básico.

## 🛠️ Stack Tecnológico4. `/tags/{tag}/check` — método GET que recibe un código RFID.



- Python 3.11   * Si el `tag` pertenece a un usuario → devolver `200` con los datos del usuario.

- Flask 3.0   * Si no está vinculado → devolver `404` con `{ "detail": "Tag not found" }`.

- Flask-Smorest (OpenAPI/Swagger)

- SQLAlchemy 2.0---

- PostgreSQL 15

- Alembic### 🗄️ Base de datos (PostgreSQL)

- Pydantic

- Docker & Docker ComposeDebe correr en `docker-compose` y usarse mediante SQLAlchemy.

- Gunicorn

**Tablas:**

## 📦 Instalación y Ejecución

#### users

### Usando Docker (Recomendado)

* `id` SERIAL (PK)

1. **Clonar el repositorio y navegar al directorio backend:*** `first_name` VARCHAR (no nulo)

   ```bash* `last_name` VARCHAR (no nulo)

   cd backend* `email` VARCHAR (único, no nulo)

   ```* `rfid_tag` VARCHAR (único, nullable)

* `created_at` TIMESTAMP (default now)

2. **Levantar los servicios con Docker Compose:**

   ```bash#### reads

   docker-compose up --build

   ```* `id` SERIAL (PK)

* `name` VARCHAR (no nulo)

   Esto hará:* `timestamp` TIMESTAMP (default now)

   - ✅ Crear la base de datos PostgreSQL* `user_id` INTEGER FK → users.id (nullable)

   - ✅ Ejecutar las migraciones de Alembic* `created_at` TIMESTAMP (default now)

   - ✅ Insertar datos de prueba (seeds)

   - ✅ Iniciar la API en http://localhost:8000#### pumps



3. **Acceder a la documentación Swagger UI:*** `id` SERIAL (PK)

   ```* `read_id` INTEGER FK → reads.id (único, no nulo)

   http://localhost:8000/docs* `name` VARCHAR (no nulo)

   ```* `status` BOOLEAN (no nulo)



### Instalación Local (Sin Docker)#### sensors



1. **Crear entorno virtual:*** `id` SERIAL (PK)

   ```bash* `read_id` INTEGER FK → reads.id (único, no nulo)

   python -m venv venv* `name` VARCHAR (no nulo)

   .\venv\Scripts\activate  # Windows* `humidity` FLOAT (no nulo)

   source venv/bin/activate # Linux/Mac* `temperature` FLOAT (no nulo)

   ```

#### fans

2. **Instalar dependencias:**

   ```bash* `id` SERIAL (PK)

   pip install -r requirements.txt* `read_id` INTEGER FK → reads.id (único, no nulo)

   ```* `name` VARCHAR (no nulo)

* `status` BOOLEAN (no nulo)

3. **Configurar variables de entorno:**

   Editar `.env` con tu configuración local de PostgreSQL#### access



4. **Ejecutar migraciones:*** `id` SERIAL (PK)

   ```bash* `user_id` INTEGER FK → users.id (no nulo)

   alembic upgrade head* `timestamp` TIMESTAMP (default now)

   ```

---

5. **Sembrar datos de prueba:**

   ```bash### ⚙️ Tecnologías y librerías

   python manage.py seed

   ```* Python 3.11+

* Flask

6. **Iniciar servidor:*** SQLAlchemy (ORM)

   ```bash* Alembic (migraciones)

   python -m app* Flask-Migrate o configuración directa de Alembic

   ```* Pydantic (validación de datos)

* flask-smorest o flask-restx para Swagger UI

## 📚 Endpoints Disponibles* psycopg2-binary

* python-dotenv

### 🔍 Documentación* gunicorn (para correr en contenedor)

- `GET /` - Información de la API* pytest (opcional)

- `GET /docs` - Swagger UI (documentación interactiva)

- `GET /health` - Health check---



### 👥 Users### 📁 Estructura de proyecto

- `GET /users` - Lista todos los usuarios

- `POST /users` - Crea un usuario```

- `GET /users/<id>` - Obtiene un usuarioproject_root/

- `PUT /users/<id>` - Actualiza un usuario├─ app/

- `DELETE /users/<id>` - Elimina un usuario│  ├─ __init__.py

│  ├─ config.py

### 📊 Reads│  ├─ db.py

- `GET /reads` - Lista todos los reads│  ├─ models.py

- `POST /reads` - Crea un read (con pump, sensor, fan)│  ├─ schemas.py

- `GET /reads/<id>` - Obtiene un read│  ├─ api/

- `PUT /reads/<id>` - Actualiza un read│  │  ├─ __init__.py

- `DELETE /reads/<id>` - Elimina un read│  │  ├─ users.py

│  │  ├─ reads.py

### 🚪 Access│  │  ├─ access.py

- `GET /access` - Lista accesos│  ├─ seeds.py

- `POST /access` - Registra un acceso├─ alembic/

- `GET /access/<id>` - Obtiene un acceso│  └─ versions/

- `DELETE /access/<id>` - Elimina un acceso├─ Dockerfile

├─ docker-compose.yml

### 🏷️ Tags (RFID)├─ requirements.txt

- `GET /tags/<tag>/check` - Verifica si un tag RFID existe├─ manage.py

├─ README.md

## 💡 Ejemplos de Uso```



### Crear un Usuario---

```bash

curl -X POST http://localhost:8000/users \### 🧠 Lógica y validaciones

  -H "Content-Type: application/json" \

  -d '{#### `/users`

    "first_name": "Juan",

    "last_name": "Pérez",CRUD completo:

    "email": "juan@example.com",

    "rfid_tag": "TAG123"* `POST` valida email único.

  }'* `rfid_tag` puede ser null o string única.

```* Al eliminar usuario, sus `access` quedan eliminados en cascada.



### Verificar un Tag RFID---

```bash

curl http://localhost:8000/tags/ABC123/check#### `/reads`

```

Debe manejar estructuras anidadas según los tipos del frontend:

**Respuesta exitosa (200):**

```json```ts

{export interface Read {

  "id": 1,  id: number;

  "first_name": "Jorge",  name: string;

  "last_name": "Hernández",  pump: Pump;

  "email": "jorge@example.com",  sensor: Sensor;

  "rfid_tag": "ABC123",  fan: Fan;

  "created_at": "2025-11-07T12:00:00"  timestamp: Date;

}}

```export interface Pump {

  id: number;

**Tag no encontrado (404):**  readId: number;

```json  name: string;

{  status: boolean;

  "message": "Tag not found"}

}export interface Sensor {

```  id: number;

  readId: number;

### Crear un Read con entidades relacionadas  name: string;

```bash  humidity: number;

curl -X POST http://localhost:8000/reads \  temperature: number;

  -H "Content-Type: application/json" \}

  -d '{export interface Fan {

    "name": "Lectura Sensor Principal",  id: number;

    "user_id": 1,  readId: number;

    "pump": {  name: string;

      "name": "Bomba Principal",  status: boolean;

      "status": true}

    },```

    "sensor": {

      "name": "DHT22",**Relaciones:**

      "humidity": 65.5,

      "temperature": 23.8* `Read` tiene 1 `Pump`, 1 `Sensor`, 1 `Fan`.

    },* Relaciones `one-to-one` en SQLAlchemy con `cascade="all, delete-orphan"`.

    "fan": {

      "name": "Ventilador Extracción",**Pydantic Schemas:**

      "status": false

    }* `PumpCreate`, `PumpRead` → `name`, `status`

  }'* `SensorCreate`, `SensorRead` → `name`, `humidity`, `temperature`

```* `FanCreate`, `FanRead` → `name`, `status`

* `ReadCreate` → `name`, `timestamp`, `user_id`, `pump`, `sensor`, `fan`

## 🗄️ Esquema de Base de Datos* `ReadRead` → incluye las relaciones anidadas



### Tabla `users`**Validaciones:**

| Campo      | Tipo      | Restricciones    |

|------------|-----------|------------------|* `humidity` entre 0 y 100.

| id         | SERIAL    | PK               |* `temperature` entre -50 y 100.

| first_name | VARCHAR   | NOT NULL         |* `name` no vacío.

| last_name  | VARCHAR   | NOT NULL         |* Si `user_id` no existe, devolver 400.

| email      | VARCHAR   | UNIQUE, NOT NULL |

| rfid_tag   | VARCHAR   | UNIQUE, NULL     |**Endpoints `/reads`:**

| created_at | TIMESTAMP | DEFAULT now()    |

* `POST /reads` — crear lectura con datos anidados (pump, sensor, fan).

### Tabla `reads`* `GET /reads` — listar todas las lecturas con datos anidados.

| Campo      | Tipo      | Restricciones |* `GET /reads/{id}` — obtener lectura con detalles.

|------------|-----------|---------------|* `PUT /reads/{id}` — actualizar `read` y sus subentidades.

| id         | SERIAL    | PK            |* `DELETE /reads/{id}` — eliminar lectura (borrado en cascada).

| name       | VARCHAR   | NOT NULL      |

| timestamp  | TIMESTAMP | DEFAULT now() |Ejemplo de request:

| user_id    | INTEGER   | FK → users.id |

| created_at | TIMESTAMP | DEFAULT now() |```json

{

### Relaciones One-to-One  "name": "Lectura principal",

- `reads` ↔ `pumps` (1:1)  "user_id": 1,

- `reads` ↔ `sensors` (1:1)  "pump": {"name": "Pump A", "status": true},

- `reads` ↔ `fans` (1:1)  "sensor": {"name": "Sensor A", "humidity": 55.3, "temperature": 22.4},

  "fan": {"name": "Fan A", "status": false}

## 🧪 Datos de Prueba}

```

Los seeds incluyen:

---

**Usuarios:**

- Jorge Hernández (jorge@example.com) - Tag: ABC123#### `/access`

- Ana Pérez (ana@example.com) - Sin tag

- Luis Martínez (luis@example.com) - Tag: XYZ789CRUD básico:



**Reads:*** `user_id` requerido.

- 2 lecturas con sus respectivos pump, sensor y fan* `timestamp` default `now()`.



**Access:**---

- 2 registros de acceso

#### `/tags/{tag}/check`

## 🔧 Comandos Útiles

* Consulta `users` por `rfid_tag`.

### Docker* Si existe → `200` con `{id, first_name, last_name, email}`.

```bash* Si no → `404` con `{ "detail": "Tag not found" }`.

# Ver logs de la API

docker-compose logs -f web---



# Ver logs de la BD### 🧪 Datos de prueba (seed)

docker-compose logs -f db

Cargar automáticamente si la base está vacía:

# Detener servicios

docker-compose down**Users**



# Eliminar volúmenes (resetear BD)```py

docker-compose down -v[

  {"first_name": "Jorge", "last_name": "Hernández", "email": "jorge@example.com", "rfid_tag": "ABC123"},

# Ejecutar comando en el contenedor  {"first_name": "Ana", "last_name": "Pérez", "email": "ana@example.com"}

docker-compose exec web python manage.py seed]

``````



### Alembic (Migraciones)**Reads**

```bash3 lecturas con datos completos (pump, sensor, fan).

# Crear nueva migración

alembic revision --autogenerate -m "descripción"**Access**

3 registros asociados a usuarios existentes.

# Aplicar migraciones

alembic upgrade head---



# Revertir última migración### 🐳 Docker y despliegue

alembic downgrade -1

```**Dockerfile**



### Base de Datos* Base: `python:3.11-slim`

```bash* Instalar requirements

# Conectar a PostgreSQL (desde host)* Copiar el código

docker-compose exec db psql -U postgres -d flaskdb* Exponer puerto 8000

* Comando final:

# Resetear y sembrar BD

docker-compose exec web python manage.py seed  ```

```  CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]

  ```

## 📝 Variables de Entorno

**docker-compose.yml**

Archivo `.env`:

```env```yaml

DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/flaskdbversion: "3.9"

POSTGRES_USER=postgresservices:

POSTGRES_PASSWORD=postgres  db:

POSTGRES_DB=flaskdb    image: postgres:15

```    restart: always

    environment:

## 🏗️ Estructura del Proyecto      POSTGRES_USER: postgres

      POSTGRES_PASSWORD: postgres

```      POSTGRES_DB: flaskdb

backend/    volumes:

├── app/      - pgdata:/var/lib/postgresql/data

│   ├── __init__.py          # Factory de Flask app  web:

│   ├── config.py            # Configuración    build: .

│   ├── db.py                # Inicialización de SQLAlchemy    ports:

│   ├── models.py            # Modelos SQLAlchemy      - "8000:8000"

│   ├── schemas.py           # Esquemas Pydantic    depends_on:

│   ├── seeds.py             # Datos de prueba      - db

│   └── api/    environment:

│       ├── __init__.py      DATABASE_URL: postgresql+psycopg2://postgres:postgres@db:5432/flaskdb

│       ├── users.py         # Endpoints de usuariosvolumes:

│       ├── reads.py         # Endpoints de reads  pgdata:

│       ├── access.py        # Endpoints de accesos```

│       └── tags.py          # Endpoint de verificación RFID

├── alembic/**Al iniciar el contenedor web:**

│   ├── env.py               # Config de Alembic

│   ├── script.py.mako       # Template de migraciones1. Esperar DB (`wait-for-db.sh`).

│   └── versions/            # Migraciones2. Ejecutar `alembic upgrade head`.

├── docker/3. Ejecutar `python manage.py seed`.

│   └── wait-for-db.sh       # Script de espera de BD4. Lanzar `gunicorn`.

├── .env                     # Variables de entorno

├── .gitignore---

├── alembic.ini              # Configuración de Alembic

├── docker-compose.yml       # Orquestación de servicios### 📘 Swagger / Documentación

├── Dockerfile               # Imagen de la API

├── manage.py                # Script de gestión* Documentación visible en `/docs` o `/`.

├── requirements.txt         # Dependencias Python* Debe mostrar todos los endpoints, modelos Pydantic y ejemplos de request/response.

└── README.md               # Este archivo

```---



## 🚀 Próximos Pasos### 🧰 README.md



- [ ] Agregar autenticación JWTIncluir instrucciones:

- [ ] Implementar rate limiting

- [ ] Agregar tests unitarios con pytest```bash

- [ ] Implementar logging avanzado# Levantar el proyecto

- [ ] Agregar caché con Redisdocker-compose up --build

- [ ] Métricas con Prometheus

# Acceder a la API

## 📄 Licenciahttp://localhost:8000



Este proyecto es de código abierto y está disponible bajo la licencia MIT.# Swagger UI

http://localhost:8000/docs

## 👨‍💻 Autor

# Probar endpoints

Proyecto 2 - Arquitectura de Software - UMGcurl http://localhost:8000/users

curl http://localhost:8000/tags/ABC123/check
```

---

### ✅ Casos de prueba esperados

* Crear user con email duplicado → 400.
* Consultar tag existente → 200.
* Consultar tag inexistente → 404.
* Crear read con nested objects → 201.
* Eliminar read → elimina pump/sensor/fan asociados.

---

### 💾 Migraciones Alembic

* Configurar `alembic/env.py` con `app.models.Base.metadata`.
* Crear migración inicial `alembic revision --autogenerate -m "initial"`.
* Incluir archivo en `alembic/versions/`.

---

**Resultado esperado:**
Un proyecto Flask en Docker funcional, con Swagger UI, Alembic, Pydantic, PostgreSQL, CRUD de users/reads/access y validación de tags RFID.

---

¿Quieres que te genere ahora el **código completo del proyecto** (con todos los archivos) para copiarlo o descargarlo? Puedo hacerlo en formato ZIP o en el canvas.
