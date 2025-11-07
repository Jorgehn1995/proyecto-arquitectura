

# 🚀 Proyecto API Flask + PostgreSQL + Docker + Alembic + Pydantic + Swagger UI

## 🧩 Descripción General

Este proyecto define una API REST construida con **Python (Flask)** y **PostgreSQL**, completamente **contenedorizada con Docker**.  
La API incluye **Swagger UI**, validaciones con **Pydantic**, migraciones con **Alembic**, y relaciones de datos según el siguiente esquema:

- **Users** (con RFID tag)
- **Reads** (con Pump, Sensor, Fan y Smoke)
- **Access**
- **Thresholds** (umbrales de humedad y temperatura)
- **Tag check** endpoint (`/tags/<tag>/check`)
- **Threshold validation** endpoint (`/thresholds/validate`)

Tanto la **API** como la **base de datos** se ejecutan dentro de contenedores Docker.  
El proyecto se levanta con un solo comando:  
````markdown
docker-compose up --build
````

---

## 🛠️ Requisitos Técnicos

* Python 3.11+
* Flask
* SQLAlchemy
* Alembic
* flask-smorest o flask-restx (para Swagger)
* Pydantic
* psycopg2-binary
* gunicorn
* python-dotenv

---

## 📁 Estructura del Proyecto

```
project_root/
├─ app/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ db.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ seeds.py
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ users.py
│  │  ├─ reads.py
│  │  ├─ access.py
│  └─ utils.py
├─ alembic/
│  ├─ env.py
│  └─ versions/
├─ docker/
│  ├─ wait-for-db.sh
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ manage.py
├─ README.md
└─ INSTRUCTIONS.md
```

---

## 🧱 Esquema de Base de Datos (PostgreSQL)

### Tabla `users`

| Campo      | Tipo      | Restricciones    |
| ---------- | --------- | ---------------- |
| id         | SERIAL    | PK               |
| first_name | VARCHAR   | NOT NULL         |
| last_name  | VARCHAR   | NOT NULL         |
| email      | VARCHAR   | UNIQUE, NOT NULL |
| rfid_tag   | VARCHAR   | UNIQUE, NULL     |
| created_at | TIMESTAMP | DEFAULT now()    |

### Tabla `reads`

| Campo      | Tipo      | Restricciones |
| ---------- | --------- | ------------- |
| id         | SERIAL    | PK            |
| name       | VARCHAR   | NOT NULL      |
| timestamp  | TIMESTAMP | DEFAULT now() |
| user_id    | INTEGER   | FK → users.id |
| created_at | TIMESTAMP | DEFAULT now() |

### Tabla `pumps`

| Campo   | Tipo    | Restricciones        |
| ------- | ------- | -------------------- |
| id      | SERIAL  | PK                   |
| read_id | INTEGER | UNIQUE FK → reads.id |
| status  | BOOLEAN | NOT NULL             |

### Tabla `sensors`

| Campo       | Tipo    | Restricciones        |
| ----------- | ------- | -------------------- |
| id          | SERIAL  | PK                   |
| read_id     | INTEGER | UNIQUE FK → reads.id |
| humidity    | FLOAT   | NOT NULL             |
| temperature | FLOAT   | NOT NULL             |

### Tabla `fans`

| Campo   | Tipo    | Restricciones        |
| ------- | ------- | -------------------- |
| id      | SERIAL  | PK                   |
| read_id | INTEGER | UNIQUE FK → reads.id |
| status  | BOOLEAN | NOT NULL             |

### Tabla `smokes`

| Campo   | Tipo    | Restricciones        |
| ------- | ------- | -------------------- |
| id      | SERIAL  | PK                   |
| read_id | INTEGER | UNIQUE FK → reads.id |
| status  | BOOLEAN | NOT NULL             |

### Tabla `access`

| Campo     | Tipo      | Restricciones |
| --------- | --------- | ------------- |
| id        | SERIAL    | PK            |
| user_id   | INTEGER   | FK → users.id |
| timestamp | TIMESTAMP | DEFAULT now() |

### Tabla `thresholds`

| Campo           | Tipo      | Restricciones |
| --------------- | --------- | ------------- |
| id              | SERIAL    | PK            |
| min_humidity    | FLOAT     | NOT NULL      |
| max_humidity    | FLOAT     | NOT NULL      |
| min_temperature | FLOAT     | NOT NULL      |
| max_temperature | FLOAT     | NOT NULL      |
| created_at      | TIMESTAMP | DEFAULT now() |
| updated_at      | TIMESTAMP | DEFAULT now() |

**Nota:** Solo debe existir un registro en esta tabla.

---

## ⚙️ Endpoints

### `/users`

| Método | Ruta          | Descripción              |
| ------ | ------------- | ------------------------ |
| GET    | `/users`      | Lista todos los usuarios |
| GET    | `/users/<id>` | Obtiene un usuario       |
| POST   | `/users`      | Crea un usuario          |
| PUT    | `/users/<id>` | Actualiza un usuario     |
| DELETE | `/users/<id>` | Elimina un usuario       |

### `/reads`

* CRUD completo para `reads` y sus entidades anidadas (`pump`, `sensor`, `fan`, `smoke`).
* Las relaciones son **uno a uno**.
* Ejemplo de payload para crear un `read`:

