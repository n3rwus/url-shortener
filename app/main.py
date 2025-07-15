from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.logging_config import setup_logger
from app.routes import urls_router
from starlette.responses import JSONResponse
from starlette import status

logger = setup_logger()
settings = get_settings()


def create_app():
    application = FastAPI(
        title="URL Shortener API",
        version="0.0.1",
        docs_url="/docs" if settings.ENV else None,
        redoc_url="/redoc" if settings.ENV else None,
        openapi_url="/openapi.json" if settings.ENV else None
    )

    origins = [
        "http://localhost:3000",
        "https://yourfrontend.com",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=[
            "Content-Type", "Authorization", "Accept",
            "X-Requested-With", "X-Frame-Options"
        ],
    )


    @application.get("/v1/health")
    def health_check():
        return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_200_OK)

    application.include_router(urls_router.router)

    return application

app = create_app()




