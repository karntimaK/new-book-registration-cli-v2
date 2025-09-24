import axios from 'axios'

// ตั้งค่า base URL จาก ENV ถ้าไม่ตั้งจะใช้ http://localhost:8000
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' }
})
