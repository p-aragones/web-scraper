from fastapi import APIRouter
from app.services.scraper_service import get_posts

router = APIRouter()

@router.get("/", summary="Get posts from page 1")
async def scrape_rows_default():
    return await get_posts(1)

@router.get("/{page_number}", summary="Get posts from specified page")
async def scrape_rows(page_number: int):
    return await get_posts(page_number)