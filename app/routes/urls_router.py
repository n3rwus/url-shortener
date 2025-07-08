from urllib.parse import urlparse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.integration.blacklist import fetch_blacklist, BlacklistUnavailableError
from app.core.cache import timed_cache
from app.db.database import get_db
from app.repositories.url_repository import UrlsRepository
from app.service.url_service import UrlsService
from app.schemas.schema import UrlsResponse, UrlsCreateRequest
from app.core.logging_config import setup_logger

logger = setup_logger()

router = APIRouter(tags=["Urls"])

def get_service(db: Session = Depends(get_db)) -> UrlsService:
    return UrlsService(UrlsRepository(db))

@router.post("/urls", response_model=UrlsResponse, status_code=status.HTTP_201_CREATED)
async def shorten_url(payload: UrlsCreateRequest,service: UrlsService = Depends(get_service)):

    parsed_url = urlparse(payload.original_url)

    if parsed_url.scheme not in {"http", "https"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL must start with http or https."
        )

    try:
        blacklist = await fetch_blacklist()
    except BlacklistUnavailableError:
        logger.error("Cannot validate domain: blacklist unavailable.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to validate domain against blacklist at this time. Please try again later."
        )

    domain = parsed_url.netloc.lower()
    if domain in blacklist:
        logger.info(f"Rejected blacklisted domain: {domain}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The domain '{domain}' is blacklisted."
        )

    parsed = service.shorten_url(
        original_url=payload.original_url,
        valid_until=payload.valid_until
    )

    if parsed is None:
        logger.warning("No URL object returned — likely duplicate.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A shortened URL for this link already exists"
        )

    return UrlsResponse.model_validate(parsed)

@timed_cache(seconds=300)
@router.get("/{short_code}")
def redirect_short_url(short_code: str, service: UrlsService = Depends(get_service)):
    if short_code == "favicon.ico":
        raise HTTPException(status_code=404, detail="Not Found")
    url = service.resolve_url(short_code)
    if not url:
        logger.warning(f"Shortened URL not found or expired: {short_code}")
        raise HTTPException(status_code=404, detail="Shortened URL not found or expired")
    return RedirectResponse(url.original_url)

