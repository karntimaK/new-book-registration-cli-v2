import React, { useState, useEffect } from 'react'

export default function BookForm({ initial, onSubmit, onCancel }) {
  const [title, setTitle] = useState(initial?.title || '')
  const [author, setAuthor] = useState(initial?.author || '')
  const [isbn, setIsbn] = useState(initial?.isbn || '')
  const [error, setError] = useState('')

  useEffect(() => {
    setTitle(initial?.title || '')
    setAuthor(initial?.author || '')
    setIsbn(initial?.isbn || '')
  }, [initial])

  const handleSubmit = (e) => {
    e.preventDefault()
    setError('')
    if (!title.trim()) return setError('กรุณาใส่ชื่อหนังสือ')
    if (!author.trim()) return setError('กรุณาใส่ชื่อผู้แต่ง')

    const isbnTrim = isbn.trim()
    if (!/^\d+$/.test(isbnTrim)) return setError('ISBN ต้องเป็นตัวเลขเท่านั้น')
    if (isbnTrim.length !== 13) return setError('ISBN ต้องมี 13 หลัก')

    onSubmit({ title: title.trim(), author: author.trim(), isbn: isbnTrim })
  }

  return (
    <form onSubmit={handleSubmit} style={{ border: '1px solid #ddd', padding: 12, borderRadius: 8 }}>
      <h3>{initial ? 'แก้ไขหนังสือ' : 'เพิ่มหนังสือ'}</h3>
      {error && <div style={{ color: 'red', marginBottom: 8 }}>{error}</div>}
      <div style={{ marginBottom: 8 }}>
        <label>ชื่อหนังสือ: </label>
        <input value={title} onChange={(e) => setTitle(e.target.value)} style={{ padding: 6, width: 280 }}/>
      </div>
      <div style={{ marginBottom: 8 }}>
        <label>ผู้แต่ง: </label>
        <input value={author} onChange={(e) => setAuthor(e.target.value)} style={{ padding: 6, width: 280 }}/>
      </div>
      <div style={{ marginBottom: 8 }}>
        <label>ISBN: </label>
        <input value={isbn} onChange={(e) => setIsbn(e.target.value)} style={{ padding: 6, width: 280 }}/>
      </div>
      <div>
        <button type="submit" style={{ padding: '6px 12px' }}>{initial ? 'บันทึก' : 'เพิ่ม'}</button>
        {onCancel && <button type="button" onClick={onCancel} style={{ padding: '6px 12px', marginLeft: 8 }}>ยกเลิก</button>}
      </div><br />
      <details>
      <summary>ผู้จัดทำ</summary>
        <p>นายณัฐพัฒน์ แสนตรี 663380012-6</p>
        <p>นางสาวการติมา คำภีร์ 663380199-4</p>
      </details>
    </form>
  )
}
