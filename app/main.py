from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from app.core.logging_config import setup_logger
from app.routes import urls_router

logger = setup_logger()

def create_app():
    application = FastAPI(
        title="URL Shortener API",
        version="0.0.1",
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

    application.include_router(urls_router.router)

    @application.get("/v1/health")
    def health_check():
        return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_200_OK)

    return application

app = create_app()




