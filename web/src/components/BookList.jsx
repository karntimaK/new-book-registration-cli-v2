import React from 'react'

export default function BookList({ books, onEdit, onDelete }) {
  if (!books.length) return <div>ยังไม่มีรายการหนังสือ</div>

  return (
    <div>
      {books.map((b, idx) => (
        <div key={b.id} style={{ borderBottom: '1px solid #eee', padding: '8px 0' }}>
          <div><strong>{idx + 1}. {b.title}</strong></div>
          <div>ผู้แต่ง: {b.author}</div>
          <div>ISBN: {b.isbn}</div>
          <div style={{ marginTop: 6 }}>
            <button onClick={() => onEdit(b)} style={{ padding: '4px 10px' }}>แก้ไข</button>
            <button onClick={() => onDelete(b)} style={{ padding: '4px 10px', marginLeft: 8, color: 'white', background: 'crimson', border: 'none' }}>ลบ</button>
          </div>
        </div>
      ))}
    </div>
  )
}
