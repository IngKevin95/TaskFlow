# 🧪 Guía Completa de Testing - TaskFlow API

**Fecha:** 6 de noviembre de 2025  
**Base URL:** `http://localhost:8000`  
**Credenciales Admin:** 
- Username: `admin`
- Password: `AdminTaskFlow@2025!`

---

## 📋 Tabla de Contenidos

1. [Autenticación](#autenticación)
2. [Gestión de Usuarios](#gestión-de-usuarios)
3. [Gestión de Proyectos](#gestión-de-proyectos)
4. [Gestión de Tareas](#gestión-de-tareas)
5. [Control de Acceso (RBAC)](#control-de-acceso-rbac)
6. [Escenarios de Error](#escenarios-de-error)

---

## 🔐 Autenticación

### 1️⃣ Login - Obtener Token (SIN autenticación requerida)

**Endpoint:** `POST /api/auth/login`

**Descripción:** Autentica un usuario y devuelve un JWT token válido por 24 horas.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=AdminTaskFlow@2025!"
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTc2MjU3NTM0Nn0.HgAxD5rlDenIynASoevhC8HhBA73SeonD2nVDjgwGzQ",
  "token_type": "bearer"
}
```

**Escenarios de Error:**

❌ **Credenciales inválidas:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=passwordIncorrecto"
```
Response (401):
```json
{
  "detail": "Credenciales inválidas"
}
```

❌ **Usuario no existe:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=noexiste&password=AdminTaskFlow@2025!"
```
Response (401):
```json
{
  "detail": "Credenciales inválidas"
}
```

---

### 2️⃣ Get Me - Obtener Datos del Usuario (CON autenticación requerida)

**Endpoint:** `GET /api/auth/me`

**Descripción:** Devuelve la información del usuario autenticado.

**Request:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTc2MjU3NTM0Nn0.HgAxD5rlDenIynASoevhC8HhBA73SeonD2nVDjgwGzQ"

curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "System",
  "last_name": "Administrator",
  "role": "admin",
  "is_active": true,
  "created_at": "2025-11-07T03:13:43.099284",
  "updated_at": "2025-11-07T03:13:43.099288"
}
```

**Escenarios de Error:**

❌ **Sin token:**
```bash
curl -X GET "http://localhost:8000/api/auth/me"
```
Response (401):
```json
{
  "detail": "No token provided"
}
```

❌ **Token inválido:**
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer token_invalido_xyz"
```
Response (401):
```json
{
  "detail": "Invalid or expired token"
}
```

❌ **Token expirado:**
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTcwMDAwMDAwMH0.old"
```
Response (401):
```json
{
  "detail": "Invalid or expired token"
}
```

---

## 👥 Gestión de Usuarios

**Requisito:** Token de autenticación + Rol ADMIN o READ_WRITE (con limitaciones)

### 3️⃣ Crear Usuario (ADMIN y READ_WRITE)

**Endpoint:** `POST /api/users/`

**Descripción:** 
- **ADMIN:** Puede crear usuarios con cualquier rol (admin, read_write, read_only)
- **READ_WRITE:** Solo puede crear usuarios con rol read_only
- **READ_ONLY:** No puede crear usuarios

**Request (como ADMIN):**
```bash
TOKEN="<your-admin-token>"

curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan.developer",
    "email": "juan@example.com",
    "password": "SecurePass123!",
    "role": "read_write",
    "first_name": "Juan",
    "last_name": "Developer"
  }'
```

**Response (201 Created):**
```json
{
  "id": 2,
  "username": "juan.developer",
  "email": "juan@example.com",
  "first_name": "Juan",
  "last_name": "Developer",
  "role": "read_write",
  "is_active": true,
  "created_at": "2025-11-07T04:20:15.123456",
  "updated_at": "2025-11-07T04:20:15.123456"
}
```

**Request (como READ_WRITE - crear user READ_ONLY):**
```bash
TOKEN="<your-read-write-token>"

curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria.viewer",
    "email": "maria@example.com",
    "password": "ViewerPass123!",
    "role": "read_only",
    "first_name": "María",
    "last_name": "Viewer"
  }'
```

**Response (201 Created):**
```json
{
  "id": 3,
  "username": "maria.viewer",
  "email": "maria@example.com",
  "first_name": "María",
  "last_name": "Viewer",
  "role": "read_only",
  "is_active": true,
  "created_at": "2025-11-07T04:21:30.654321",
  "updated_at": "2025-11-07T04:21:30.654321"
}
```

**Escenarios de Error:**

❌ **READ_WRITE intenta crear ADMIN:**
```bash
TOKEN="<read-write-token>"

curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new.admin",
    "email": "admin2@example.com",
    "password": "AdminPass123!",
    "role": "admin",
    "first_name": "Nuevo",
    "last_name": "Admin"
  }'
```
Response (403):
```json
{
  "detail": "READ_WRITE users can only create READ_ONLY users. Requested: admin"
}
```

❌ **READ_ONLY intenta crear usuario:**
```bash
TOKEN="<read-only-token>"

curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "otro.user",
    "email": "otro@example.com",
    "password": "Pass123!",
    "role": "read_only",
    "first_name": "Otro",
    "last_name": "User"
  }'
```
Response (403):
```json
{
  "detail": "Users with READ_ONLY role cannot create new users"
}
```

❌ **Usuario ya existe:**
```bash
TOKEN="<admin-token>"

curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "nuevo@example.com",
    "password": "Pass123!",
    "role": "read_write",
    "first_name": "Nuevo",
    "last_name": "User"
  }'
```
Response (400):
```json
{
  "detail": "Usuario admin ya existe"
}
```

❌ **Email ya existe:**
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo.usuario",
    "email": "admin@example.com",
    "password": "Pass123!",
    "role": "read_write",
    "first_name": "Nuevo",
    "last_name": "User"
  }'
```
Response (400):
```json
{
  "detail": "El email admin@example.com ya está registrado"
}
```

❌ **Email inválido:**
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo.usuario",
    "email": "correo-invalido",
    "password": "Pass123!",
    "role": "read_write"
  }'
```
Response (422):
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "input": "correo-invalido"
    }
  ]
}
```

---

### 4️⃣ Listar Usuarios (ADMIN y READ_WRITE)

**Endpoint:** `GET /api/users/?skip=0&limit=10`

**Descripción:**
- **ADMIN:** Ve todos los usuarios
- **READ_WRITE:** Ve todos los usuarios
- **READ_ONLY:** No puede listar usuarios

**Request:**
```bash
TOKEN="<admin-token>"

curl -X GET "http://localhost:8000/api/users/?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "System",
    "last_name": "Administrator",
    "role": "admin",
    "is_active": true,
    "created_at": "2025-11-07T03:13:43.099284",
    "updated_at": "2025-11-07T03:13:43.099288"
  },
  {
    "id": 2,
    "username": "juan.developer",
    "email": "juan@example.com",
    "first_name": "Juan",
    "last_name": "Developer",
    "role": "read_write",
    "is_active": true,
    "created_at": "2025-11-07T04:20:15.123456",
    "updated_at": "2025-11-07T04:20:15.123456"
  }
]
```

**Escenarios de Error:**

❌ **READ_ONLY intenta listar:**
```bash
TOKEN="<read-only-token>"

