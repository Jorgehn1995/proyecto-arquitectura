# 🚀 Inicio Rápido - Flask API

## ⚡ Comandos Rápidos

### 1. Iniciar el Proyecto (Primera vez)
```bash
docker-compose up --build
```

### 2. Iniciar el Proyecto (después)
```bash
docker-compose up
```

### 3. Detener el Proyecto
```bash
docker-compose down
```

### 4. Ver la Documentación
Abre tu navegador en: **http://localhost:8000/docs**

### 5. Probar la API
```bash
# Windows PowerShell
.\test_api.ps1

# Linux/Mac
bash test_api.sh
```

### 6. Ver Logs
```bash
# Ver logs de la API
docker-compose logs -f web

# Ver logs de la BD
docker-compose logs -f db
```

### 7. Resetear Base de Datos
```bash
docker-compose down -v
docker-compose up --build
```

## 📍 URLs Importantes

- **API Base:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🧪 Pruebas Rápidas

### Listar usuarios
```bash
curl http://localhost:8000/users
```

### Verificar un tag RFID
```bash
curl http://localhost:8000/tags/ABC123/check
```

### Crear un usuario
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "rfid_tag": "TEST123"
  }'
```

## 🛠️ Troubleshooting

### El puerto 8000 está en uso
```bash
# Detener el contenedor
docker-compose down

# Cambiar el puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usar 8001 en lugar de 8000
```

### Resetear todo (incluida la base de datos)
```bash
docker-compose down -v
docker-compose up --build
```

### Ver base de datos directamente
```bash
docker-compose exec db psql -U postgres -d flaskdb
```

## 📚 Para más información
Ver el archivo **README.md** completo.
