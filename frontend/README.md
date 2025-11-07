# Frontend - Nuxt 3 Application

Aplicación frontend construida con Nuxt 3, Vuetify y TypeScript.

## 🚀 Inicio Rápido con Docker (Recomendado)

La forma más fácil de ejecutar el frontend junto con el backend y la base de datos:

```bash
# Desde la raíz del proyecto
cd ..
docker-compose up -d
```

El frontend estará disponible en http://localhost:3000

Ver más en [README principal](../README.md)

## 📋 Desarrollo Local (sin Docker)

### Pre-requisitos

- Node.js 20+
- pnpm (recomendado)

### Instalación

```bash
# Instalar dependencias
pnpm install
```

### Variables de Entorno

Crea un archivo `.env` en la raíz del frontend:

```bash
NUXT_PUBLIC_API_URL=http://localhost:8000
```

### Servidor de Desarrollo

Inicia el servidor de desarrollo en `http://localhost:3000`:

```bash
pnpm dev
```

## 🏗️ Build de Producción

```bash
# Build para producción
pnpm build

# Preview del build
pnpm preview
```

## 🐳 Docker

### Build de la imagen

```bash
# Desarrollo (con hot-reload)
docker build -f Dockerfile.dev -t proyecto2-frontend:dev .

# Producción (optimizado)
docker build -t proyecto2-frontend:prod .
```

### Ejecutar contenedor

```bash
# Desarrollo
docker run -p 3000:3000 -v ${PWD}:/app proyecto2-frontend:dev

# Producción
docker run -p 3000:3000 proyecto2-frontend:prod
```

## 🛠️ Tecnologías

- **Framework**: Nuxt 3
- **UI Library**: Vuetify 3
- **State Management**: Pinia
- **Styling**: SCSS
- **Type Checking**: TypeScript

## 📁 Estructura

```
app/
├── assets/          # Recursos estáticos (CSS, imágenes)
├── components/      # Componentes Vue
│   ├── app/        # Componentes específicos de la app
│   ├── base/       # Componentes base reutilizables
│   └── v/          # Wrappers de Vuetify
├── composables/     # Composables de Vue
├── configs/         # Configuraciones (theme, etc)
├── layouts/         # Layouts de la aplicación
├── pages/          # Páginas (rutas automáticas)
├── plugins/        # Plugins de Nuxt
├── stores/         # Stores de Pinia
└── types/          # Definiciones TypeScript
```

## 🔧 Configuración

### API URL

El frontend se conecta al backend usando la variable de entorno `NUXT_PUBLIC_API_URL`.

- **Desarrollo local**: `http://localhost:8000`
- **Docker (SSR)**: `http://backend:8000`
- **Docker (Cliente)**: `http://localhost:8000`

### Theme

Configura el tema en `app/configs/theme.ts`

## 📚 Documentación

- [Nuxt 3 Docs](https://nuxt.com/docs/getting-started/introduction)
- [Vuetify 3 Docs](https://vuetifyjs.com/)
- [Pinia Docs](https://pinia.vuejs.org/)

## 🐛 Troubleshooting

### Puerto 3000 ocupado

```bash
# Windows
netstat -ano | findstr :3000

# Cambiar puerto
pnpm dev -- --port 3001
```

### Errores de TypeScript

```bash
# Regenerar tipos
pnpm nuxt prepare
```

### Módulos no encontrados

```bash
# Limpiar e reinstalar
rm -rf node_modules .nuxt
pnpm install
```

