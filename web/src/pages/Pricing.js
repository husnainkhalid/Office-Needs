import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Pricing() {
  const [clients, setClients] = useState([]);
  const [selectedClient, setSelectedClient] = useState('');
  const [products, setProducts] = useState([]);
  const [selectedProducts, setSelectedProducts] = useState([]);

  useEffect(() => {
    // Fetch client list from backend
    axios.get('http://localhost:8000/clients')
      .then(res => setClients(res.data.clients))
      .catch(err => console.error(err));
  }, []);

  const handleProductSelect = (code, qty) => {
    setSelectedProducts(prev => [...prev, { code, qty }]);
  };

  const generatePricing = () => {
    axios.post('http://localhost:8000/price', {
      client_id: selectedClient,
      products: selectedProducts
    })
    .then(res => alert('Pricing generated: ' + JSON.stringify(res.data)))
    .catch(err => console.error(err));
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Pricing</h2>

      <div>
        <label>Client: </label>
        <select value={selectedClient} onChange={e => setSelectedClient(e.target.value)}>
          <option value="">Select Client</option>
          {clients.map(c => <option key={c.client_id} value={c.client_id}>{c.name}</option>)}
        </select>
      </div>

      <div style={{ marginTop: '20px' }}>
        <label>Products (dummy input for now): </label>
        <input type="text" placeholder="Enter code:qty, comma separated" onBlur={e => {
          const list = e.target.value.split(',').map(s => {
            const [code, qty] = s.split(':');
            return { code: code.trim(), qty: parseInt(qty) };
          });
          setSelectedProducts(list);
        }} />
      </div>

      <button onClick={generatePricing} style={{ marginTop: '20px' }}>Generate Pricing</button>
    </div>
  );
}

export default Pricing;
