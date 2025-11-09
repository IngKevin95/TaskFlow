"""
FastAPI application entry point
"""
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.database.session import create_tables, get_db, SessionLocal
from app.api.routers import auth, users, projects, tasks


# Startup event
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("Starting up TaskFlow API...")
    try:
        # Create database tables
        create_tables()
        print("Database tables created successfully")
        
        # Initialize admin user if needed
        from app.services.auth_service import AuthService
        from app.core.enums import UserRole
        from app.models.models import User
        from datetime import datetime, timezone
        from app.core.security import hash_password
        
        db = SessionLocal()
        try:
            admin_user = db.query(User).filter(User.username == "admin").first()
            if not admin_user:
                print("Creating default admin user...")
                admin_user = User(
                    username="admin",
                    email="admin@example.com",
                    hashed_password=hash_password(os.getenv("ADMIN_PASSWORD", "AdminTaskFlow@2025!")),
                    first_name="Admin",
                    last_name="User",
                    role=UserRole.ADMIN.value,
                    is_active=True,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                db.add(admin_user)
                db.commit()
                print("Default admin user created successfully")
        finally:
            db.close()
            
    except Exception as e:
        print(f"Startup error: {e}")
    
    yield
    
    # Shutdown
    print("Shutting down TaskFlow API...")


# Create FastAPI application
app = FastAPI(
    title="TaskFlow API",
    description="API para gestión de tareas con autenticación JWT y control de roles RBAC",
    version="1.0.0",
    docs_url=None,  # Lo crearemos personalizado
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# Custom OpenAPI schema with Bearer token security
def custom_openapi():
    """
    Custom OpenAPI schema with JWT Bearer authentication
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="TaskFlow API",
        version="1.0.0",
        description="""
        ## API para gestión de tareas con autenticación JWT y control de roles RBAC
        
        ### 🔐 Autenticación
        
        Esta API utiliza autenticación JWT (JSON Web Token) con Bearer scheme.
        
        **Pasos para autenticarte:**
        
        1. **Obtén un token**: Usa el endpoint `/api/auth/login` con tus credenciales (username y password)
        2. **Copia el token**: Del campo `access_token` en la respuesta
        3. **Autorízate**: Haz clic en el botón **"Authorize" 🔓** (arriba a la derecha)
        4. **Pega el token**: En el campo "Value" (sin agregar "Bearer", solo el token)
        5. **Haz clic en "Authorize"** y luego en "Close"
        
        Una vez autorizado, todas las peticiones incluirán automáticamente el token en el header `Authorization: Bearer <token>`.
        
        ### 📝 Roles de Usuario
        - **ADMIN**: Acceso completo a todos los recursos
        - **READ_WRITE**: Gestión de proyectos y tareas
        - **READ_ONLY**: Acceso limitado de solo visualización
        """,
        routes=app.routes,
    )
    
    # Add Bearer JWT security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Ingresa el token JWT obtenido del endpoint /api/auth/login (sin el prefijo 'Bearer')"
        }
    }
    
    # No aplicamos seguridad global aquí, lo hacemos por endpoint
    # El login debe ser público, otros endpoints requieren autenticación
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
try:
    from app.api.routers import auth, users, projects, tasks
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(projects.router)
    app.include_router(tasks.router)
except ImportError as e:
    print(f"Warning: Could not import some routers: {e}")


# Swagger UI personalizado
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <link type="text/css" rel="stylesheet" href="/static/swagger-custom.css">
        <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
        <title>TaskFlow API - Swagger UI</title>
    </head>
    <body>
        <div class="auth-info-banner">
            <strong>🔐 Autenticación JWT con Validación Automática</strong>
            <div class="auth-status" id="authStatus">
                <span class="status-indicator status-logged-out">🔴 No autenticado</span>
            </div>

        </div>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.ui = SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                persistAuthorization: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout"
            });
        </script>
        <script src="/static/swagger-custom.js"></script>
    </body>
    </html>
    """, status_code=200)


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status
    """
    return {"status": "healthy", "service": "TaskFlow API"}


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint
    
    Returns:
        Welcome message
    """
    return {
        "message": "Welcome to TaskFlow API",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
