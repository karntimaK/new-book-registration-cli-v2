import json
import os
import builtins
import pytest
import book_manager as bm

@pytest.fixture
def book_file(tmp_path, monkeypatch):
    path = tmp_path / "test_book.json"
    monkeypatch.setattr(bm, "file_name", str(path))
    return path

def set_inputs(monkeypatch, inputs, echo=False):
    it = iter(inputs)
    def fake_input(prompt=""):
        try:
            val = next(it)
        except StopIteration:
            raise AssertionError("No more test inputs provided") from None
        if echo:
            print(f"[TEST INPUT] {prompt}{val}")
        return val
    monkeypatch.setattr(builtins, "input", fake_input)

# ---------- load/save ----------
def test_load_books_when_file_missing(book_file):
    assert not os.path.exists(book_file)
    assert bm.load_books() == []

def test_load_books_when_file_exists(book_file):
    data = [{"title": "A", "author": "B", "isbn": "1234567890123"}]
    book_file.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")
    assert bm.load_books() == data

def test_save_writes_json(book_file):
    data = [{"title": "ภาษาไทย", "author": "ผู้เขียน", "isbn": "0000000000000"}]
    bm.save(data)
    content = book_file.read_text(encoding="utf-8")
    assert json.loads(content) == data
    assert "ภาษาไทย" in content

# ---------- add_book ----------
def test_add_book_happy_path(book_file, monkeypatch):
    books = []
    set_inputs(monkeypatch, ["Python 101", "Guido", "1234567890123"])
    bm.add_book(books)
    assert len(books) == 1
    assert books[0] == {"title": "Python 101","author": "Guido","isbn": "1234567890123"}
    saved = json.loads(book_file.read_text(encoding="utf-8"))
    assert saved == books

def test_add_book_validation_loops(book_file, monkeypatch, capsys):
    books = []
    set_inputs(monkeypatch, ["", "  ", "Book", "", "Author", "", "abc", "123", "0000000000000"])
    bm.add_book(books)
    out = capsys.readouterr().out
    assert "ไม่มีชื่อหนังสือ กรุณาใส่ชื่อหนังสือ" in out
    assert "กรุณาใส่ชื่อผู้เขียน" in out
    assert "ISBN ต้องเป็นตัวเลขเท่านั้น" in out
    assert "ISBN ต้องมี 13 หลัก" in out
    assert books[0] == {"title": "Book","author": "Author","isbn": "0000000000000"}

def test_add_book_duplicate_title_author(book_file, monkeypatch, capsys):
    books = [{"title": "Same", "author": "Person", "isbn": "1111111111111"}]
    set_inputs(monkeypatch, ["Same", "Person", "9999999999999"])
    bm.add_book(books)
    out = capsys.readouterr().out
    assert "มีอยู่แล้วในระบบ" in out
    assert len(books) == 1
    assert not os.path.exists(book_file)

def test_add_book_duplicate_isbn(book_file, monkeypatch, capsys):
    books = [{"title": "Old", "author": "Auth", "isbn": "2222222222222"}]
    set_inputs(monkeypatch, ["New", "Writer", "2222222222222"])
    bm.add_book(books)
    out = capsys.readouterr().out
    assert "มีอยู่แล้วในระบบ" in out
    assert len(books) == 1
    assert not os.path.exists(book_file)

# ---------- show_books ----------
def test_show_books_empty(capsys):
    bm.show_books([])
    out = capsys.readouterr().out
    assert "Book registration list is empty." in out

def test_show_books_list(capsys):
    books = [
        {"title": "T1", "author": "A1", "isbn": "1111111111111"},
        {"title": "T2", "author": "A2", "isbn": "2222222222222"},
    ]
    bm.show_books(books)
    out = capsys.readouterr().out
    assert "รายการหนังสือทั้งหมด" in out
    assert "1. ชื่อหนังสือ : T1" in out
    assert "2. ชื่อหนังสือ : T2" in out

# ---------- delete_book ----------
def test_delete_book_empty(capsys):
    bm.delete_book([])
    out = capsys.readouterr().out
    assert "Book registration list is empty" in out
    assert "ไม่สามารถลบได้" in out

def test_delete_book_by_title(book_file, monkeypatch, capsys):
    books = [
        {"title": "T1", "author": "A1", "isbn": "1111111111111"},
        {"title": "T2", "author": "A2", "isbn": "2222222222222"},
    ]
    set_inputs(monkeypatch, ["T2"])
    bm.delete_book(books)
    out = capsys.readouterr().out
    assert "ลบหนังสือ T2 สำเร็จ" in out
    assert len(books) == 1 and books[0]["title"] == "T1"
    saved = json.loads(book_file.read_text(encoding="utf-8"))
    assert saved == books

