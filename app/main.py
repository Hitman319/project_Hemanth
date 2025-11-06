"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import hello
from app.api.routes import ai
from app.api.routes import pdf_converter
from app.api.routes import pdf_demo
from app.api.routes import simple_pdf
# from app.api.routes import database  # Temporarily commented


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title=settings.app_name,
        description=settings.description,
        version=settings.app_version,
        debug=settings.debug,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )    # Include API routes
    app.include_router(
        hello.router,
        prefix=settings.api_v1_prefix,
        tags=["hello"]    )
    
    # Include AI routes
    app.include_router(
        ai.router,
        prefix=settings.api_v1_prefix,
        tags=["ai"]
    )
    
    # Include PDF Converter routes
    app.include_router(
        pdf_converter.router,
        prefix=settings.api_v1_prefix,
        tags=["pdf-converter"]
    )
    
    # Include PDF Demo routes (working without LLM)
    app.include_router(
        pdf_demo.demo_router,
        prefix=settings.api_v1_prefix,
        tags=["pdf-demo"]
    )
    
    # Include Simple PDF routes (guaranteed working)
    app.include_router(
        simple_pdf.simple_router,
        prefix=settings.api_v1_prefix,
        tags=["simple-pdf"]
    )
    
    # Include Database routes (temporarily commented)
    # app.include_router(
    #     database.router,
    #     prefix=settings.api_v1_prefix,
    #     tags=["database"]
    # )

    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint with welcome message"""
        return {"message": "Welcome to Hemanth's Hello World API"}

    return app


# Create the FastAPI app instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
