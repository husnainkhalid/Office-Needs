import React, { useState } from 'react';

function Pricing() {
  const [items, setItems] = useState([
    { id: 1, name: 'Scalpel', price: 12 },
    { id: 2, name: 'Forceps', price: 18 },
  ]);

  return (
    <div>
      <h2>Pricing</h2>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Item</th>
            <th>Price ($)</th>
          </tr>
        </thead>
        <tbody>
          {items.map((i) => (
            <tr key={i.id}>
              <td>{i.name}</td>
              <td>{i.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Pricing;