curl -X GET "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN"
```
Response (403):
```json
{
  "detail": "READ_ONLY users cannot list users"
}
```

---

### 5️⃣ Obtener Usuario por ID (ADMIN y READ_WRITE)

**Endpoint:** `GET /api/users/{user_id}`

**Request:**
```bash
TOKEN="<admin-token>"

curl -X GET "http://localhost:8000/api/users/2" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200 OK):**
```json
{
  "id": 2,
  "username": "juan.developer",
  "email": "juan@example.com",
  "first_name": "Juan",
  "last_name": "Developer",
  "role": "read_write",
  "is_active": true,
  "created_at": "2025-11-07T04:20:15.123456",
  "updated_at": "2025-11-07T04:20:15.123456"
}
```

**Escenarios de Error:**

❌ **Usuario no existe:**
```bash
curl -X GET "http://localhost:8000/api/users/999" \
  -H "Authorization: Bearer $TOKEN"
```
Response (404):
```json
{
  "detail": "Usuario con ID 999 no encontrado"
}
```

---

### 6️⃣ Actualizar Usuario (ADMIN y READ_WRITE)

**Endpoint:** `PATCH /api/users/{user_id}`

**Descripción:**
- **ADMIN:** Puede cambiar cualquier campo incluyendo rol
- **READ_WRITE:** Solo puede cambiar a rol read_only

