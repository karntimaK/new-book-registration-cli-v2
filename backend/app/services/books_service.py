from __future__ import annotations
from typing import List, Optional
from ..domain.models import Book, BookCreate, BookUpdate
from ..infra.repositories.json_repository import JsonBookRepository

class BookAlreadyExists(Exception):
    pass

class BookNotFound(Exception):
    pass

class BooksService:
    def __init__(self, repo: JsonBookRepository):
        self.repo = repo

    def list_books(self, search: Optional[str] = None) -> List[Book]:
        return [Book(**b) for b in self.repo.list(search=search)]

    def get_book(self, book_id: str) -> Book:
        b = self.repo.get(book_id)
        if not b:
            raise BookNotFound("ไม่พบบันทึกหนังสือตามที่ระบุ")
        return Book(**b)

    def create_book(self, data: BookCreate) -> Book:
        # เช็คซ้ำด้วย (title, author) หรือ ISBN
        if self.repo.exists_by_title_author(data.title, data.author):
            raise BookAlreadyExists("หนังสือเล่มนี้มีอยู่แล้วในระบบ (ซ้ำชื่อและผู้แต่ง)")
        if self.repo.find_by_isbn(data.isbn):
            raise BookAlreadyExists("หนังสือเล่มนี้มีอยู่แล้วในระบบ (ซ้ำ ISBN)")
        book = Book(**data.model_dump())
        self.repo.add(book.model_dump())
        return book

    def update_book(self, book_id: str, patch: BookUpdate) -> Book:
        # หาเล่มเดิมก่อน
        existing = self.repo.get(book_id)
        if not existing:
            raise BookNotFound("ไม่พบบันทึกหนังสือตามที่ระบุ")
        # ถ้าจะเปลี่ยนเป็นชื่อ/ผู้แต่งใหม่ ตรวจซ้ำ
        new_title = patch.title if patch.title is not None else existing["title"]
        new_author = patch.author if patch.author is not None else existing["author"]
        new_isbn = patch.isbn if patch.isbn is not None else existing["isbn"]

        # ถ้าชื่อ-ผู้แต่งเปลี่ยน แต่อาจชนกับเล่มอื่น
        if (new_title != existing["title"] or new_author != existing["author"]):
            # วิธีเร็ว: ลิสต์ทั้งหมดแล้วเช็ค (ยกเว้นเล่มนี้)
            for b in self.repo.list():
                if b["id"] != book_id and b["title"] == new_title and b["author"] == new_author:
                    raise BookAlreadyExists("ชื่อและผู้แต่งนี้ถูกใช้แล้ว")
        # เช็ค ISBN ซ้ำกับเล่มอื่น
        for b in self.repo.list():
            if b["id"] != book_id and b["isbn"] == new_isbn:
                raise BookAlreadyExists("ISBN นี้ถูกใช้แล้ว")

        updated = self.repo.update(book_id, patch.model_dump())
        if not updated:
            raise BookNotFound("ไม่พบบันทึกหนังสือตามที่ระบุ")
        return Book(**updated)

    def delete_book(self, book_id: str) -> None:
        ok = self.repo.delete(book_id)
        if not ok:
            raise BookNotFound("ไม่พบบันทึกหนังสือตามที่ระบุ")
