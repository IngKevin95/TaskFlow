# 🔧 TaskFlow Backend API

API RESTful completa para la gestión colaborativa de tareas con control de acceso basado en roles (RBAC), autenticación JWT y Swagger UI personalizado con validación automática de tokens.

**Versión:** 1.0.0  
**Estado:** En producción ✅

---

## 📋 Contenido

1. [Características](#características)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación Rápida](#instalación-rápida)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Sistema de Roles RBAC](#sistema-de-roles-rbac)
6. [Swagger UI Personalizado](#swagger-ui-personalizado)
7. [Endpoints Disponibles](#endpoints-disponibles)
8. [Guía de Testing](#guía-de-testing)
9. [Modelos de Base de Datos](#modelos-de-base-de-datos)
10. [Filtros y Búsqueda](#filtros-y-búsqueda)
11. [Desarrollo](#desarrollo)
12. [Despliegue](#despliegue)

---

## ✨ Características

### 🔐 Autenticación y Seguridad
- ✅ Autenticación JWT (JSON Web Tokens) con expiración configurable
- ✅ Hashing de contraseñas con bcrypt
- ✅ Tokens de larga duración (24 horas por defecto)
- ✅ Validación de email y contraseña robusta
- ✅ Protección contra ataques comunes
- ✅ HTTPBearer security scheme integrado con Swagger

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

### 🎨 Swagger UI Personalizado (NEW!)
- ✅ Interfaz mejorada con validación automática de tokens JWT
- ✅ Banner informativo con estado de autenticación en tiempo real
- ✅ Notificaciones visuales (success/error/info) para feedback del usuario
- ✅ Indicador de usuario autenticado con rol
- ✅ Limpieza automática de campos de formulario (remover valores "string" por defecto)
- ✅ Enmascaramiento del campo password en login
- ✅ Detección automática de token en botón Authorize
- ✅ Endpoint dedicado `/api/auth/validate-token` para validación de tokens
- ✅ Inyección automática de tokens a todos los endpoints protegidos

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
cd TaskFlow/backend

# 2. Crear archivo .env (si no existe)
cp .env.example .env

# 3. Iniciar contenedores
docker-compose up -d

# 4. Verificar que está corriendo
docker ps
docker logs taskflow_backend

# 5. Acceder a la API
# Swagger UI Personalizado: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
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
│   │   │   ├── tasks.py             # Endpoints de tareas
│   │   │   └── dependencies.py      # Dependencias inyectables (HTTPBearer)
│   │   ├── dependencies.py          # Dependencias compartidas
│   │   └── dependencies_rbac.py     # RBAC personalizado
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
│   │   ├── base.py                  # Clase base para modelos
│   │   ├── models.py                # Modelos principales
│   │   ├── user.py                  # Modelo User (SQLAlchemy)
│   │   ├── project.py               # Modelo Project
│   │   └── task.py                  # Modelo Task
│   ├── schemas/
│   │   ├── common.py                # Esquemas comunes
│   │   ├── user.py                  # Esquemas User (Pydantic)
│   │   ├── project.py               # Esquemas Project
│   │   └── task.py                  # Esquemas Task
│   ├── services/
│   │   ├── auth_service.py          # Lógica de autenticación
│   │   ├── user_management_service.py # Lógica de usuarios
│   │   ├── project_service.py       # Lógica de proyectos
│   │   └── task_service.py          # Lógica de tareas
│   ├── repositories/
│   │   ├── base.py                  # Clase base de repositorios
│   │   ├── user_repository.py       # Acceso a datos de usuarios
│   │   ├── project_repository.py    # Acceso a datos de proyectos
│   │   └── task_repository.py       # Acceso a datos de tareas
│   ├── static/                      # Archivos estáticos personalizados
│   │   ├── swagger-custom.js        # JavaScript para validación de tokens
│   │   ├── swagger-custom.css       # Estilos personalizados
│   │   └── (otros archivos estáticos)
│   ├── main.py                      # Punto de entrada FastAPI
│   └── config.py                    # Configuración de aplicación
├── tests/
│   ├── unit/                        # Tests unitarios
│   └── integration/                 # Tests de integración
├── docker-compose.yml               # Configuración Docker
├── Dockerfile                       # Imagen Docker
├── requirements.txt                 # Dependencias Python
├── .env.example                     # Ejemplo de variables de entorno
├── API_REQUESTS.rest                # Colección de requests REST (50+ ejemplos)
├── TESTING_ENDPOINTS.md             # Guía de testing
├── EJEMPLOS_API_RBAC.md             # Ejemplos completos de RBAC
├── GUIA_SWAGGER_RBAC.md             # Documentación de Swagger personalizado
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

## 🎨 Swagger UI Personalizado (NEW!)

### Características Principales

La API incluye un **Swagger UI completamente personalizado** con validación automática de tokens JWT:

#### 🔐 Validación Automática de Tokens
```
1. Haz clic en botón "Authorize 🔓" en Swagger UI
2. Ingresa el token JWT obtenido de /api/auth/login
3. El sistema valida automáticamente el token
4. Muestra notificación: ✅ Token válido o ❌ Token inválido
5. Actualiza estado de autenticación en banner
```

#### 🟢 Banner de Estado de Autenticación
- Muestra en tiempo real si estás autenticado
- Indica usuario actual y su rol
- Animación pulse cuando token es válido
- Color verde para autenticado, rojo para no autenticado

#### 🔔 Notificaciones Visuales
- **✅ Success:** Token válido, usuario autenticado
- **❌ Error:** Token inválido, no autorizado
- **🔄 Info:** Validando token...
- Se desaparecen automáticamente después de 5 segundos

#### 🔑 Inyección Automática de Tokens
- Token se inyecta automáticamente a todos los endpoints protegidos
- No necesitas copiar/pegar el token en cada request
- Funciona con HTTPBearer security scheme

#### 🎯 Endpoint de Validación
```http
GET /api/auth/validate-token
Authorization: Bearer {token}

Respuesta (válido):
{
  "message": "Token válido",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}

Respuesta (inválido): 401 Unauthorized
```

### Acceder a Swagger UI

```
Swagger UI Personalizado: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

### Archivos Personalizados

```
backend/app/static/
├── swagger-custom.js       # Lógica de validación de tokens
│   ├── validateToken()     # Función para validar tokens
│   ├── updateAuthStatus()  # Actualizar estado en banner
│   ├── fixLoginInputs()    # Limpiar campos del formulario
│   └── (Interceptores localStorage)
│
└── swagger-custom.css      # Estilos personalizados
    ├── .auth-info-banner   # Banner de autenticación
    ├── .status-indicator   # Indicador de estado
    ├── .token-validation-notification  # Notificaciones
    └── (Animaciones y estilos)
```

---

## 📡 Endpoints Disponibles

### 🔑 Autenticación (`/api/auth`)

#### Login - Obtener Token JWT
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=AdminTaskFlow@2025!
```
**Respuesta (200):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### Validar Token
```http
GET /api/auth/validate-token
Authorization: Bearer {token}
```
**Respuesta (200):**
```json
{
  "message": "Token válido",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

#### Obtener Datos del Usuario Actual
```http
GET /api/auth/me
Authorization: Bearer {token}
```
**Respuesta:** Usuario autenticado con rol y datos

---

### 👥 Usuarios (`/api/users`)

#### Crear Usuario
```http
POST /api/users/
Authorization: Bearer {token}
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
Authorization: Bearer {token}
```

#### Obtener Usuario Específico
```http
GET /api/users/{user_id}
Authorization: Bearer {token}
```

#### Actualizar Usuario
```http
PATCH /api/users/{user_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "role": "read_write"
}
```

#### Cambiar Contraseña
```http
POST /api/users/{user_id}/change-password
Authorization: Bearer {token}
Content-Type: application/json

{
  "new_password": "NuevoPass123!"
}
```

---

### 🏢 Proyectos (`/api/projects`)

#### Crear Proyecto
```http
POST /api/projects
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Mi Proyecto",
  "description": "Descripción del proyecto"
}
```

#### Listar Proyectos
```http
GET /api/projects?skip=0&limit=10
Authorization: Bearer {token}
```

#### Obtener Proyecto Específico
```http
GET /api/projects/{project_id}
Authorization: Bearer {token}
```

#### Actualizar Proyecto
```http
PATCH /api/projects/{project_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Proyecto Actualizado",
  "description": "Nueva descripción"
}
```

#### Eliminar Proyecto
```http
DELETE /api/projects/{project_id}
Authorization: Bearer {token}
```

---

### ✅ Tareas (`/api/tasks`)

#### Crear Tarea
```http
POST /api/tasks
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Mi Tarea",
  "description": "Descripción de la tarea",
  "priority": "high",
  "project_id": 1,
  "assigned_to_id": 2
}
```

#### Listar Tareas del Proyecto (con filtros)
```http
GET /api/tasks/project/{project_id}
Authorization: Bearer {token}

# Con filtros opcionales
GET /api/tasks/project/1?status_filter=pending&priority_filter=high
GET /api/tasks/project/1?assigned_to_id=2
GET /api/tasks/project/1?creator_id=1&priority_filter=critical
```

#### Listar Mis Tareas Asignadas
```http
GET /api/tasks/my-tasks
Authorization: Bearer {token}

# Con filtros
GET /api/tasks/my-tasks?status_filter=in_progress
GET /api/tasks/my-tasks?project_id=1&priority_filter=high
```

#### Actualizar Tarea
```http
PATCH /api/tasks/{task_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Tarea Actualizada",
  "status": "in_progress",
  "priority": "critical"
}
```

#### Cambiar Estado de Tarea
```http
PATCH /api/tasks/{task_id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "completed"
}
```

#### Eliminar Tarea
```http
DELETE /api/tasks/{task_id}
Authorization: Bearer {token}
```

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

# Combinación de múltiples filtros con paginación
GET /api/tasks/project/1?status_filter=pending&priority_filter=high&assigned_to_id=2&skip=0&limit=25
```

---

## 🧪 Guía de Testing

### Archivo de Colección REST

Se incluye **`API_REQUESTS.rest`** con **50+ ejemplos de requests** completamente documentados:

- ✅ Requests de autenticación
- ✅ Requests de usuarios (crear, listar, actualizar, eliminar)
- ✅ Requests de proyectos (crear, agregar miembros, etc.)
- ✅ Requests de tareas (CRUD completo con filtros)
- ✅ Flujos de testing integrados
- ✅ Pruebas de seguridad y permisos
- ✅ Ejemplos de cada rol

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

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Solo tests unitarios
pytest tests/unit -v

# Solo tests de integración
pytest tests/integration -v

# Con coverage
pytest tests/ --cov=app --cov-report=html
```

---

## 🗄️ Modelos de Base de Datos

### User (Usuarios)

```python
- id: INT, PRIMARY KEY
- username: VARCHAR(255), UNIQUE
- email: VARCHAR(255), UNIQUE
- hashed_password: VARCHAR(255)
- first_name: VARCHAR(255)
- last_name: VARCHAR(255)
- role: ENUM('admin', 'read_write', 'read_only')
- is_active: BOOLEAN
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### Project (Proyectos)

```python
- id: INT, PRIMARY KEY
- name: VARCHAR(255)
- description: TEXT
- owner_id: INT, FOREIGN KEY (User.id)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### Task (Tareas)

```python
- id: INT, PRIMARY KEY
- title: VARCHAR(255)
- description: TEXT
- project_id: INT, FOREIGN KEY (Project.id)
- creator_id: INT, FOREIGN KEY (User.id)
- assigned_to_id: INT, FOREIGN KEY (User.id), NULLABLE
- priority: ENUM('low', 'medium', 'high', 'critical')
- status: ENUM('pending', 'in_progress', 'review', 'completed')
- due_date: DATE, NULLABLE
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
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
API_PORT=8000

# Admin inicial
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=AdminTaskFlow@2025!
```

---

## 🚀 Despliegue

### Producción

```bash
# 1. Build imagen
docker build -t taskflow-api:1.0.0 .

# 2. Run contenedor
docker run -d \
  --name taskflow \
  -p 8000:8000 \
  --env-file .env \
  taskflow-api:1.0.0

# 3. Con Gunicorn
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

---

## 📦 Dependencias Principales

```
FastAPI==0.104.1
Uvicorn==0.24.0
SQLAlchemy==2.0.23
Pydantic==2.5.0
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.1
psycopg2-binary==2.9.9
```

Ver `requirements.txt` para versiones exactas.

---

## 📞 Soporte

**Documentación:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- TESTING_ENDPOINTS.md: Guía de testing

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0.0 ✅