**Request (como ADMIN - cambiar rol):**
```bash
TOKEN="<admin-token>"

curl -X PATCH "http://localhost:8000/api/users/2" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin",
    "first_name": "Juan",
    "last_name": "Admin Developer"
  }'
```

**Response (200 OK):**
```json
{
  "id": 2,
  "username": "juan.developer",
  "email": "juan@example.com",
  "first_name": "Juan",
  "last_name": "Admin Developer",
  "role": "admin",
  "is_active": true,
  "created_at": "2025-11-07T04:20:15.123456",
  "updated_at": "2025-11-07T04:25:40.654321"
}
```

**Escenarios de Error:**

❌ **READ_WRITE intenta cambiar a admin:**
```bash
TOKEN="<read-write-token>"

curl -X PATCH "http://localhost:8000/api/users/3" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin"
  }'
```
Response (403):
```json
{
  "detail": "READ_WRITE users can only set READ_ONLY role. Requested: admin"
}
```

---

### 7️⃣ Desactivar Usuario (ADMIN solo)

**Endpoint:** `DELETE /api/users/{user_id}`

**Descripción:** Marca el usuario como inactivo (no lo elimina físicamente)

**Request:**
```bash
TOKEN="<admin-token>"

curl -X DELETE "http://localhost:8000/api/users/3" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (204 No Content):**
```
(vacío)
```

**Escenarios de Error:**

❌ **READ_WRITE intenta eliminar:**
```bash
TOKEN="<read-write-token>"

curl -X DELETE "http://localhost:8000/api/users/2" \
  -H "Authorization: Bearer $TOKEN"
```
Response (403):
```json
{
  "detail": "Only ADMIN users can delete users"
}
```

---

### 8️⃣ Cambiar Contraseña de Usuario (ADMIN solo)

**Endpoint:** `POST /api/users/{user_id}/change-password`

**Request:**
```bash
TOKEN="<admin-token>"

curl -X POST "http://localhost:8000/api/users/2/change-password" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "new_password": "NuevaPassword123!"
  }'
```

**Response (200 OK):**
```json
{
  "message": "Contraseña del usuario 2 actualizada exitosamente"
}
```

---

## 📁 Gestión de Proyectos

### 9️⃣ Crear Proyecto (Todos excepto READ_ONLY)

**Endpoint:** `POST /api/projects`

**Request:**
```bash
TOKEN="<user-token>"

curl -X POST "http://localhost:8000/api/projects" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "App Mobile - Desarrollo",
    "description": "Desarrollo de aplicación mobile para iOS y Android"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "App Mobile - Desarrollo",
  "description": "Desarrollo de aplicación mobile para iOS y Android",
  "owner_id": 2,
  "is_active": true,
  "created_at": "2025-11-07T05:10:20.123456",
  "updated_at": "2025-11-07T05:10:20.123456"
}
```

---

### 🔟 Listar Proyectos (Todos)

**Endpoint:** `GET /api/projects?skip=0&limit=10`

**Request:**
```bash
TOKEN="<user-token>"

curl -X GET "http://localhost:8000/api/projects?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "App Mobile - Desarrollo",
    "description": "Desarrollo de aplicación mobile para iOS y Android",
    "owner_id": 2,
    "is_active": true,
    "created_at": "2025-11-07T05:10:20.123456",
    "updated_at": "2025-11-07T05:10:20.123456"
  }
]
```

---

### 1️⃣1️⃣ Obtener Proyecto por ID (Dueño o miembro)

**Endpoint:** `GET /api/projects/{project_id}`

**Request:**
```bash
TOKEN="<user-token>"