```json
{
  "name": "Read 1",
  "user_id": 1,
  "pump": { "status": true },
  "sensor": { "humidity": 45.5, "temperature": 24.1 },
  "fan": { "status": false },
  "smoke": { "status": false }
}
```

### `/access`

| Método | Ruta           | Descripción       |
| ------ | -------------- | ----------------- |
| GET    | `/access`      | Lista accesos     |
| POST   | `/access`      | Crea acceso       |
| GET    | `/access/<id>` | Obtiene un acceso |
| DELETE | `/access/<id>` | Elimina acceso    |

### `/tags/<tag>/check`

* **GET**: verifica si una tarjeta RFID (`tag`) está vinculada a un usuario.

  * Si existe → `200 OK`
  * Si no existe → `404 Not Found`

Ejemplo:

```bash
curl http://localhost:8000/tags/ABC123/check
```

Respuesta exitosa:

```json
{
  "id": 1,
  "first_name": "Jorge",
  "last_name": "Hernández",
  "email": "jorge@example.com"
}
```

### `/thresholds`

CRUD completo para gestionar umbrales de humedad y temperatura.

| Método | Ruta                     | Descripción                      |
| ------ | ------------------------ | -------------------------------- |
| GET    | `/thresholds`            | Obtiene los umbrales configurados |
| GET    | `/thresholds/<id>`       | Obtiene un umbral por ID         |
| POST   | `/thresholds`            | Crea/actualiza umbrales          |
| PUT    | `/thresholds/<id>`       | Actualiza umbrales parcialmente  |
| DELETE | `/thresholds/<id>`       | Elimina umbrales                 |
| POST   | `/thresholds/validate`   | Valida lecturas contra umbrales  |

**Ejemplo de validación:**

```bash
curl -X POST http://localhost:8000/thresholds/validate \
  -H "Content-Type: application/json" \
  -d '{"humidity": 55.5, "temperature": 23.2}'
```

Respuesta dentro de umbrales (`200 OK`):

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

Respuesta fuera de umbrales (`400 Bad Request`):

```json
{
  "status": "outside_thresholds",
  "message": "Sensor readings are outside configured thresholds",
  "errors": ["Humidity 85.5 is above maximum threshold 70.0"],
  "humidity": 85.5,
  "temperature": 23.2,
  "thresholds": {...}
}
```

---

## 🐳 Docker Compose

**docker-compose.yml**

* **db**: PostgreSQL 15, con volumen `pgdata`
* **web**: API Flask
* Dependencia: `depends_on: db`
* Puerto expuesto: `8000:8000`
* Secuencia:

  1. Espera la base de datos (`wait-for-db.sh`)
  2. Ejecuta migraciones con Alembic
  3. Inserta datos de prueba (`python manage.py seed`)
  4. Inicia Gunicorn en `0.0.0.0:8000`

---

## 🧾 Datos de Prueba (Seeds)

`app/seeds.py` debe insertar:

* **Usuarios**

  * Jorge Hernández (`jorge@example.com`, tag `ABC123`)
  * Ana Pérez (`ana@example.com`, sin tag)
* **Reads** con `pump`, `sensor`, `fan`, `smoke`
* **Access** de ejemplo
* **Threshold** con valores por defecto (humedad: 30-70%, temperatura: 18-28°C)

---

## 📚 Swagger UI

Disponible en:

```
http://localhost:8000/docs
```

Muestra modelos y ejemplos de requests/responses generados a partir de esquemas Pydantic.

---

## 🧠 Migraciones Alembic

* `alembic/env.py` importa `Base.metadata` desde `app.models`
* Ejemplo de creación:

  ```bash
  alembic revision --autogenerate -m "initial"
  alembic upgrade head
  ```

---

## 🧩 Ejemplo de Uso

Crear usuario:

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Luis", "last_name": "Martínez", "email": "luis@example.com", "rfid_tag": "XYZ789"}'
```

Verificar tag:

```bash
curl http://localhost:8000/tags/XYZ789/check
```

Validar lecturas de sensores:

```bash
curl -X POST http://localhost:8000/thresholds/validate \
  -H "Content-Type: application/json" \
  -d '{"humidity": 55.5, "temperature": 23.2}'
```

---

## 🔄 Iniciar el Proyecto

1. Clonar o generar el proyecto.
2. Ejecutar:

   ```bash
   docker-compose up --build
   ```
3. Acceder a la API:

   ```
   http://localhost:8000
   ```
4. Documentación:

   ```
   http://localhost:8000/docs
   ```

---

## 📦 Variables de Entorno

Crear archivo `.env` (ejemplo):

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/flaskdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=flaskdb
```

---

## ✅ Tests (opcional)

Agregar pruebas básicas en `tests/` con pytest:

* `GET /tags/ABC123/check` debe devolver 200.
* `GET /tags/INVALID/check` debe devolver 404.

---

## 🧭 Comandos Útiles

* Ejecutar migraciones manualmente:

  ```bash
  docker-compose run web alembic upgrade head
  ```
* Sembrar datos:

  ```bash
  docker-compose run web python manage.py seed
  ```
* Ver logs:

  ```bash
  docker-compose logs -f web
  ```

---

## 🧾 Créditos

Creado para un entorno de desarrollo moderno con Flask + SQLAlchemy + Docker + Alembic + Swagger UI + Pydantic.

