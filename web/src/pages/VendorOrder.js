import React, { useState } from 'react';

function VendorOrder() {
  const [vendor, setVendor] = useState('');
  const [details, setDetails] = useState([]);

  const handleAdd = () => {
    if (vendor.trim() !== '') {
      setDetails([...details, vendor]);
      setVendor('');
    }
  };

  return (
    <div>
      <h2>Vendor Order</h2>
      <input
        type="text"
        placeholder="Vendor Name"
        value={vendor}
        onChange={(e) => setVendor(e.target.value)}
      />
      <button onClick={handleAdd}>Add</button>

      <h3>Vendors</h3>
      <ul>
        {details.map((v, i) => (
          <li key={i}>{v}</li>
        ))}
      </ul>
    </div>
  );
}

export default VendorOrder;
