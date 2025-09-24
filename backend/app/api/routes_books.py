from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from ..domain.models import Book, BookCreate, BookUpdate
from ..services.books_service import BooksService, BookAlreadyExists, BookNotFound

def get_service() -> BooksService:
    from ..main import service  # ใช้ instance global จาก main
    return service

router = APIRouter(prefix="/api/books", tags=["books"])

@router.get("", response_model=List[Book])
def list_books(search: Optional[str] = Query(default=None), svc: BooksService = Depends(get_service)):
    return svc.list_books(search=search)

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: str, svc: BooksService = Depends(get_service)):
    try:
        return svc.get_book(book_id)
    except BookNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("", response_model=Book, status_code=201)
def create_book(payload: BookCreate, svc: BooksService = Depends(get_service)):
    try:
        return svc.create_book(payload)
    except BookAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: str, payload: BookUpdate, svc: BooksService = Depends(get_service)):
    try:
        return svc.update_book(book_id, payload)
    except BookNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BookAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: str, svc: BooksService = Depends(get_service)):
    try:
        svc.delete_book(book_id)
    except BookNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None
