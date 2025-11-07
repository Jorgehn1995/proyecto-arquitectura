# Proyecto 2 - Arquitectura de Software

Aplicación full-stack con arquitectura multi-contenedor usando Docker.

## 📚 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| **[DOCKER.md](./DOCKER.md)** | 🐳 Guía completa de comandos Docker |
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | 🏗️ Diagramas y arquitectura del sistema |
| **[CHECKLIST.md](./CHECKLIST.md)** | ✅ Checklist de configuración paso a paso |
| **[TESTING.md](./TESTING.md)** | 🧪 Guía de testing y verificación |
| **[SUMMARY.md](./SUMMARY.md)** | 📦 Resumen de archivos y cambios |
| **[frontend/README.md](./frontend/README.md)** | 🎨 Documentación del Frontend |
| **[frontend/API_USAGE.md](./frontend/API_USAGE.md)** | 🔌 Guía de integración con API |

## 🏗️ Arquitectura

Este proyecto está dividido en tres servicios principales:

- **Frontend**: Aplicación Nuxt 3 (Puerto 3000)
- **Backend**: API Python/Flask (Puerto 8000)
- **Database**: PostgreSQL 15 (Puerto 5432)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │────▶│   Backend   │────▶│  Database   │
│  (Nuxt 3)   │     │   (Flask)   │     │(PostgreSQL) │
│   :3000     │     │    :8000    │     │    :5432    │
└─────────────┘     └─────────────┘     └─────────────┘
```

## 📋 Pre-requisitos

- Docker Desktop instalado
- Docker Compose V2
- Git

## 🚀 Inicio Rápido

### Método 1: Script Automático (Recomendado) ⭐

```powershell
# 1. Configurar variables de entorno
copy .env.example .env

# 2. Ejecutar script de inicio
.\start.ps1
```

### Método 2: Manual

```powershell
# 1. Configurar variables de entorno
copy .env.example .env

# 2. Levantar servicios
docker-compose up -d

# 3. Ver logs
docker-compose logs -f
```

### 4. Acceder a los servicios

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: localhost:5432

### 5. Verificar que todo funciona

Sigue la guía paso a paso: **[TESTING.md](./TESTING.md)** 🧪

## 🛠️ Comandos Útiles

### Ver logs de todos los servicios

```powershell
docker-compose logs -f
```

### Ver logs de un servicio específico

```powershell
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f db
```

### Detener todos los servicios

```powershell
docker-compose down
```

### Detener y eliminar volúmenes (⚠️ Elimina la base de datos)

```powershell
docker-compose down -v
```

### Reconstruir las imágenes

```powershell
docker-compose build
docker-compose up -d
```

### Reconstruir un servicio específico

```powershell
docker-compose build frontend
docker-compose up -d frontend
```

### Ejecutar comandos dentro de un contenedor

```powershell
# Backend - Ejecutar migraciones
docker-compose exec backend alembic upgrade head

# Backend - Seed de datos
docker-compose exec backend python manage.py seed

# Frontend - Instalar dependencias
docker-compose exec frontend pnpm install

# Base de datos - Acceder a psql
docker-compose exec db psql -U postgres -d flaskdb
```

## 📁 Estructura del Proyecto

```
proyecto2/
├── backend/                 # API Python/Flask
│   ├── app/                # Código de la aplicación
│   ├── alembic/            # Migraciones de base de datos
│   ├── docker/             # Scripts de Docker
│   ├── Dockerfile          # Imagen Docker del backend
│   └── requirements.txt    # Dependencias Python
│
├── frontend/               # Aplicación Nuxt 3
│   ├── app/               # Código de la aplicación
│   ├── Dockerfile         # Imagen Docker producción
│   ├── Dockerfile.dev     # Imagen Docker desarrollo
│   └── package.json       # Dependencias Node.js
│
├── docker-compose.yml      # Orquestación desarrollo
├── docker-compose.prod.yml # Orquestación producción
├── .env.example           # Variables de entorno ejemplo
└── README.md              # Este archivo
```

## 🔧 Desarrollo Local

### Backend

El backend usa hot-reload montando el código fuente como volumen. Los cambios se reflejan automáticamente.

```powershell
# Ver logs del backend
docker-compose logs -f backend

# Reiniciar el backend
docker-compose restart backend
```

### Frontend

El frontend usa Vite con hot-reload. Los cambios se reflejan automáticamente en el navegador.

```powershell
# Ver logs del frontend
docker-compose logs -f frontend

# Reiniciar el frontend
docker-compose restart frontend
```

### Base de Datos

Para ver o modificar datos:

```powershell
# Acceder a la consola de PostgreSQL
docker-compose exec db psql -U postgres -d flaskdb

# Backup de la base de datos
docker-compose exec db pg_dump -U postgres flaskdb > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U postgres -d flaskdb < backup.sql
```

## 🌐 Variables de Entorno

### Backend (.env)

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/flaskdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=flaskdb
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend (variables en docker-compose.yml)

```env
NUXT_PUBLIC_API_URL=http://backend:8000           # Para SSR (server-side)
NUXT_PUBLIC_API_URL_CLIENT=http://localhost:8000  # Para cliente (browser)
```

## 🐛 Troubleshooting

### El frontend no puede conectarse al backend

1. Verifica que ambos servicios estén corriendo:
   ```powershell
   docker-compose ps
   ```

2. Verifica las variables de entorno:
   ```powershell
   docker-compose config
   ```

3. Revisa los logs:
   ```powershell
   docker-compose logs frontend backend
   ```

### Error de conexión a la base de datos

1. Verifica que el servicio de DB esté saludable:
   ```powershell
   docker-compose ps db
   ```

2. Espera a que el healthcheck pase (puede tomar 10-30 segundos)

3. Verifica las credenciales en el archivo `.env`

### Cambios no se reflejan

1. Para el backend/frontend, los volúmenes están montados y deberían reflejarse automáticamente

2. Si los cambios no aparecen, intenta reconstruir:
   ```powershell
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

### Puertos ocupados

Si obtienes errores de puertos ya en uso:

```powershell
# Ver qué está usando el puerto
netstat -ano | findstr :3000
netstat -ano | findstr :8000
netstat -ano | findstr :5432

# Detener el proceso o cambiar los puertos en docker-compose.yml
```

## 📚 Documentación Adicional

- [Frontend README](./frontend/README.md)
- [Backend API Reference](./backend/docs/API_REFERENCE.md)
- [Backend Architecture](./backend/docs/ARCHITECTURE.md)

## 🚢 Despliegue en Producción

Para producción, usa el archivo `docker-compose.prod.yml`:

```powershell
# Construir imágenes optimizadas
docker-compose -f docker-compose.prod.yml build

# Levantar servicios en modo producción
docker-compose -f docker-compose.prod.yml up -d
```

**Diferencias en producción:**
- Frontend: Build estático optimizado (no hot-reload)
- Backend: Configuración de producción
- Sin montaje de volúmenes de código
- Restart policy: always

## 📝 Notas

- El primer inicio puede tomar varios minutos mientras se descargan las imágenes y se construyen los contenedores
- Los datos de la base de datos persisten en un volumen Docker llamado `pgdata`
- Para desarrollo, los cambios en el código se reflejan automáticamente sin necesidad de reconstruir
