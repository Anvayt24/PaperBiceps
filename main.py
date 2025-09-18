from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from app.routes import podcast, explain, health

app = FastAPI(
    title="PaperBiceps",
    description="Backend API for the PaperBiceps Chrome extension",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(podcast.router)
app.include_router(explain.router)
