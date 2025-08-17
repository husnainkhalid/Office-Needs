import React, { useState } from 'react';

function Invoice() {
  const [invoices, setInvoices] = useState([]);
  const [form, setForm] = useState({ customer: '', amount: '' });

  const handleSubmit = (e) => {
    e.preventDefault();
    setInvoices([...invoices, form]);
    setForm({ customer: '', amount: '' });
  };

  return (
    <div>
      <h2>Invoice</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Customer"
          value={form.customer}
          onChange={(e) => setForm({ ...form, customer: e.target.value })}
        />
        <input
          type="number"
          placeholder="Amount"
          value={form.amount}
          onChange={(e) => setForm({ ...form, amount: e.target.value })}
        />
        <button type="submit">Add Invoice</button>
      </form>

      <h3>Invoices</h3>
      <ul>
        {invoices.map((inv, idx) => (
          <li key={idx}>{inv.customer} - ${inv.amount}</li>
        ))}
      </ul>
    </div>
  );
}

export default Invoice;
