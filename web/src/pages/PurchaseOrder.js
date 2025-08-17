import React, { useState } from 'react';

function PurchaseOrder() {
  const [order, setOrder] = useState({ item: '', qty: 1 });
  const [orders, setOrders] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setOrders([...orders, order]);
    setOrder({ item: '', qty: 1 });
  };

  return (
    <div>
      <h2>Purchase Order</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Item name"
          value={order.item}
          onChange={(e) => setOrder({ ...order, item: e.target.value })}
        />
        <input
          type="number"
          min="1"
          value={order.qty}
          onChange={(e) => setOrder({ ...order, qty: e.target.value })}
        />
        <button type="submit">Add</button>
      </form>

      <h3>Orders</h3>
      <ul>
        {orders.map((o, idx) => (
          <li key={idx}>{o.qty} × {o.item}</li>
        ))}
      </ul>
    </div>
  );
}

export default PurchaseOrder;
