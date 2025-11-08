# 📖 Guía Completa: Cómo Usar Swagger para Consumir la API RBAC

## 🚀 Acceso a Swagger

Abre tu navegador y ve a:
```
http://localhost:8000/api/docs
```

Verás la interfaz de Swagger con todos los endpoints disponibles.

---

## 🔐 PASO 1: Autenticarse (Login)

### En Swagger:

1. **Busca la sección "auth"** (en la parte superior izquierda)
2. **Abre el endpoint:** `POST /api/auth/login`
3. **Haz clic en "Try it out"**

### Parámetros a enviar:

En la sección de parámetros, verás dos campos:
- `username` → Escribe: `admin`
- `password` → Escribe: `AdminTaskFlow@2025!`

### Envía la petición:

1. Haz clic en el botón azul **"Execute"**
2. Espera la respuesta

### Respuesta esperada (200 OK):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTc2MjU3MjExN30.F2SM8gRyFfpo5rtHiyq5w58Mb4l25TP1KmkoIMMHvOE",
  "token_type": "bearer"
}
```

### 📋 Copia el token:

**Copia el valor completo de `access_token`** (todo el texto largo entre comillas). Lo necesitarás para los siguientes pasos.

---

## 🔑 PASO 2: Autorizar Swagger con el Token

Esta es la parte **más importante** para que funcione:

### 1. Haz clic en el botón **"Authorize"** (arriba a la derecha de Swagger)

![Botón Authorize en Swagger]

### 2. Se abrirá un modal con el título "Available authorizations"

### 3. En el campo que dice "HTTPBearer", pega el token:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTc2MjU3MjExN30.F2SM8gRyFfpo5rtHiyq5w58Mb4l25TP1KmkoIMMHvOE
```

⚠️ **IMPORTANTE**: Solo pega el token, **sin la palabra "Bearer"**. Swagger la agrega automáticamente.

### 4. Haz clic en **"Authorize"** (el botón azul del modal)

### 5. Haz clic en **"Close"**

✅ **Ahora estás autenticado en Swagger**. El token se enviará automáticamente en todos los siguientes requests.

---

## 👤 PASO 3: Obtener Tu Información (GET /api/auth/me)

### En Swagger:

1. **Busca el endpoint:** `GET /api/auth/me` (en la sección "auth")
2. **Haz clic en "Try it out"**
3. **Haz clic en "Execute"**

### Respuesta esperada (200 OK):

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

✅ **¡Funciona!** Ahora ves tu información de usuario.

---

## 👥 PASO 4: Crear Nuevo Usuario (POST /api/users/)

### En Swagger:

1. **Busca el endpoint:** `POST /api/users/` (en la sección "users")
2. **Haz clic en "Try it out"**

### Datos a enviar (Body JSON):

En el campo de texto que aparece, pega esto:

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

### Haz clic en **"Execute"**

### Respuesta esperada (201 Created):

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

✅ **¡Usuario creado exitosamente!**

---

## 📋 PASO 5: Listar Todos los Usuarios (GET /api/users/)

### En Swagger:

1. **Busca el endpoint:** `GET /api/users/` (en la sección "users")
2. **Haz clic en "Try it out"**
3. Puedes ajustar los parámetros opcionales:
   - `skip`: 0 (comenzar desde el primer usuario)
   - `limit`: 10 (obtener máximo 10 usuarios)
4. **Haz clic en "Execute"**

### Respuesta esperada (200 OK):

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

✅ **¡Ves todos los usuarios!**

---

## 🔄 PASO 6: Actualizar Usuario (PATCH /api/users/{id})

### En Swagger:

1. **Busca el endpoint:** `PATCH /api/users/{id}` (en la sección "users")
2. **Haz clic en "Try it out"**
3. En el parámetro `id`, escribe: `2` (para actualizar a Juan)

### Datos a enviar (Body JSON):

```json
{
  "role": "admin",
  "is_active": true
}
```

### Haz clic en **"Execute"**

### Respuesta esperada (200 OK):

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

✅ **¡Juan ahora es ADMIN!**

---

## ⚠️ Solución de Problemas

### Error: "No token provided"

**Causa:** No autorizaste Swagger con el token.

**Solución:**
1. Haz clic en **"Authorize"** (arriba a la derecha)
2. Pega tu token en el campo **"HTTPBearer"**
3. Haz clic en **"Authorize"** nuevamente
4. Cierra el modal

### Error: "Token expired"

**Causa:** El token expiró (después de 24 horas).

**Solución:**
1. Vuelve al endpoint `POST /api/auth/login`
2. Obtén un nuevo token
3. Vuelve a autorizar Swagger con el nuevo token

### Error: "No tienes permisos para realizar esta acción"

**Causa:** Tu rol no tiene permisos para esa acción.

**Solución:**
- Solo **ADMIN** puede crear/editar/eliminar usuarios
- Asegúrate de estar usando un token de admin

### Error: "Usuario juan ya existe"

**Causa:** Ya existe un usuario con ese nombre.

**Solución:**
- Usa un nombre de usuario diferente
- O borra el usuario anterior

---

## 📝 Resumen de Endpoints Principales

| Método | Endpoint | Descripción | Requiere Auth |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login` | Obtener token | ❌ No |
| GET | `/api/auth/me` | Ver tu info | ✅ Sí |
| POST | `/api/users/` | Crear usuario | ✅ Sí (Admin) |
| GET | `/api/users/` | Listar usuarios | ✅ Sí (Admin) |
| GET | `/api/users/{id}` | Ver usuario | ✅ Sí (Admin) |
| PATCH | `/api/users/{id}` | Actualizar usuario | ✅ Sí (Admin) |
| DELETE | `/api/users/{id}` | Desactivar usuario | ✅ Sí (Admin) |
| POST | `/api/users/{id}/change-password` | Cambiar contraseña | ✅ Sí (Admin) |

---

## 🎯 Checklist de Prueba

- [ ] Login y obtener token
- [ ] Autorizar Swagger con el token
- [ ] Ver tu información con GET /api/auth/me
- [ ] Crear un nuevo usuario
- [ ] Listar todos los usuarios
- [ ] Obtener un usuario específico
- [ ] Actualizar el rol de un usuario
- [ ] Cambiar la contraseña de un usuario