curl -X GET "http://localhost:8000/api/projects/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "App Mobile - Desarrollo",
  "description": "Desarrollo de aplicación mobile para iOS y Android",
  "owner_id": 2,
  "tasks": [],
  "members": [
    {
      "id": 2,
      "username": "juan.developer",
      "email": "juan@example.com",
      "first_name": "Juan",
      "last_name": "Developer",
      "role": "admin"
    }
  ],
  "is_active": true,
  "created_at": "2025-11-07T05:10:20.123456",
  "updated_at": "2025-11-07T05:10:20.123456"
}
```

---

### 1️⃣2️⃣ Actualizar Proyecto (ADMIN solo)

**Endpoint:** `PATCH /api/projects/{project_id}`

**Request:**
```bash
TOKEN="<admin-token>"

curl -X PATCH "http://localhost:8000/api/projects/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "App Mobile - En Producción",
    "description": "Aplicación mobile en producción - soporte y mantenimiento"
  }'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "App Mobile - En Producción",
  "description": "Aplicación mobile en producción - soporte y mantenimiento",
  "owner_id": 2,
  "is_active": true,
  "created_at": "2025-11-07T05:10:20.123456",
  "updated_at": "2025-11-07T05:15:45.987654"
}
```

---

### 1️⃣3️⃣ Eliminar Proyecto (Dueño solo)

**Endpoint:** `DELETE /api/projects/{project_id}`

**Request:**
```bash
TOKEN="<owner-token>"

curl -X DELETE "http://localhost:8000/api/projects/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (204 No Content):**
```
(vacío)
```

---

## ✅ Gestión de Tareas

### 1️⃣4️⃣ Crear Tarea (Todos excepto READ_ONLY)

**Endpoint:** `POST /api/projects/{project_id}/tasks`

**Request:**
```bash
TOKEN="<user-token>"

curl -X POST "http://localhost:8000/api/projects/1/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar autenticación",
    "description": "Implementar JWT authentication con roles",
    "priority": "high",
    "status": "in_progress",
    "assigned_to": 2
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Implementar autenticación",
  "description": "Implementar JWT authentication con roles",
  "priority": "high",
  "status": "in_progress",
  "project_id": 1,
  "creator_id": 2,
  "assigned_to": 2,
  "created_at": "2025-11-07T05:20:30.123456",
  "updated_at": "2025-11-07T05:20:30.123456"
}
```

---

### 1️⃣5️⃣ Listar Tareas del Proyecto (Todos)

**Endpoint:** `GET /api/projects/{project_id}/tasks`

**Request:**
```bash
TOKEN="<user-token>"

curl -X GET "http://localhost:8000/api/projects/1/tasks" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Implementar autenticación",
    "description": "Implementar JWT authentication con roles",
    "priority": "high",
    "status": "in_progress",
    "project_id": 1,
    "creator_id": 2,
    "assigned_to": 2,
    "created_at": "2025-11-07T05:20:30.123456",
    "updated_at": "2025-11-07T05:20:30.123456"
  }
]
```

---

### 1️⃣6️⃣ Actualizar Tarea (ADMIN solo)

**Endpoint:** `PATCH /api/projects/{project_id}/tasks/{task_id}`

**Request:**
```bash
TOKEN="<admin-token>"

curl -X PATCH "http://localhost:8000/api/projects/1/tasks/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "priority": "medium"
  }'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Implementar autenticación",
  "description": "Implementar JWT authentication con roles",
  "priority": "medium",
  "status": "completed",
  "project_id": 1,
  "creator_id": 2,
  "assigned_to": 2,
  "created_at": "2025-11-07T05:20:30.123456",
  "updated_at": "2025-11-07T05:25:15.654321"
}
```

---

### 1️⃣7️⃣ Eliminar Tarea (ADMIN solo)

**Endpoint:** `DELETE /api/projects/{project_id}/tasks/{task_id}`

