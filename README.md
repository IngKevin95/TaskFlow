# 🚀 TaskFlow - Gestión Colaborativa de Tareas

**Sistema fullstack completo para la gestión de tareas en equipo con autenticación JWT, control de roles (RBAC) y documentación interactiva en Swagger.**

**Versión:** 1.0.0  
**Estado:** En producción ✅

---

## 📋 Contenido

1. [Características Generales](#características-generales)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Instalación Rápida](#instalación-rápida)
5. [Documentación](#documentación)
6. [Despliegue](#despliegue)

---

## ✨ Características Generales

### 🎯 Backend (FastAPI)
- ✅ API RESTful con autenticación JWT
- ✅ Sistema RBAC con 3 niveles de roles (ADMIN, READ_WRITE, READ_ONLY)
- ✅ Gestión completa de usuarios, proyectos y tareas
- ✅ Filtrado y búsqueda avanzada de tareas (5+ filtros combinables)
- ✅ Swagger UI personalizado con validación automática de tokens
- ✅ Documentación interactiva en ReDoc
- ✅ Base de datos PostgreSQL con ORM SQLAlchemy

### 🎨 Frontend (React + TypeScript)
- ✅ Interfaz moderna con Tailwind CSS
- ✅ Componentes reutilizables y tipados
- ✅ Context API para gestión de estado
- ✅ Integración con API backend
- ✅ Sistema de autenticación con JWT
- ✅ Formularios validados y responsivos
- ✅ Tests unitarios con Jest y React Testing Library

---

## 📁 Estructura del Proyecto

```
TaskFlow/
├── backend/                          # 🔧 API Backend (FastAPI + PostgreSQL)
│   ├── app/
│   │   ├── api/
│   │   │   ├── routers/             # Endpoints de cada módulo
│   │   │   ├── dependencies.py      # Inyección de dependencias
│   │   │   └── dependencies_rbac.py # RBAC personalizado
│   │   ├── core/                    # Configuración y utilidades
│   │   ├── database/                # Conexión y sesión
│   │   ├── models/                  # Modelos SQLAlchemy
│   │   ├── schemas/                 # Esquemas Pydantic
│   │   ├── services/                # Lógica de negocio
│   │   ├── static/                  # Archivos estáticos (JS, CSS personalizado)
│   │   └── main.py                  # Punto de entrada
│   ├── tests/                       # Tests unitarios e integración
│   ├── docker-compose.yml           # Orquestación de servicios
│   ├── Dockerfile                   # Imagen Docker del backend
│   ├── requirements.txt             # Dependencias Python
│   ├── .env.example                 # Variables de entorno (ejemplo)
│   └── README.md                    # 📖 Documentación detallada del backend
│
├── frontend/                         # 🎨 UI Frontend (React + TypeScript)
│   ├── src/
│   │   ├── api/                     # Servicios HTTP
│   │   ├── components/              # Componentes React
│   │   ├── context/                 # Context API (autenticación)
│   │   ├── hooks/                   # Custom hooks
│   │   ├── pages/                   # Páginas principales
│   │   ├── router/                  # Rutas de la aplicación
│   │   ├── store/                   # Gestión de estado
│   │   ├── styles/                  # Estilos CSS
│   │   ├── types/                   # Tipos TypeScript
│   │   ├── utils/                   # Funciones utilitarias
│   │   └── main.tsx                 # Punto de entrada
│   ├── tests/                       # Tests con Jest y React Testing Library
│   ├── public/                      # Activos estáticos
│   ├── vite.config.ts              # Configuración Vite
│   ├── jest.config.js              # Configuración Jest
│   ├── tailwind.config.js          # Configuración Tailwind CSS
│   ├── package.json                # Dependencias npm
│   └── README.md                   # 📖 Documentación del frontend
│
├── .gitignore                       # Archivos a ignorar en Git
├── README.md                        # Este archivo (documentación general)
└── API_REQUESTS.rest                # Colección REST con 50+ ejemplos
```

---

## 🛠️ Stack Tecnológico

### Backend
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Python** | 3.11+ | Lenguaje principal |
| **FastAPI** | 0.104+ | Framework web asincrónico |
| **PostgreSQL** | 12+ | Base de datos relacional |
| **SQLAlchemy** | 2.0+ | ORM para BD |
| **Pydantic** | 2.5+ | Validación de datos |
| **JWT (python-jose)** | 3.3+ | Autenticación de tokens |
| **Docker** | Latest | Containerización |

### Frontend
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **React** | 18+ | Biblioteca de UI |
| **TypeScript** | 5+ | Tipado estático |
| **Vite** | Latest | Build tool y dev server |
| **Tailwind CSS** | 3+ | Estilos utilitarios |
| **Context API** | Native | Gestión de estado |
| **Axios** | Latest | HTTP client |
| **Jest** | Latest | Testing framework |

---

## 🚀 Instalación Rápida

### Opción 1: Docker Compose (Recomendado) ⭐

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd TaskFlow

# 2. Iniciar servicios (backend + frontend + BD)
docker-compose up -d

# 3. Esperar a que se inicialice la BD (~10 segundos)
sleep 10

# 4. Acceder a los servicios
# Backend Swagger: http://localhost:8000/docs
# Frontend App: http://localhost:5173
# ReDoc: http://localhost:8000/redoc
```

### Opción 2: Desarrollo Local

#### Backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Acceder a http://localhost:5173
```

---

## 📚 Documentación

### Backend
La documentación completa del backend está en **`backend/README.md`** con:
- 🔐 Sistema RBAC detallado (matriz de permisos)
- 📡 Endpoints disponibles (50+ ejemplos)
- 🔍 Filtros y búsqueda avanzada
- 🗄️ Modelos de base de datos (ER diagram)
- 🧪 Guía completa de testing
- 🚀 Despliegue en producción

### Frontend
La documentación completa del frontend está en **`frontend/README.md`** con:
- 🎨 Estructura de componentes
- 🧩 Componentes disponibles
- 🪝 Custom hooks
- 🏠 Pages/Rutas
- �� Testing con Jest
- 📦 Build y despliegue

### Documentación Interactiva

**Swagger UI (API):** http://localhost:8000/docs
- Interfaz interactiva para probar todos los endpoints
- Validación automática de tokens JWT
- Ejemplos de requests y responses

**ReDoc:** http://localhost:8000/redoc
- Documentación legible de la API
- Esquemas y modelos detallados

---

## 🔐 Autenticación y Roles

El sistema implementa **3 roles con permisos granulares**:

| Rol | Permisos | Uso |
|-----|----------|-----|
| **ADMIN** | Acceso total al sistema | Administradores |
| **READ_WRITE** | Crear y editar recursos propios | Colaboradores activos |
| **READ_ONLY** | Solo lectura | Observadores/Stakeholders |

**Credenciales de Prueba:**
```
Usuario: admin
Contraseña: AdminTaskFlow@2025!
```

---

## 🧪 Testing

### Backend
```bash
cd backend

# Ejecutar todos los tests
pytest tests/ -v

# Con coverage
pytest tests/ --cov=app
```

### Frontend
```bash
cd frontend

# Ejecutar todos los tests
npm test

# Con coverage
npm test -- --coverage
```

---

## 🐳 Docker

### Build Manual
```bash
# Backend
cd backend
docker build -t taskflow-backend:1.0.0 .

# Frontend
cd frontend
docker build -t taskflow-frontend:1.0.0 .
```

### Gestionar Servicios
```bash
# Ver estado
docker ps

# Ver logs
docker logs taskflow_backend
docker logs taskflow_frontend

# Reiniciar servicio
docker restart taskflow_backend
docker restart taskflow_frontend

# Detener todo
docker-compose down

# Eliminar volúmenes
docker-compose down -v
```

---

## 🚀 Despliegue

### Producción

#### Backend
1. Cambiar `SECRET_KEY` en `.env`
2. Cambiar `DEBUG=False`
3. Usar Gunicorn como ASGI server
4. Configurar Nginx como reverse proxy
5. Usar HTTPS (SSL/TLS)

#### Frontend
1. Build optimizado: `npm run build`
2. Servir con servidor estático
3. Configurar headers de cache
4. Usar CDN para assets

Ver documentación específica en `backend/README.md` y `frontend/README.md`

---

## 📡 API Endpoints Principales

### Autenticación
```http
POST   /api/auth/login         # Obtener token JWT
GET    /api/auth/me            # Datos del usuario autenticado
GET    /api/auth/validate-token # Validar token (para Swagger UI)
```

### Usuarios
```http
GET    /api/users              # Listar usuarios
POST   /api/users              # Crear usuario
GET    /api/users/{id}         # Obtener usuario
PATCH  /api/users/{id}         # Actualizar usuario
```

### Proyectos
```http
GET    /api/projects           # Listar proyectos
POST   /api/projects           # Crear proyecto
GET    /api/projects/{id}      # Obtener proyecto
PATCH  /api/projects/{id}      # Actualizar proyecto
DELETE /api/projects/{id}      # Eliminar proyecto
```

### Tareas
```http
GET    /api/tasks/project/{id} # Listar tareas del proyecto
GET    /api/tasks/my-tasks     # Mis tareas asignadas
POST   /api/tasks              # Crear tarea
GET    /api/tasks/{id}         # Obtener tarea
PATCH  /api/tasks/{id}         # Actualizar tarea
DELETE /api/tasks/{id}         # Eliminar tarea
```

---

## 🔧 Configuración

### Variables de Entorno (Backend)

```bash
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/taskflow_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

# Aplicación
APP_NAME=TaskFlow API
DEBUG=True
API_PORT=8000

# Admin inicial
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=AdminTaskFlow@2025!
```

### Variables de Entorno (Frontend)

```bash
# API Backend
VITE_API_BASE_URL=http://localhost:8000

# Aplicación
VITE_APP_NAME=TaskFlow
VITE_APP_VERSION=1.0.0
```

---

## 🐛 Troubleshooting

### Backend no inicia
```bash
# Ver logs
docker logs taskflow_backend

# Reiniciar servicios
docker-compose restart

# Verificar puerto
lsof -i :8000
```

### BD no conecta
```bash
# Reiniciar BD
docker-compose down -v
docker-compose up -d
```

### Frontend no carga
```bash
# Limpiar caché npm
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 📈 Roadmap Futuro

- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Comentarios en tareas
- [ ] Historial de cambios (audit log)
- [ ] Subida de archivos
- [ ] Reportes y análiticas
- [ ] Integración con calendarios
- [ ] Mobile app (React Native)

---

## �� Contribuir

1. Fork el repositorio
2. Crear rama: `git checkout -b feature/NewFeature`
3. Commit: `git commit -m 'feat: add NewFeature'`
4. Push: `git push origin feature/NewFeature`
5. Pull Request

---

## 📄 Licencia

MIT License - Ver LICENSE file

---

## 📞 Soporte

**Documentación:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`

**Reportar Issues:**
- GitHub Issues
- Pull Requests son bienvenidos

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0.0 ✅
