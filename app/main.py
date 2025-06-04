from fastapi import FastAPI
from app.routes import scraper

app = FastAPI(title="Web Scraper API")

app.include_router(scraper.router)

