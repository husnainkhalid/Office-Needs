import React, { useState } from 'react';
import axios from 'axios';

function Inventory() {
  const [code, setCode] = useState('');
  const [stock, setStock] = useState([]);

  const fetchStock = () => {
    if (!code) return;
    axios.get(`http://localhost:8000/inventory/available?code=${code}`)
      .then(res => setStock(res.data.stock))
      .catch(err => console.error(err));
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Inventory Check</h2>
      <div>
        <input
          type="text"
          placeholder="Enter product code"
          value={code}
          onChange={e => setCode(e.target.value)}
        />
        <button onClick={fetchStock}>Check Stock</button>
      </div>
      <ul>
        {stock.map((s, index) => (
          <li key={index}>{s.box_id}: {s.qty}</li>
        ))}
      </ul>
    </div>
  );
}

export default Inventory;
