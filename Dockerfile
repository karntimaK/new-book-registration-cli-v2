# ใช้ Python 3.12 เป็น base image
FROM python:3.12-slim

# กำหนด working directory ใน container
WORKDIR /app

# คัดลอกไฟล์โค้ดทั้งหมดเข้า container
COPY main.py .
COPY test_unit.py .

# ตั้งค่า default command เมื่อ container รัน
CMD ["python", "main.py"]
