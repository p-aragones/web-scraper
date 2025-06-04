from fastapi import APIRouter
from app.services.scraper_service import get_posts

router = APIRouter()

@router.get("/")
def scrape_rows():
    return get_posts()
