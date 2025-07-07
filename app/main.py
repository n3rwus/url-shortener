from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import setup_logger
from app.routes import urls_router

logger = setup_logger()

def create_app():
    app = FastAPI(
        title="URL Shortener API",
        version="0.0.1",
        servers=[{"url": "http://127.0.0.1:8000"}]
    )

    origins = [
        "http://localhost:3000",
        "https://yourfrontend.com",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=[
            "Content-Type", "Authorization", "Accept",
            "X-Requested-With", "X-Frame-Options"
        ],
    )

    app.include_router(urls_router.router)

    return app

app = create_app()

