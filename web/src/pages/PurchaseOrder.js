import React, { useState, useEffect } from 'react';
import axios from 'axios';

function PurchaseOrder() {
  const [quotes, setQuotes] = useState([]);
  const [selectedQuote, setSelectedQuote] = useState(null);

  useEffect(() => {
    // Fetch confirmed quotes from backend
    axios.get('http://localhost:8000/quotes')
      .then(res => setQuotes(res.data.quotes))
      .catch(err => console.error(err));
  }, []);

  const createPO = () => {
    if (!selectedQuote) return alert('Select a quote first!');
    axios.post('http://localhost:8000/po', { quote_id: selectedQuote.quote_id })
      .then(res => alert('PO created: ' + JSON.stringify(res.data)))
      .catch(err => console.error(err));
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Purchase Orders</h2>

      <div>
        <label>Select Quote: </label>
        <select value={selectedQuote?.quote_id || ''} onChange={e => {
          const q = quotes.find(q => q.quote_id === parseInt(e.target.value));
          setSelectedQuote(q);
        }}>
          <option value="">--Select--</option>
          {quotes.map(q => (
            <option key={q.quote_id} value={q.quote_id}>
              {q.client_name} - {q.date}
            </option>
          ))}
        </select>
      </div>

      <button onClick={createPO} style={{ marginTop: '20px' }}>Create PO</button>
    </div>
  );
}

export default PurchaseOrder;
