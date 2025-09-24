from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .infra.repositories.json_repository import JsonBookRepository
from .services.books_service import BooksService
from .api.routes_books import router as books_router

# สร้าง instance เดียวไว้ใช้ทั้งแอป
repo = JsonBookRepository(settings.DATA_PATH)
service = BooksService(repo)

app = FastAPI(title="Book Registration API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ALLOW_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

app.include_router(books_router)
