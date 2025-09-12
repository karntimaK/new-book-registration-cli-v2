import json
import os

file_name = "book.json"

#โหลดข้อมูลหนังสือ ถ้าไม่มีจะเป็นลิสต์ว่างไว้
def load_books():
    if os.path.exists(file_name):
        with open(file_name,"r",encoding="utf-8") as file:
            return json.load(file)
    return []

#บันทึกหนังสือ
def save(books):
    with open(file_name,"w",encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)

#เพิ่มฟังก์ชั่น เพิ่มหนังสือ
def add_book(books):
    title = ""
    author = ""
    while not title:
        title = input("กรุณาใส่ชื่อหนังสือ : ").strip()
        if not title:
            print("ไม่มีชื่อหนังสือ กรุณาใส่ชื่อหนังสือ")


    while not author:
        author = input("กรุณาใส่ชื่อผู้เขียน : ").strip()
        if not author:
            print("ไม่มีชื่อหนังสือ กรุณาใส่ชื่อผู้เขียน")

    for book in books:
        if book['title'] == title and book['author'] == author:
            print("\n!!หนังสือเล่มนี้มีอยู่แล้วในระบบ!!\n")
            return

    books.append({"title" : title, "author" : author})
    save(books)
    print(f"\n!!เพิ่มหนังสือเสร็จสิ้น ({title})!!\n")

def main():
    books = load_books()
    print("Welcome to Book Registration!\n")
    while True:
        print("\n" + "-"*20 + " จัดการหนังสือ " + "-"*20)
        print(f"1.เพิ่มหนังสือ\n2.ดูรายการหนังสือ\n3.ลบหนังสือ\n4.ค้นหาหนังสือ\n5.แก้ไขข้อมูลหนังสือ\n6.ผู้จัดทำ\n0.ออก")
        choice = input("กรุณาใส่ตัวเลือก : ")

        if choice == "1":
           add_book(books)
        elif choice == "2":
            print("TODO: show_book")
        elif choice == "3":
            print("TODO: delete_book")
        elif choice == "4":
            print("TODO: search_book")
        elif choice == "5":
            print("TODO: edit_book")
        elif choice == "6":
            print(f"\nจัดทำโดย\n\n1.นายณัฐพัฒน์ แสนตรี 663380012-6 (Coder)\n2.นางสาวการติมา คำภีร์ 663380199-4 (Planner)")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("\nตัวเลือกผิดพลาด กรุณาใส่ตัวเลือกที่มีอยู่\n")

if __name__ == "__main__":
    main()
