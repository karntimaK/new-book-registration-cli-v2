import json
import os

file_name = "book.json"

#โหลดข้อมูลหนังสือ ถ้าไม่มีจะเป็นลิสต์ว่างไว้
def load_books():
    if os.path.exists(file_name):
        with open(file_name,"r",encoding="utf-8") as file:
            return json.load(file)
    return []

def main():
    books = load_books()
    print("Welcome to Book Registration!\n")
    while True:
        print("\n" + "-"*20 + " จัดการหนังสือ " + "-"*20)
        print(f"1.เพิ่มหนังสือ\n2.ดูรายการหนังสือ\n3.ลบหนังสือ\n4.ค้นหาหนังสือ\n5.แก้ไขข้อมูลหนังสือ\n6.ผู้จัดทำ\n0.ออก")
        choice = input("กรุณาใส่ตัวเลือก : ")

        if choice == "1":
            print("TODO: add_book")
        elif choice == "2":
            print("TODO: show_book")
        elif choice == "3":
            print("TODO: delete_book")
        elif choice == "4":
            print("TODO: search_book")
        elif choice == "5":
            print("TODO: edit_book")
        elif choice == "6":
            print(f"\nจัดทำโดย\n\n1.นายณัฐพัฒน์ แสนตรี 663380012-6\n2.นางสาวการติมา คำภีร์ 663380199-4")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("\n Invalid command. Please try again.\n")

if __name__ == "__main__":
    main()
