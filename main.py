import json
import os

file_name = "book.json"

# โหลดข้อมูลหนังสือ ถ้าไม่มีจะเป็นลิสต์ว่างไว้
def load_books():
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# บันทึกหนังสือ
def save(books):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)

# เพิ่มฟังก์ชั่น เพิ่มหนังสือ
def add_book(books):
    title = ""
    author = ""
    isbn = ""
    while not title:
        title = input("กรุณาใส่ชื่อหนังสือ : ").strip()
        if not title:
            print("ไม่มีชื่อหนังสือ กรุณาใส่ชื่อหนังสือ")

    while not author:
        author = input("กรุณาใส่ชื่อผู้เขียน : ").strip()
        if not author:
            print("ไม่มีชื่อหนังสือ กรุณาใส่ชื่อผู้เขียน")

    while len(isbn) != 13:
        isbn = input("กรุณาใส่เลขมาตรฐานสากลประจำหนังสือ : ").strip()
        if not isbn:
            print("ไม่มีเลขมาตรฐานสากลประจำหนังสือ กรุณาใส่ข้อมูล")
        elif not isbn.isdigit():
            print("ISBN ต้องเป็นตัวเลขเท่านั้น")
        else:
            print("ISBN ต้องมี 13 หลัก")

    for book in books:
        if book['title'] == title and book['author'] == author:
            print("\n!!หนังสือเล่มนี้มีอยู่แล้วในระบบ!!\n")
            return
        elif book['isbn'] == isbn:
            print("\n!!หนังสือเล่มนี้มีอยู่แล้วในระบบ!!\n")
            return

    books.append({"title": title, "author": author, "isbn": isbn})
    save(books)
    print(f"\n!!เพิ่มหนังสือเสร็จสิ้น ({title})!!\n")

# ฟังก์ชันแสดงรายการหนังสือ
def show_books(books):
    if not books:
        print("\nBook registration list is empty.\n")
        return

    print("\nรายการหนังสือทั้งหมด\n")
    for index, book in enumerate(books, start=1):
        print(f"{index}. ชื่อหนังสือ : {book['title']}")
        print(f"   ผู้แต่ง     : {book['author']}")
        print(f"   ISBN       : {book['isbn']}\n")

# ฟังก์ชันลบหนังสือ
def delete_book(books):
    if not books:
        print("\nBook registration list is empty. ไม่สามารถลบได้\n")
        return
    
    keyword = input("กรอกชื่อหนังสือหรือ ISBN ที่ต้องการลบ : ").strip()
    for book in books:
        if book['title'] == keyword or book['isbn'] == keyword:
            books.remove(book)
            save(books)
            print(f"\n!!ลบหนังสือ {book['title']} สำเร็จ!!\n")
            return
    print("\n!!ไม่พบบันทึกหนังสือตามที่ระบุ!!\n")

# ฟังก์ชันค้นหาหนังสือ
def search_book(books):
    if not books:
        print("\nBook registration list is empty.\n")
        return

    keyword = input("กรอกชื่อหนังสือหรือชื่อผู้แต่งเพื่อค้นหา : ").strip().lower()
    results = [book for book in books if keyword in book['title'].lower() or keyword in book['author'].lower()]
    
    if results:
        print("\nผลการค้นหา:\n")
        for index, book in enumerate(results, start=1):
            print(f"{index}. ชื่อหนังสือ : {book['title']}")
            print(f"   ผู้แต่ง     : {book['author']}")
            print(f"   ISBN       : {book['isbn']}\n")
    else:
        print("\n!!ไม่พบหนังสือตามคำค้นหา!!\n")

# ฟังก์ชันแก้ไขข้อมูลหนังสือ
def edit_book(books):
    if not books:
        print("\nBook registration list is empty.\n")
        return

    keyword = input("กรอกชื่อหนังสือหรือ ISBN ที่ต้องการแก้ไข : ").strip()
    for book in books:
        if book['title'] == keyword or book['isbn'] == keyword:
            print(f"\nแก้ไขข้อมูลหนังสือ: {book['title']}\n")
            new_title = input("ชื่อหนังสือใหม่ (เว้นว่างถ้าไม่แก้ไข): ").strip()
            new_author = input("ผู้แต่งใหม่ (เว้นว่างถ้าไม่แก้ไข): ").strip()
            new_isbn = input("ISBN ใหม่ (13 หลัก, เว้นว่างถ้าไม่แก้ไข): ").strip()

            if new_title: book['title'] = new_title
            if new_author: book['author'] = new_author
            if new_isbn and len(new_isbn) == 13 and new_isbn.isdigit():
                book['isbn'] = new_isbn

            save(books)
            print("\n!!แก้ไขข้อมูลเสร็จสิ้น!!\n")
            return
    print("\n!!ไม่พบบันทึกหนังสือตามที่ระบุ!!\n")

def main():
    books = load_books()
    print("Welcome to Book Registration!\n")
    while True:
        print("\n" + "-" * 20 + " จัดการหนังสือ " + "-" * 20)
        print("1.เพิ่มหนังสือ\n2.ดูรายการหนังสือ\n3.ลบหนังสือ\n4.ค้นหาหนังสือ\n5.แก้ไขข้อมูลหนังสือ\n6.ผู้จัดทำ\n0.ออก")
        choice = input("กรุณาใส่ตัวเลือก : ")

        if choice == "1":
            add_book(books)
        elif choice == "2":
            show_books(books)
        elif choice == "3":
            delete_book(books)
        elif choice == "4":
            search_book(books)
        elif choice == "5":
            edit_book(books)
        elif choice == "6":
            print("\nจัดทำโดย\n\n1.นายณัฐพัฒน์ แสนตรี 663380012-6 (Coder)\n2.นางสาวการติมา คำภีร์ 663380199-4 (Planner)")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("\nตัวเลือกผิดพลาด กรุณาใส่ตัวเลือกที่มีอยู่\n")

if __name__ == "__main__":
    main()
