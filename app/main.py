from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.modules.users.routes import router as users_router
from app.modules.chats.routes import router as chat_router
from app.infrastructure.init_db import init_db

init_db()

app = FastAPI(
    title="Japi AI Tutor API",
    description="Backend API for Japi AI Tutor - A personalized English learning assistant",
    version="1.0.0",
    contact={
        "name": "Aman",
        "email": "m.jawahiruzzaman@gmail.com"
    },
    license_info={
        "name": "MIT"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Japi AI Tutor API",
        "documentation": "/docs",
        "version": "1.0.0"
    }

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Japi AI Tutor API",
        version="1.0.0",
        description="Backend API for Japi AI Tutor - A personalized English learning assistant",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    for path in openapi_schema.get("paths", {}).values():
        for method in path.values():
            if method.get("operationId") in ["root__get"]:
                continue
            method["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