**Request:**
```bash
TOKEN="<admin-token>"

curl -X DELETE "http://localhost:8000/api/projects/1/tasks/1" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (204 No Content):**
```
(vacío)
```

---

## 🛡️ Control de Acceso (RBAC)

### Matriz de Permisos

| Endpoint | ADMIN | READ_WRITE | READ_ONLY |
|----------|-------|-----------|-----------|
| POST /auth/login | ✅ | ✅ | ✅ |
| GET /auth/me | ✅ | ✅ | ✅ |
| POST /users/ | ✅ (cualquier rol) | ✅ (solo read_only) | ❌ |
| GET /users/ | ✅ | ✅ | ❌ |
| GET /users/{id} | ✅ | ✅ | ❌ |
| PATCH /users/{id} | ✅ | ✅ (solo read_only) | ❌ |
| DELETE /users/{id} | ✅ | ❌ | ❌ |
| POST /users/{id}/change-password | ✅ | ❌ | ❌ |
| POST /projects | ✅ | ✅ | ❌ |
| GET /projects | ✅ | ✅ | ✅ |
| GET /projects/{id} | ✅ | ✅ | ✅ |
| PATCH /projects/{id} | ✅ | ❌ | ❌ |
| DELETE /projects/{id} | Solo dueño | Solo dueño | ❌ |
| POST /projects/{id}/tasks | ✅ | ✅ | ❌ |
| GET /projects/{id}/tasks | ✅ | ✅ | ✅ |
| PATCH /projects/{id}/tasks/{id} | ✅ | ❌ | ❌ |
| DELETE /projects/{id}/tasks/{id} | ✅ | ❌ | ❌ |

---

## ⚠️ Escenarios de Error

### Errores de Autenticación

**401 Unauthorized - No token:**
```json
{
  "detail": "No token provided"
}
```

**401 Unauthorized - Token inválido:**
```json
{
  "detail": "Invalid or expired token"
}
```

**401 Unauthorized - Credenciales inválidas:**
```json
{
  "detail": "Credenciales inválidas"
}
```

### Errores de Autorización

**403 Forbidden - Rol insuficiente:**
```json
{
  "detail": "Users with READ_ONLY role cannot create new users"
}
```

**403 Forbidden - Permiso específico:**
```json
{
  "detail": "Only ADMIN users can delete users"
}
```

### Errores de Validación

**422 Unprocessable Entity - Email inválido:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "input": "correo-invalido"
    }
  ]
}
```

**422 Unprocessable Entity - Campo faltante:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "username"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

### Errores de Recurso

**404 Not Found - Usuario no existe:**
```json
{
  "detail": "Usuario con ID 999 no encontrado"
}
```

**404 Not Found - Proyecto no existe:**
```json
{
  "detail": "Proyecto con ID 999 no encontrado"
}
```

**400 Bad Request - Usuario duplicado:**
```json
{
  "detail": "Usuario admin ya existe"
}
```

**400 Bad Request - Email duplicado:**
```json
{
  "detail": "El email admin@example.com ya está registrado"
}
```

---

## 🧪 Flujos de Testing Completos

### Flujo 1: Crear un admin y gestionar proyectos

```bash
# 1. Login como admin
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=AdminTaskFlow@2025!" | jq -r '.access_token')

echo "✅ Token obtenido: $TOKEN"

# 2. Crear usuario READ_WRITE
USER_ID=$(curl -s -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "developer",
    "email": "dev@example.com",
    "password": "DevPass123!",
    "role": "read_write",
    "first_name": "Dev",
    "last_name": "User"
  }' | jq '.id')

echo "✅ Usuario creado: $USER_ID"

# 3. Crear proyecto
PROJECT_ID=$(curl -s -X POST "http://localhost:8000/api/projects" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Testing Project",
    "description": "Proyecto para testing"
  }' | jq '.id')

echo "✅ Proyecto creado: $PROJECT_ID"

# 4. Crear tarea
TASK_ID=$(curl -s -X POST "http://localhost:8000/api/projects/$PROJECT_ID/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Task",
    "description": "Tarea de prueba",
    "priority": "high",
    "status": "in_progress"
  }' | jq '.id')

echo "✅ Tarea creada: $TASK_ID"
```

---

## 📝 Notas Importantes

- **Token válido por:** 24 horas
- **Host:** localhost:8000
- **Protocolo:** HTTP (desarrollo) / HTTPS (producción)
- **Autenticación:** Bearer Token (JWT)
- **Formato de respuestas:** JSON

---

## 🔗 Recursos

- Swagger UI: `http://localhost:8000/api/docs`
- OpenAPI JSON: `http://localhost:8000/api/openapi.json`
- Health Check: `http://localhost:8000/health`

