from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
from filelock import FileLock

class JsonBookRepository:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_path.exists():
            self.data_path.write_text("[]", encoding="utf-8")
        # สร้างไฟล์ lock คู่กัน เช่น books.json.lock
        self.lock = FileLock(str(self.data_path) + ".lock")

    def _read_all(self) -> List[Dict[str, Any]]:
        # ล็อกอ่านเพื่อกันชนระหว่างเขียน
        with self.lock:
            text = self.data_path.read_text(encoding="utf-8").strip()
            if not text:
                return []
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                # ถ้าไฟล์เสีย ให้ถือว่าเป็นลิสต์ว่าง
                data = []
            return data

    def _write_all(self, items: List[Dict[str, Any]]) -> None:
        with self.lock:
            self.data_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    def list(self, search: Optional[str] = None) -> List[Dict[str, Any]]:
        items = self._read_all()
        if not search:
            return items
        s = search.lower()
        return [b for b in items if s in b.get("title", "").lower() or s in b.get("author", "").lower()]

    def get(self, book_id: str) -> Optional[Dict[str, Any]]:
        items = self._read_all()
        for b in items:
            if b.get("id") == book_id:
                return b
        return None

    def find_by_isbn(self, isbn: str) -> Optional[Dict[str, Any]]:
        items = self._read_all()
        for b in items:
            if b.get("isbn") == isbn:
                return b
        return None

    def exists_by_title_author(self, title: str, author: str) -> bool:
        items = self._read_all()
        for b in items:
            if b.get("title") == title and b.get("author") == author:
                return True
        return False

    def add(self, book: Dict[str, Any]) -> Dict[str, Any]:
        items = self._read_all()
        items.append(book)
        self._write_all(items)
        return book

    def update(self, book_id: str, patch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        items = self._read_all()
        updated = None
        for idx, b in enumerate(items):
            if b.get("id") == book_id:
                b.update({k: v for k, v in patch.items() if v is not None})
                items[idx] = b
                updated = b
                break
        if updated is not None:
            self._write_all(items)
        return updated

    def delete(self, book_id: str) -> bool:
        items = self._read_all()
        new_items = [b for b in items if b.get("id") != book_id]
        if len(new_items) == len(items):
            return False
        self._write_all(new_items)
        return True
