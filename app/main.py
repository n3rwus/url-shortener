from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import setup_logger
from app.routes import urls_router

logger = setup_logger()

def create_app():
    app = FastAPI(title="URL Shortener API", version="1.0.0")

    # ✅ Allow only your frontend origin(s)
    origins = [
        "http://localhost:3000",  # local dev (e.g., React)
        "https://yourfrontend.com",  # deployed frontend
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # 🔒 restrict to known domains
        allow_credentials=True,
        allow_methods=["GET", "POST"],  # only the methods you use
        allow_headers=[
            "Content-Type",  # Essential for POST requests
            "Authorization",  # If you're using authentication tokens
            "Accept",  # Common header for indicating the response type
            "X-Requested-With",  # To support AJAX requests
            "X-Frame-Options",  # Security measure for framing
        ],
    )

    app.include_router(urls_router.router)

    return app

app = create_app()

@app.get("/")
async def root():
    return {"message": "Welcome to the TinyURL-style FastAPI service!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
