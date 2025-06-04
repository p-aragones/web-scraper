from fastapi import APIRouter
from app.services.scraper_service import get_posts
from pydantic import Field
from typing import Annotated

router = APIRouter()

@router.get("/", summary="Get posts from page 1")
@router.get("/{page_number}", summary="Get posts from specified page")
async def scrape_rows(page_number: Annotated[int, Field(ge=1)] = 1):
    return await get_posts(page_number)