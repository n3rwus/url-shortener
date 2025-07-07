from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from fastapi.responses import RedirectResponse
from app.core.cache import timed_cache
from app.db.database import get_db
from app.repositories.url_repository import UrlsRepository
from app.service.url_service import UrlsService
from app.shemas.shemas import UrlsResponse, UrlsCreateRequest

router = APIRouter(tags=["Urls"])

def get_service(db: Session = Depends(get_db)) -> UrlsService:
    return UrlsService(UrlsRepository(db))

@router.post("/urls", response_model=UrlsResponse, status_code=status.HTTP_201_CREATED)
def add_url(url_data: UrlsCreateRequest, service: UrlsService = Depends(get_service)):
    url = service.shorten_url(
        original_url=url_data.original_url,
        valid_until=url_data.valid_until
    )
    return UrlsResponse.model_validate(url)

@router.get("/urls", response_model=List[UrlsResponse])
@timed_cache(seconds=300)
async def get_urls(service: UrlsService = Depends(get_service)):
    urls = await service.get_all_urls()
    return [UrlsResponse.model_validate(url) for url in urls]

@router.get("/urls/{shortened}", response_model=UrlsResponse)
def resolve_url(shortened: str, service: UrlsService = Depends(get_service)):
    url = service.resolve_url(shortened)
    if not url:
        raise HTTPException(status_code=404, detail="Shortened URL not found or expired")
    return UrlsResponse.model_validate(url)

@router.get("/urls/id/{url_id}", response_model=UrlsResponse)
def get_by_id(url_id: uuid.UUID, service: UrlsService = Depends(get_service)):
    url = service.get_url_by_id(url_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return UrlsResponse.model_validate(url)

@router.delete("/urls/{shortened}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(shortened: str, service: UrlsService = Depends(get_service)):
    deleted = service.delete_url(shortened)
    if not deleted:
        raise HTTPException(status_code=404, detail="URL not found or already deleted")

@router.get("/urls/{shortened}/expired", response_model=bool)
def check_expiration(shortened: str, service: UrlsService = Depends(get_service)):
    expired = service.is_url_expired(shortened)
    if expired is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return expired

@router.get("/{short_code}")
def redirect_short_url(short_code: str, service: UrlsService = Depends(get_service)):
    url = service.resolve_url(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="Shortened URL not found or expired")
    return RedirectResponse(url.original_url)

