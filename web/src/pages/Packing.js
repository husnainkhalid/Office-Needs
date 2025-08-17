import React, { useState } from 'react';

function Packing() {
  const [packs, setPacks] = useState([]);
  const [item, setItem] = useState('');

  const addPack = () => {
    if (item.trim() !== '') {
      setPacks([...packs, item]);
      setItem('');
    }
  };

  return (
    <div>
      <h2>Packing</h2>
      <input
        type="text"
        placeholder="Item for packing"
        value={item}
        onChange={(e) => setItem(e.target.value)}
      />
      <button onClick={addPack}>Add</button>

      <h3>Packed Items</h3>
      <ul>
        {packs.map((p, i) => (
          <li key={i}>{p}</li>
        ))}
      </ul>
    </div>
  );
}

export default Packing;
