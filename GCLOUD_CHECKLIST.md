# GCLOUD Deployment Checklist for new-book-registration-cli-v2

## 1. ตั้งค่า Google Cloud
- [ ] ติดตั้ง Google Cloud SDK (`gcloud`)  
- [ ] ลงชื่อเข้าใช้งาน: `gcloud auth login`  
- [ ] เลือก project: `gcloud config set project <PROJECT_ID>`  

## 2. สร้าง Container Registry
- [ ] กำหนดชื่อ image: `gcr.io/<PROJECT_ID>/new-book-registration-cli-v2`  
- [ ] build Docker image:  
```bash
docker build -t gcr.io/<PROJECT_ID>/new-book-registration-cli-v2 .
