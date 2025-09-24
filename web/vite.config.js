import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// ถ้าต้องการ proxy /api ไป backend ใน dev mode ให้ปลดคอมเมนต์
// server: { proxy: { '/api': 'http://localhost:8000' } }

export default defineConfig({
  plugins: [react()]
})
