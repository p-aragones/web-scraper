from fastapi import FastAPI
from app.routes import scraper
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Web Scraper API")

# Allow requests from your frontend origin
origins = [
    "http://localhost:8080",  # React/Next.js dev server
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins (not safe for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scraper.router)

