"""
FastAPI application entry point
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
                    email="admin@taskflow.local",
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
    description="Collaborative task management API",
    version="1.0.0",
    lifespan=lifespan
)

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
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
