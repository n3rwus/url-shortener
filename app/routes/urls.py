from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.cache import timed_cache
from app.db.database import get_db
from app.shemas.shemas import UrlsResponse

router = APIRouter(tags=["Urls"])

@router.get("/urls", response_model=List[UrlsResponse])
@timed_cache(seconds=300)
async def get_urls(db: Session = Depends(get_db())):
    return None
