import React, { useEffect, useState } from 'react'
import { api } from './api/client'
import SearchBar from './components/SearchBar'
import BookForm from './components/BookForm'
import BookList from './components/BookList'

export default function App() {
  const [books, setBooks] = useState([])
  const [search, setSearch] = useState('')
  const [editing, setEditing] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [formKey, setFormKey] = useState(0) // เพิ่ม state สำหรับรีเซ็ตฟอร์ม

  const load = async (q = '') => {
    setLoading(true)
    try {
      const res = await api.get('/api/books', { params: q ? { search: q } : {} })
      setBooks(res.data)
    } catch (e) {
      console.error(e)
      setMessage('โหลดข้อมูลไม่สำเร็จ')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleAdd = async (payload) => {
    setMessage('')
    try {
      await api.post('/api/books', payload)
      setEditing(null)
      setSearch('')
      await load()
      setMessage('เพิ่มหนังสือสำเร็จ')
      setFormKey(k => k + 1) // รีเซ็ตฟอร์มหลังเพิ่มสำเร็จ
    } catch (e) {
      const detail = e?.response?.data?.detail || 'เกิดข้อผิดพลาด'
      setMessage(detail)
    }
  }

  const handleUpdate = async (payload) => {
    setMessage('')
    try {
      await api.put(`/api/books/${editing.id}`, payload)
      setEditing(null)
      await load(search)
      setMessage('แก้ไขหนังสือสำเร็จ')
    } catch (e) {
      const detail = e?.response?.data?.detail || 'เกิดข้อผิดพลาด'
      setMessage(detail)
    }
  }

  const handleDelete = async (b) => {
    if (!confirm(`ต้องการลบ "${b.title}" หรือไม่?`)) return
    try {
      await api.delete(`/api/books/${b.id}`)
      await load(search)
      setMessage('ลบหนังสือสำเร็จ')
    } catch (e) {
      const detail = e?.response?.data?.detail || 'เกิดข้อผิดพลาด'
      setMessage(detail)
    }
  }

  const onSearch = async () => load(search)

  return (
    <div style={{ maxWidth: 800, margin: '20px auto', fontFamily: 'sans-serif' }}>
      <h2>Book Registration</h2>
      {message && <div style={{ marginBottom: 12, color: '#0a6' }}>{message}</div>}

      <SearchBar value={search} onChange={setSearch} onSearch={onSearch} />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div>
          {loading ? <div>กำลังโหลด...</div> : <BookList books={books} onEdit={setEditing} onDelete={handleDelete} />}
        </div>
        <div>
          <BookForm
			  key={formKey}
			  initial={editing}
			  onSubmit={editing ? handleUpdate : handleAdd}
			  onCancel={() => {
				setEditing(null)
				setFormKey(k => k + 1)
			  }}
			/>
        </div>
      </div>
    </div>
  )
}
