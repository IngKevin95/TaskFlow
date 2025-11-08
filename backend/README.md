# TaskFlow Backend API

API RESTful para la gestión colaborativa de tareas usando FastAPI y PostgreSQL.

## 🚀 Configuración Rápida

### Requisitos Previos

- Python 3.11+
- PostgreSQL 12+
- pip o poetry
- Docker (opcional)

### Instalación

#### Opción 1: Instalación Local

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus valores
```

4. **Ejecutar servidor**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Opción 2: Usando Docker Compose

```bash
docker-compose up -d
```

### Estructura del Proyecto

```
backend/
├── app/
│   ├── core/              # Security, exceptions, constants
│   ├── models/            # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic validation schemas
│   ├── repositories/      # Data access layer
│   ├── services/          # Business logic layer
│   ├── api/routers/       # API endpoints
│   ├── database/          # Database configuration
│   ├── utils/             # Utility functions
│   ├── config.py          # Application settings
│   └── main.py            # FastAPI entry point
├── tests/                 # Unit and integration tests
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker configuration
└── Dockerfile             # Container image
```

## 📚 Documentación de API

Una vez que el servidor está corriendo, accede a la documentación interactiva:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 🔑 Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación.

### Registro de Usuario

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePassword123"
  }'
```

### Usar Token

```bash
curl -X GET "http://localhost:8000/api/projects" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🗄️ Base de Datos

### Modelos Principales

#### User
- `id`: Identificador único
- `username`: Nombre de usuario (único)
- `email`: Correo electrónico (único)
- `password_hash`: Contraseña hasheada con bcrypt
- `first_name`: Nombre
- `last_name`: Apellido
- `is_active`: Estado del usuario
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

#### Project
- `id`: Identificador único
- `name`: Nombre del proyecto
- `description`: Descripción
- `owner_id`: ID del propietario (FK to User)
- `members`: Relación Many-to-Many con User
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

#### Task
- `id`: Identificador único
- `title`: Título de la tarea
- `description`: Descripción
- `project_id`: ID del proyecto (FK)
- `creator_id`: ID del creador (FK)
- `assigned_to_id`: ID del asignado (FK)
- `priority`: Prioridad (low, medium, high, critical)
- `status`: Estado (pending, in_progress, review, completed)
- `due_date`: Fecha de vencimiento
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

## 🧪 Testing

### Ejecutar Tests

```bash
# Tests unitarios
pytest tests/unit -v

# Tests de integración
pytest tests/integration -v

# Todos los tests con coverage
pytest tests/ --cov=app --cov-report=html
```

## 🔧 Desarrollo

### Inicializar Base de Datos

```python
from app.database.session import create_tables
create_tables()
```

### Limpiar Base de Datos

```python
from app.database.session import drop_tables
drop_tables()
```

## 📦 Dependencias Principales

- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **python-jose** - JWT tokens
- **passlib** - Password hashing
- **psycopg2** - Driver PostgreSQL
- **pytest** - Testing framework

## 🚀 Despliegue

### Producción

1. Actualizar variables de entorno
2. Usar Gunicorn en lugar de Uvicorn:
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

3. Configurar reverse proxy (nginx)

## 📝 Convenciones

- Usar `snake_case` para variables y funciones
- Usar `PascalCase` para clases
- Documentar funciones con docstrings
- Separar lógica en capas (routers → services → repositories)
- Reutilizar excepciones personalizadas

## 🤝 Contribuir

1. Crear rama (`git checkout -b feature/NewFeature`)
2. Commit cambios (`git commit -m 'Add NewFeature'`)
3. Push a rama (`git push origin feature/NewFeature`)
4. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 📞 Soporte

Para reportar bugs o sugerencias, crear un issue en el repositorio.
