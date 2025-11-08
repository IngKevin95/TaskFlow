# 📚 Ejemplos de Uso de la API RBAC

## 🔐 Autenticación

### 1. Login del Admin
⚠️ **IMPORTANTE**: Este endpoint **NO requiere Authorization**. Solo envía username y password.

```bash
curl -X POST "http://localhost:8000/api/auth/login?username=admin&password=AdminTaskFlow@2025!" \
  -H "Content-Type: application/json"
```

**Parámetros:**
- `username=admin` - En la URL como query parameter
- `password=AdminTaskFlow@2025!` - En la URL como query parameter

**Respuesta (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTc2MjU3MjExN30.F2SM8gRyFfpo5rtHiyq5w58Mb4l25TP1KmkoIMMHvOE",
  "token_type": "bearer"
}
```

**¿Qué hacer con el token?**
1. Guarda el valor de `access_token` 
2. Úsalo en el header `Authorization: Bearer {access_token}` para las próximas peticiones

### 2. Obtener Info del Usuario Autenticado
✅ **Este endpoint SÍ requiere Authorization**. Envía el token que obtuviste del login.

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTc2MjU3MjExN30.F2SM8gRyFfpo5rtHiyq5w58Mb4l25TP1KmkoIMMHvOE"
```

**Headers:**
- `Authorization: Bearer {access_token}` - Donde `{access_token}` es el token que obtuviste del login

**Respuesta (200 OK):**
```json
{
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "System",
  "last_name": "Administrator",
  "id": 1,
  "role": "admin",
  "is_active": true,
  "created_at": "2025-11-07T03:13:43.099284",
  "updated_at": "2025-11-07T03:13:43.099288"
}
```

---

## 👥 Gestión de Usuarios (Solo ADMIN)

⚠️ **TODOS estos endpoints requieren Authorization**. Debes enviar el token del admin en el header.

### 1. Crear Usuario con Rol READ_WRITE
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTc2MjU3MjExN30.F2SM8gRyFfpo5rtHiyq5w58Mb4l25TP1KmkoIMMHvOE" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "email": "juan@example.com",
    "password": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "read_write"
  }'
```

**Body JSON (en el body, no en la URL):**
```json
{
  "username": "juan",
  "email": "juan@example.com",
  "password": "SecurePass123!",
  "first_name": "Juan",
  "last_name": "Pérez",
  "role": "read_write"
}
```

**Headers:**
- `Authorization: Bearer {access_token}` - Token del admin
- `Content-Type: application/json` - Indica que es JSON

**Respuesta (201 Created):**
```json
{
  "username": "juan",
  "email": "juan@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "id": 2,
  "role": "read_write",
  "is_active": true,
  "created_at": "2025-11-07T03:15:22.123456",
  "updated_at": "2025-11-07T03:15:22.123456"
}
```

### 2. Crear Usuario con Rol READ_ONLY
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria",
    "email": "maria@example.com",
    "password": "SecurePass456!",
    "first_name": "María",
    "last_name": "García",
    "role": "read_only"
  }'
```

**Body JSON:**
```json
{
  "username": "maria",
  "email": "maria@example.com",
  "password": "SecurePass456!",
  "first_name": "María",
  "last_name": "García",
  "role": "read_only"
}
```

### 3. Crear Usuario con Rol ADMIN
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "carlos",
    "email": "carlos@example.com",
    "password": "SecurePass789!",
    "first_name": "Carlos",
    "last_name": "López",
    "role": "admin"
  }'
```

**Body JSON:**
```json
{
  "username": "carlos",
  "email": "carlos@example.com",
  "password": "SecurePass789!",
  "first_name": "Carlos",
  "last_name": "López",
  "role": "admin"
}
```

---

## 📋 Operaciones CRUD de Usuarios

### 1. Listar Todos los Usuarios
```bash
curl -X GET "http://localhost:8000/api/users/?skip=0&limit=10" \
  -H "Authorization: Bearer {admin_token}"
