import React from 'react'

export default function SearchBar({ value, onChange, onSearch }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="ค้นหาด้วยชื่อหนังสือหรือผู้แต่ง"
        style={{ padding: 8, width: 280 }}
      />
      <button onClick={onSearch} style={{ marginLeft: 8, padding: '8px 12px' }}>ค้นหา</button>
    </div>
  )
}
