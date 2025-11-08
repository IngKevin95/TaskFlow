# 🚀 TaskFlow Backend API

API RESTful completa para la gestión colaborativa de tareas con control de acceso basado en roles (RBAC), autenticación JWT y validación integrada usando FastAPI y PostgreSQL.

**Versión:** 1.0.0  
**Estado:** En producción ✅

---

## 📋 Contenido

1. [Características](#características)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación Rápida](#instalación-rápida)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Sistema de Roles RBAC](#sistema-de-roles-rbac)
6. [Endpoints Disponibles](#endpoints-disponibles)
7. [Guía de Testing](#guía-de-testing)
8. [Modelos de Base de Datos](#modelos-de-base-de-datos)
9. [Filtros y Búsqueda](#filtros-y-búsqueda)
10. [Desarrollo](#desarrollo)
11. [Despliegue](#despliegue)

---

## ✨ Características

### 🔐 Autenticación y Seguridad
- ✅ Autenticación JWT (JSON Web Tokens) con expiración configurable
- ✅ Hashing de contraseñas con bcrypt
- ✅ Tokens de larga duración (24 horas por defecto)
- ✅ Validación de email y contraseña robusta
- ✅ Protección contra ataques comunes

### 👥 Control de Acceso Basado en Roles (RBAC)
- ✅ 3 niveles de roles: ADMIN, READ_WRITE, READ_ONLY
- ✅ Permisos granulares por endpoint
- ✅ Validación de rol en cada operación
- ✅ Restricción de datos según rol del usuario

### 📊 Gestión de Usuarios
- ✅ Crear usuarios con asignación de rol
- ✅ Listar usuarios (filtrado por rol)
- ✅ Obtener datos de usuario específico
- ✅ Actualizar información de usuario
- ✅ Cambiar rol de usuario (solo ADMIN)
- ✅ Cambiar contraseña de usuario
- ✅ Activar/Desactivar usuarios
- ✅ Ver datos del usuario autenticado

### 🏢 Gestión de Proyectos
- ✅ Crear proyectos (ADMIN y READ_WRITE)
- ✅ Listar proyectos con paginación
- ✅ Obtener detalles de proyecto
- ✅ Actualizar información de proyecto
- ✅ Eliminar proyectos (solo propietario)
- ✅ Agregar/remover miembros del proyecto
- ✅ Validación de pertenencia del proyecto
- ✅ Control de acceso por propietario

### ✅ Gestión de Tareas (Task Management)
- ✅ Crear tareas en proyectos (ADMIN y READ_WRITE)
- ✅ Listar tareas del proyecto con **5+ filtros combinables**
- ✅ Listar tareas asignadas al usuario
- ✅ Obtener detalles de tarea específica
- ✅ Actualizar tareas (miembros del proyecto, excepto READ_ONLY)
- ✅ Eliminar tareas (solo creador/propietario)
- ✅ Cambiar estado de tarea
- ✅ Asignar/reasignar tareas
- ✅ Validación de pertenencia a proyecto

### 🔍 Filtrado y Búsqueda Avanzada
- ✅ Filtro por estado (pending, in_progress, review, completed)
- ✅ Filtro por prioridad (low, medium, high, critical)
- ✅ Filtro por usuario asignado
- ✅ Filtro por creador de tarea
- ✅ Filtro por proyecto (en tareas del usuario)
- ✅ Combinación de múltiples filtros
- ✅ Paginación (skip/limit)

---

## 📋 Requisitos Previos

- **Python** 3.11+
- **PostgreSQL** 12+
- **Docker** y **Docker Compose** (recomendado)
- **pip** o **poetry**
- **Git**

### Verificar instalación

```bash
# Python
python --version

# Docker
docker --version
docker-compose --version

# PostgreSQL (si instalas localmente)
psql --version
```

---

## 🚀 Instalación Rápida

### Opción 1: Usando Docker Compose (Recomendado) ⭐

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd ProyectoFullStack/backend

# 2. Crear archivo .env (si no existe)
cp .env.example .env

# 3. Iniciar contenedores
docker-compose up -d

# 4. Verificar que está corriendo
docker ps
docker logs taskflow_backend

# 5. Acceder a la API
# Swagger UI: http://localhost:8000/api/docs
# ReDoc: http://localhost:8000/api/redoc
# Health check: http://localhost:8000/health
```

### Opción 2: Instalación Local

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con credenciales PostgreSQL

# 4. Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. La API estará disponible en http://localhost:8000
```

---

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── api/
│   │   ├── routers/
│   │   │   ├── auth.py              # Endpoints de autenticación
│   │   │   ├── users.py             # Endpoints de usuarios
│   │   │   ├── projects.py          # Endpoints de proyectos
│   │   │   └── tasks.py             # Endpoints de tareas
│   │   └── dependencies.py          # Dependencias inyectables
│   ├── core/
│   │   ├── config.py                # Configuración de app
│   │   ├── enums.py                 # Enumeraciones (roles, prioridades, estados)
│   │   ├── exceptions.py            # Excepciones personalizadas
│   │   ├── security.py              # JWT, hashing de contraseñas
│   │   └── constants.py             # Constantes de la aplicación
│   ├── database/
│   │   ├── session.py               # Configuración de BD
│   │   └── base.py                  # Base para modelos
│   ├── models/
│   │   ├── user.py                  # Modelo User (SQLAlchemy)
│   │   ├── project.py               # Modelo Project
│   │   └── task.py                  # Modelo Task
│   ├── schemas/
│   │   ├── user.py                  # Esquemas User (Pydantic)
│   │   ├── project.py               # Esquemas Project
│   │   └── task.py                  # Esquemas Task
│   ├── services/
│   │   ├── user_service.py          # Lógica de usuarios
│   │   ├── project_service.py       # Lógica de proyectos
│   │   └── task_service.py          # Lógica de tareas
│   ├── utils/
│   │   └── responses.py             # Respuestas estándar
│   ├── main.py                      # Punto de entrada FastAPI
│   └── config.py                    # Configuración de aplicación
├── tests/                           # Tests unitarios e integración
├── API_REQUESTS.rest                # Colección de requests REST (50+ ejemplos)
├── docker-compose.yml               # Configuración Docker
├── Dockerfile                       # Imagen Docker
├── requirements.txt                 # Dependencias Python
├── .env.example                     # Ejemplo de variables de entorno
├── TESTING_ENDPOINTS.md             # Guía de testing
└── README.md                        # Este archivo
```

---

## 🔐 Sistema de Roles RBAC

La API implementa un sistema **flexible de 3 roles** con permisos granulares:

### Matriz de Permisos

| Acción | ADMIN | READ_WRITE | READ_ONLY |
|--------|-------|-----------|-----------|
| Ver usuarios | ✅ Todos | ✅ READ_WRITE+READ_ONLY | ✅ Solo READ_ONLY |
| Crear usuario | ✅ Cualquier rol | ✅ Solo READ_ONLY | ❌ |
| Cambiar rol usuario | ✅ | ❌ | ❌ |
| Cambiar contraseña usuario | ✅ | ❌ | ❌ |
| Crear proyecto | ✅ | ✅ | ❌ |
| Actualizar proyecto | ✅ | ❌ | ❌ |
| Eliminar proyecto | ✅ Propietario | ❌ | ❌ |
| Agregar miembro proyecto | ✅ Propietario | ❌ | ❌ |
| Crear tarea | ✅ | ✅ | ❌ (403) |
| Actualizar tarea | ✅ Miembro proyecto | ✅ Miembro proyecto | ❌ (403) |
| Eliminar tarea | ✅ Solo creador | ✅ Solo creador | ❌ (403) |
| Actualizar estado tarea | ✅ Miembro proyecto | ✅ Miembro proyecto | ❌ (403) |

### Definiciones de Rol

**ADMIN**
- Acceso total al sistema
- Puede crear/actualizar/eliminar cualquier recurso
- Puede cambiar roles de otros usuarios
- Puede crear usuarios con cualquier rol

**READ_WRITE**
- Puede crear proyectos y tareas
- Puede actualizar/reasignar tareas dentro de su proyecto
- Solo puede eliminar tareas que creó (es el propietario)
- Puede crear usuarios solo con rol READ_ONLY
- No puede cambiar roles de otros usuarios

**READ_ONLY**
- Solo lectura en todos los recursos
- No puede crear, actualizar o eliminar nada
- Recibe 403 Forbidden en cualquier operación de modificación
- Puede ver solo a otros READ_ONLY

---

## 📡 Endpoints Disponibles

### 🔑 Autenticación (`/api/auth`)

#### Login - Obtener Token JWT
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=AdminTaskFlow@2025!
```
**Respuesta:** `{ "access_token": "...", "token_type": "bearer" }`

#### Obtener Datos del Usuario Actual
```http
GET /api/auth/me
Authorization: Bearer {{token}}
```
**Respuesta:** Usuario autenticado con rol y datos

---

### 👥 Usuarios (`/api/users`)

#### Crear Usuario (ADMIN crea cualquier rol, READ_WRITE solo READ_ONLY)
```http
POST /api/users/
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "username": "nuevo.usuario",
  "email": "nuevo@example.com",
  "password": "Pass123!",
  "role": "read_write",
  "first_name": "Nombre",
  "last_name": "Apellido"
}
```

#### Listar Usuarios (filtrado por rol)
```http
GET /api/users/?skip=0&limit=10
Authorization: Bearer {{token}}
```

#### Obtener Usuario Específico
```http
GET /api/users/{user_id}
Authorization: Bearer {{token}}
```

#### Actualizar Usuario (cambiar rol solo ADMIN)
```http
PATCH /api/users/{user_id}
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "role": "read_write"
}
```

#### Cambiar Contraseña (solo ADMIN para otros)
```http
POST /api/users/{user_id}/change-password
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "new_password": "NuevoPass123!"
}
```

#### Activar/Desactivar Usuario
```http
POST /api/users/{user_id}/activate
Authorization: Bearer {{token}}
```

---

### 🏢 Proyectos (`/api/projects`)

#### Crear Proyecto (ADMIN, READ_WRITE)
```http
POST /api/projects
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "name": "Mi Proyecto",
  "description": "Descripción del proyecto"
}
```

#### Listar Proyectos
```http
GET /api/projects?skip=0&limit=10
Authorization: Bearer {{token}}
```

#### Obtener Proyecto Específico
```http
GET /api/projects/{project_id}
Authorization: Bearer {{token}}
```

#### Actualizar Proyecto (solo ADMIN)
```http
PATCH /api/projects/{project_id}
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "name": "Proyecto Actualizado",
  "description": "Nueva descripción"
}
```

#### Eliminar Proyecto (solo propietario)
```http
DELETE /api/projects/{project_id}
Authorization: Bearer {{token}}
```

#### Agregar Miembro al Proyecto (solo propietario)
```http
POST /api/projects/{project_id}/members?member_id={user_id}
Authorization: Bearer {{token}}
```

#### Remover Miembro del Proyecto (solo propietario)
```http
DELETE /api/projects/{project_id}/members/{user_id}
Authorization: Bearer {{token}}
```

---

### ✅ Tareas (`/api/tasks`)

#### Crear Tarea (ADMIN, READ_WRITE en su proyecto)
```http
POST /api/tasks
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "title": "Mi Tarea",
  "description": "Descripción de la tarea",
  "priority": "high",
  "project_id": 1,
  "assigned_to_id": 2
}
```
**Nota:** El `status` se establece automáticamente como `pending` en creación.

#### Listar Tareas del Proyecto (con filtros)
```http
GET /api/tasks/project/{project_id}
Authorization: Bearer {{token}}

# Con filtros opcionales (ver sección de Filtros)
GET /api/tasks/project/1?status_filter=pending&priority_filter=high
GET /api/tasks/project/1?assigned_to_id=2
GET /api/tasks/project/1?creator_id=1&priority_filter=critical
```

#### Listar Mis Tareas Asignadas (con filtros)
```http
GET /api/tasks/my-tasks
Authorization: Bearer {{token}}

# Con filtros
GET /api/tasks/my-tasks?status_filter=in_progress
GET /api/tasks/my-tasks?project_id=1&priority_filter=high
```

#### Obtener Tarea Específica
```http
GET /api/tasks/{task_id}
Authorization: Bearer {{token}}
```

#### Actualizar Tarea (miembros del proyecto, excepto READ_ONLY)
```http
PATCH /api/tasks/{task_id}
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "title": "Tarea Actualizada",
  "status": "in_progress",
  "priority": "critical",
  "assigned_to_id": 3
}
```

#### Cambiar Estado de Tarea
```http
PATCH /api/tasks/{task_id}/status
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "status": "completed"
}
```
**Estados disponibles:** `pending`, `in_progress`, `review`, `completed`

#### Eliminar Tarea (solo creador/propietario)
```http
DELETE /api/tasks/{task_id}
Authorization: Bearer {{token}}
```
**Nota:** Solo el creador puede eliminar, incluso si es ADMIN.

---

## 🔍 Filtros y Búsqueda

### Filtros de Tareas del Proyecto

**Endpoint:** `GET /api/tasks/project/{project_id}`

| Filtro | Valores | Tipo | Descripción |
|--------|--------|------|-------------|
| `status_filter` | pending, in_progress, review, completed | Query | Filtrar por estado |
| `priority_filter` | low, medium, high, critical | Query | Filtrar por prioridad |
| `assigned_to_id` | {user_id} | Query | Filtrar por usuario asignado |
| `creator_id` | {user_id} | Query | Filtrar por creador |
| `skip` | Número (default: 0) | Query | Paginación: saltar N registros |
| `limit` | Número (default: 50, máx: 200) | Query | Paginación: máximo de registros |

#### Ejemplos de Uso

```http
# Solo tareas pendientes
GET /api/tasks/project/1?status_filter=pending

# Solo tareas de alta prioridad en progreso
GET /api/tasks/project/1?priority_filter=high&status_filter=in_progress

# Tareas asignadas a usuario específico
GET /api/tasks/project/1?assigned_to_id=2

# Tareas creadas por usuario específico con prioridad crítica
GET /api/tasks/project/1?creator_id=1&priority_filter=critical

# Combinación de múltiples filtros con paginación
GET /api/tasks/project/1?status_filter=pending&priority_filter=high&assigned_to_id=2&skip=0&limit=25
```

### Filtros de Mis Tareas

**Endpoint:** `GET /api/tasks/my-tasks`

| Filtro | Valores | Tipo | Descripción |
|--------|--------|------|-------------|
| `status_filter` | pending, in_progress, review, completed | Query | Filtrar por estado |
| `priority_filter` | low, medium, high, critical | Query | Filtrar por prioridad |
| `project_id` | {project_id} | Query | Filtrar por proyecto |
| `skip` | Número (default: 0) | Query | Paginación: saltar N registros |
| `limit` | Número (default: 50, máx: 200) | Query | Paginación: máximo de registros |

#### Ejemplos de Uso

```http
# Mis tareas pendientes
GET /api/tasks/my-tasks?status_filter=pending

# Mis tareas de alta prioridad en un proyecto específico
GET /api/tasks/my-tasks?project_id=1&priority_filter=high

# Todas mis tareas en progreso
GET /api/tasks/my-tasks?status_filter=in_progress
```

---

## 🧪 Guía de Testing

### Archivo de Colección REST

Se incluye **`API_REQUESTS.rest`** con **50+ ejemplos de requests** completamente documentados, incluyendo:

- ✅ Requests de autenticación
- ✅ Requests de usuarios (crear, listar, actualizar, eliminar)
- ✅ Requests de proyectos (crear, agregar miembros, etc.)
- ✅ Requests de tareas (CRUD completo con filtros)
- ✅ Flujos de testing integrados (FLUJO 1, 2, 3)
- ✅ Pruebas de seguridad y permisos
- ✅ Ejemplos de cada rol (ADMIN, READ_WRITE, READ_ONLY)

### Usar API_REQUESTS.rest

#### Con VS Code (Extensión REST Client)

1. **Instalar extensión:**
   - Ir a Extensions (Ctrl+Shift+X)
   - Buscar "REST Client" de Huachao Mao
   - Instalar

2. **Obtener Token JWT:**
   - Abrir `API_REQUESTS.rest`
   - Ir a la sección `1.1 Login - Obtener Token ADMIN`
   - Hacer click en "Send Request" (o Ctrl+Alt+R)
   - Copiar el valor de `access_token`

3. **Configurar Variable de Token:**
   - En VS Code: Ctrl+H (Find and Replace)
   - Find: `{{token}}`
   - Replace with: `eyJhbGc...` (el token copiado)
   - Replace All

4. **Ejecutar Requests:**
   - Cada línea con `###` define un nuevo request
   - Hacer click en "Send Request" para ejecutar
   - Ver respuesta en el panel derecho

#### Con Postman

1. **Importar colección:**
   ```bash
   # Se incluye: TaskFlow_API_Postman.json
   ```
   - Abrir Postman
   - Click en Import
   - Seleccionar el archivo JSON

2. **Configurar variables:**
   - Crear Environment
   - Agregar variables: `token`, `token_read_write`, `token_read_only`
   - Usar `{{variable}}` en los requests

#### Con cURL

```bash
# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=AdminTaskFlow@2025!"

# Usar token
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -X GET "http://localhost:8000/api/users" \
  -H "Authorization: Bearer $TOKEN"
```

### Credenciales de Prueba

```
┌─────────────────┬──────────────────────────────┬─────────────┐
│ Usuario         │ Contraseña                   │ Rol         │
├─────────────────┼──────────────────────────────┼─────────────┤
│ admin           │ AdminTaskFlow@2025!          │ ADMIN       │
│ mike.developer  │ 123456789                    │ READ_WRITE  │
│ laura.viewer    │ 123456789                    │ READ_ONLY   │
└─────────────────┴──────────────────────────────┴─────────────┘
```

### Flujos de Testing Incluidos

**FLUJO 1:** Setup Inicial
- Crear usuario READ_WRITE
- Crear usuario READ_ONLY
- Verificar creación

**FLUJO 2:** Crear Proyecto y Tareas
- Crear proyecto
- Crear 2 tareas con diferentes prioridades
- Listar tareas del proyecto

**FLUJO 3:** Probar Restricciones de Roles
- Login como READ_WRITE
- Listar usuarios
- Intentar crear admin (debe fallar)
- Crear usuario READ_ONLY (debe funcionar)

### Ejecutar Tests Automatizados

```bash
# Todos los tests
pytest tests/ -v

# Solo tests unitarios
pytest tests/unit -v

# Solo tests de integración
pytest tests/integration -v

# Con coverage
pytest tests/ --cov=app --cov-report=html

# Ver reporte de coverage
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

---

## 🗄️ Modelos de Base de Datos

### User (Usuarios)

```python
- id: INT, PRIMARY KEY, AUTO INCREMENT
- username: VARCHAR(255), UNIQUE, NOT NULL
- email: VARCHAR(255), UNIQUE, NOT NULL
- password_hash: VARCHAR(255), NOT NULL
- first_name: VARCHAR(255), NOT NULL
- last_name: VARCHAR(255), NOT NULL
- role: ENUM('admin', 'read_write', 'read_only'), NOT NULL
- is_active: BOOLEAN, DEFAULT TRUE
- created_at: TIMESTAMP, DEFAULT NOW()
- updated_at: TIMESTAMP, DEFAULT NOW(), ON UPDATE NOW()

Relaciones:
- projects_owner (One-to-Many): Proyectos que el usuario propietario
- created_tasks (One-to-Many): Tareas que el usuario creó
- assigned_tasks (One-to-Many): Tareas asignadas al usuario
- project_members (Many-to-Many): Proyectos donde es miembro
```

### Project (Proyectos)

```python
- id: INT, PRIMARY KEY, AUTO INCREMENT
- name: VARCHAR(255), NOT NULL
- description: TEXT
- owner_id: INT, FOREIGN KEY (User.id), NOT NULL
- created_at: TIMESTAMP, DEFAULT NOW()
- updated_at: TIMESTAMP, DEFAULT NOW(), ON UPDATE NOW()

Relaciones:
- owner (Many-to-One): Usuario propietario
- tasks (One-to-Many): Tareas del proyecto
- members (Many-to-Many): Usuarios miembros del proyecto
```

### ProjectMember (Tabla de Unión)

```python
- project_id: INT, FOREIGN KEY (Project.id), PRIMARY KEY
- user_id: INT, FOREIGN KEY (User.id), PRIMARY KEY
- added_at: TIMESTAMP, DEFAULT NOW()
```

### Task (Tareas)

```python
- id: INT, PRIMARY KEY, AUTO INCREMENT
- title: VARCHAR(255), NOT NULL
- description: TEXT
- project_id: INT, FOREIGN KEY (Project.id), NOT NULL
- creator_id: INT, FOREIGN KEY (User.id), NOT NULL
- assigned_to_id: INT, FOREIGN KEY (User.id), NULLABLE
- priority: ENUM('low', 'medium', 'high', 'critical'), NOT NULL
- status: ENUM('pending', 'in_progress', 'review', 'completed'), NOT NULL
- due_date: DATE, NULLABLE
- created_at: TIMESTAMP, DEFAULT NOW()
- updated_at: TIMESTAMP, DEFAULT NOW(), ON UPDATE NOW()

Relaciones:
- project (Many-to-One): Proyecto contenedor
- creator (Many-to-One): Usuario que creó la tarea
- assigned_to_user (Many-to-One): Usuario asignado a la tarea
```

### Diagrama ER

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ username (UQ)   │
│ email (UQ)      │
│ password_hash   │
│ first_name      │
│ last_name       │
│ role            │
│ is_active       │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:N (owner_id)
         │
    ┌────▼──────────────┐
    │    Project        │
    ├───────────────────┤
    │ id (PK)           │
    │ name              │
    │ description       │
    │ owner_id (FK)     │
    │ created_at        │
    │ updated_at        │
    └────┬──────────────┘
         │
    ┌────▼──────────────────────┐
    │  ProjectMember (N:M)      │
    ├───────────────────────────┤
    │ project_id (FK, PK)       │
    │ user_id (FK, PK)          │
    │ added_at                  │
    └───────────────────────────┘
         │
    ┌────▼──────────────┐
    │      Task         │
    ├───────────────────┤
    │ id (PK)           │
    │ title             │
    │ description       │
    │ project_id (FK)   │
    │ creator_id (FK)   │
    │ assigned_to_id    │
    │ priority          │
    │ status            │
    │ due_date          │
    │ created_at        │
    │ updated_at        │
    └───────────────────┘
```

---

## 🔧 Desarrollo

### Variables de Entorno (.env)

```bash
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/taskflow_db

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

# Aplicación
APP_NAME=TaskFlow API
DEBUG=True
```

### Inicializar Base de Datos

```python
# Dentro de la app
from app.database.session import create_tables
create_tables()  # Crea todas las tablas
```

### Script de Seed Inicial

```bash
# Crear usuario admin inicial y datos de prueba
python scripts/seed_database.py
```

### Estructura de Servicios

Cada módulo (usuarios, proyectos, tareas) sigue la arquitectura de capas:

```
Router (API) 
    ↓
Service (Lógica de negocio)
    ↓
Repository (Acceso a datos)
    ↓
Database (SQLAlchemy ORM)
```

---

## 🚀 Despliegue

### Producción con Docker

```bash
# Build imagen
docker build -t taskflow-api:1.0.0 .

# Run contenedor
docker run -d \
  --name taskflow \
  -p 8000:8000 \
  --env-file .env \
  --network backend-network \
  taskflow-api:1.0.0
```

### Usando Docker Compose (Producción)

```bash
# Actualizar imagen
docker pull taskflow-api:latest

# Reiniciar servicios
docker-compose up -d --force-recreate

# Ver logs
docker-compose logs -f taskflow_backend
```

### Configuración de Producción

```bash
# 1. Cambiar SECRET_KEY en .env
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')

# 2. Cambiar DEBUG a False
DEBUG=False

# 3. Usar Gunicorn en lugar de Uvicorn
pip install gunicorn

# 4. Ejecutar
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

### Configuración de Nginx (Reverse Proxy)

```nginx
upstream taskflow_api {
    server backend:8000;
}

server {
    listen 80;
    server_name api.taskflow.com;

    location / {
        proxy_pass http://taskflow_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📚 Documentación Adicional

- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc
- **TESTING_ENDPOINTS.md:** Guía detallada de testing
- **EJEMPLOS_API_RBAC.md:** Ejemplos completos de RBAC
- **GUIA_SWAGGER_RBAC.md:** Documentación de Swagger

---

## 📦 Dependencias Principales

```
FastAPI==0.104.1          # Framework web moderno asincrónico
Uvicorn==0.24.0           # ASGI server
SQLAlchemy==2.0.23        # ORM para base de datos
Pydantic==2.5.0           # Validación de datos con type hints
python-jose==3.3.0        # JWT tokens
passlib==1.7.4            # Password hashing
bcrypt==4.1.1             # Algoritmo de hashing seguro
psycopg2-binary==2.9.9    # Driver PostgreSQL
python-multipart==0.0.6   # Parsing de form data
pytest==7.4.3             # Testing framework
pytest-cov==4.1.0         # Coverage para pytest
httpx==0.25.2             # HTTP client para tests
```

Ver `requirements.txt` para versiones exactas.

---

## 🧪 Ejecución Rápida

### Checklist de Inicio

```bash
# 1. Clonar y entrar
git clone <repo> && cd ProyectoFullStack/backend

# 2. Iniciar con Docker
docker-compose up -d

# 3. Esperar ~10 segundos por inicialización de BD
sleep 10

# 4. Verificar que está corriendo
curl http://localhost:8000/health

# 5. Obtener token admin
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=AdminTaskFlow@2025!"

# 6. Acceder a Swagger
# Abrir: http://localhost:8000/api/docs
```

### Troubleshooting

**Puerto 8000 ya está en uso:**
```bash
docker-compose down
lsof -i :8000  # Identificar proceso
kill -9 <PID>
docker-compose up -d
```

**Errores de conexión BD:**
```bash
# Ver logs
docker logs taskflow_postgres

# Reiniciar BD
docker-compose down
docker volume rm taskflow_postgres_data
docker-compose up -d
```

**Migraciones fallidas:**
```bash
# Entrar al contenedor
docker exec -it taskflow_backend bash

# Ejecutar script de inicialización
python scripts/init_db.py
```

---

## 📝 Convenciones de Código

- **Variables y funciones:** `snake_case`
- **Clases y modelos:** `PascalCase`
- **Constantes:** `UPPER_SNAKE_CASE`
- **Archivos:** `snake_case.py`
- **Docstrings:** Google style format
- **Máximo 100 caracteres por línea**

---

## 🤝 Contribuir

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

**Documentación API completa:**
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

**Reportar Issues:**
- GitHub Issues
- Email: support@taskflow.com

**Última actualización:** Noviembre 2025
**Versión:** 1.0.0 ✅