```

**Respuesta (200 OK):**
```json
[
  {
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "System",
    "last_name": "Administrator",
    "id": 1,
    "role": "admin",
    "is_active": true,
    "created_at": "2025-11-07T03:13:43.099284",
    "updated_at": "2025-11-07T03:13:43.099288"
  },
  {
    "username": "juan",
    "email": "juan@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "id": 2,
    "role": "read_write",
    "is_active": true,
    "created_at": "2025-11-07T03:15:22.123456",
    "updated_at": "2025-11-07T03:15:22.123456"
  }
]
```

### 2. Obtener Usuario por ID
```bash
curl -X GET "http://localhost:8000/api/users/2" \
  -H "Authorization: Bearer {admin_token}"
```

**Respuesta (200 OK):**
```json
{
  "username": "juan",
  "email": "juan@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "id": 2,
  "role": "read_write",
  "is_active": true,
  "created_at": "2025-11-07T03:15:22.123456",
  "updated_at": "2025-11-07T03:15:22.123456"
}
```

### 3. Actualizar Usuario (Cambiar Rol/Estado)
```bash
curl -X PATCH "http://localhost:8000/api/users/2" \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin",
    "is_active": true
  }'
```

**Body JSON:**
```json
{
  "role": "admin",
  "is_active": true
}
```

**Respuesta (200 OK):**
```json
{
  "username": "juan",
  "email": "juan@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "id": 2,
  "role": "admin",
  "is_active": true,
  "created_at": "2025-11-07T03:15:22.123456",
  "updated_at": "2025-11-07T03:20:45.654321"
}
```

### 4. Cambiar Contraseña de Usuario
```bash
curl -X POST "http://localhost:8000/api/users/2/change-password" \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "new_password": "NewSecurePass999!"
  }'
```

**Body JSON:**
```json
{
  "new_password": "NewSecurePass999!"
}
```

**Respuesta (200 OK):**
```json
{
  "message": "Contraseña actualizada exitosamente",
  "username": "juan"
}
```

### 5. Desactivar Usuario (Soft Delete)
```bash
curl -X DELETE "http://localhost:8000/api/users/2" \
  -H "Authorization: Bearer {admin_token}"
```

**Respuesta (200 OK):**
```json
{
  "message": "Usuario desactivado exitosamente",
  "username": "juan"
}
```

---

## 🔑 Información de Roles

### Roles Disponibles

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| `admin` | Administrador del sistema | Acceso total, crear/editar/eliminar usuarios |
| `read_write` | Editor | Leer y escribir datos |
| `read_only` | Lector | Solo lectura de datos |

---

## ⚠️ Códigos de Error

### 401 Unauthorized
```json
{
  "detail": "Credenciales inválidas"
}
```

### 403 Forbidden
```json
{
  "detail": "No tienes permisos para realizar esta acción"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "input": "invalid-email"
    }
  ]
}
```

### 409 Conflict
```json
{
  "detail": "Usuario juan ya existe"
}
```

---

## 📝 Notas Importantes

1. **Token Expiration**: Los tokens expiran después de 24 horas
2. **Contraseña**: Mínimo 8 caracteres, máximo 50
3. **Email**: Debe ser un email válido
4. **Username**: 3-50 caracteres
5. **Soft Delete**: Los usuarios no se eliminan, solo se desactivan (`is_active: false`)
6. **Solo ADMIN**: Solo usuarios con rol `admin` pueden crear/editar/eliminar otros usuarios

---

## 🚀 Ejemplo Completo: Workflow

### 1. Login como admin
```bash
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login?username=admin&password=AdminTaskFlow@2025!" | jq -r '.access_token')
echo "Token: $TOKEN"
```

### 2. Crear nuevo usuario
```bash
curl -s -X POST "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "developers",
    "email": "dev@example.com",
    "password": "DevPass123!",
    "first_name": "Developer",
    "last_name": "Team",
    "role": "read_write"
  }' | jq .
```

### 3. Listar usuarios
```bash
curl -s -X GET "http://localhost:8000/api/users/?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### 4. Login con el nuevo usuario
```bash
NEW_TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login?username=developers&password=DevPass123!" | jq -r '.access_token')
echo "Nuevo Token: $NEW_TOKEN"
```

### 5. Ver información del nuevo usuario
```bash
curl -s -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $NEW_TOKEN" | jq .
```

