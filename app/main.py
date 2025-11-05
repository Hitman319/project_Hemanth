"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import hello


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
    )

    # Include API routes
    app.include_router(
        hello.router,
        prefix=settings.api_v1_prefix,
        tags=["hello"]
    )

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