def test_delete_book_by_isbn(book_file, monkeypatch, capsys):
    books = [
        {"title": "T1", "author": "A1", "isbn": "1111111111111"},
        {"title": "T2", "author": "A2", "isbn": "2222222222222"},
    ]
    set_inputs(monkeypatch, ["1111111111111"])
    bm.delete_book(books)
    out = capsys.readouterr().out
    assert "ลบหนังสือ T1 สำเร็จ" in out
    assert len(books) == 1 and books[0]["title"] == "T2"

def test_delete_book_not_found(book_file, monkeypatch, capsys):
    books = [{"title": "T1", "author": "A1", "isbn": "1111111111111"}]
    set_inputs(monkeypatch, ["Nope"])
    bm.delete_book(books)
    out = capsys.readouterr().out
    assert "ไม่พบบันทึกหนังสือตามที่ระบุ" in out
    assert books == [{"title": "T1", "author": "A1", "isbn": "1111111111111"}]

# ---------- search_book ----------
def test_search_book_empty(capsys):
    bm.search_book([])
    out = capsys.readouterr().out
    assert "Book registration list is empty." in out

def test_search_book_by_title(monkeypatch, capsys):
    books = [
        {"title": "Python 101", "author": "Guido", "isbn": "1234567890123"},
        {"title": "Java Basics", "author": "James", "isbn": "9876543210987"},
    ]
    set_inputs(monkeypatch, ["py"])
    bm.search_book(books)
    out = capsys.readouterr().out
    assert "ผลการค้นหา" in out
    assert "Python 101" in out
    assert "Java Basics" not in out

def test_search_book_by_author(monkeypatch, capsys):
    books = [
        {"title": "C Programming", "author": "Dennis", "isbn": "1111111111111"},
        {"title": "Go in Action", "author": "Rob Pike", "isbn": "2222222222222"},
    ]
    set_inputs(monkeypatch, ["pike"])
    bm.search_book(books)
    out = capsys.readouterr().out
    assert "Go in Action" in out
    assert "C Programming" not in out

def test_search_book_not_found(monkeypatch, capsys):
    books = [{"title": "C Programming", "author": "Dennis", "isbn": "1111111111111"}]
    set_inputs(monkeypatch, ["zzz"])
    bm.search_book(books)
    out = capsys.readouterr().out
    assert "ไม่พบหนังสือตามคำค้นหา" in out

# ---------- edit_book ----------
def test_edit_book_empty(capsys):
    bm.edit_book([])
    out = capsys.readouterr().out
    assert "Book registration list is empty." in out

def test_edit_book_update_title_only(book_file, monkeypatch, capsys):
    books = [{"title": "OldTitle", "author": "Auth", "isbn": "1111111111111"}]
    set_inputs(monkeypatch, ["OldTitle", "NewTitle", "", ""])
    bm.edit_book(books)
    out = capsys.readouterr().out
    assert "แก้ไขข้อมูลเสร็จสิ้น" in out
    assert books[0]["title"] == "NewTitle"
    assert books[0]["author"] == "Auth"
    assert books[0]["isbn"] == "1111111111111"
    saved = json.loads(book_file.read_text(encoding="utf-8"))
    assert saved == books

def test_edit_book_update_valid_isbn(book_file, monkeypatch):
    books = [{"title": "Book", "author": "A", "isbn": "1111111111111"}]
    set_inputs(monkeypatch, ["Book", "", "NewAuth", "3333333333333"])
    bm.edit_book(books)
    assert books[0] == {"title": "Book", "author": "NewAuth", "isbn": "3333333333333"}

def test_edit_book_invalid_isbn_should_not_change(monkeypatch):
    books = [{"title": "Book", "author": "A", "isbn": "1111111111111"}]
    set_inputs(monkeypatch, ["Book", "", "", "abc"])
    bm.edit_book(books)
    assert books[0]["isbn"] == "1111111111111"

def test_edit_book_not_found(monkeypatch, capsys):
    books = [{"title": "Book", "author": "A", "isbn": "1111111111111"}]
    set_inputs(monkeypatch, ["NoMatch"])
    bm.edit_book(books)
    out = capsys.readouterr().out
    assert "ไม่พบบันทึกหนังสือตามที่ระบุ" in out

# ---------- main ----------
def test_main_exit(book_file, monkeypatch, capsys):
    set_inputs(monkeypatch, ["0"])
    bm.main()
    out = capsys.readouterr().out
    assert "Welcome to Book Registration!" in out
    assert "Goodbye!" in out
