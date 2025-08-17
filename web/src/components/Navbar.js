import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={{ background: '#333', padding: '10px' }}>
      <ul style={{ display: 'flex', listStyle: 'none', margin: 0, padding: 0 }}>
        <li style={{ marginRight: '15px' }}>
          <Link to="/" style={{ color: '#fff', textDecoration: 'none' }}>Pricing</Link>
        </li>
        <li style={{ marginRight: '15px' }}>
          <Link to="/purchase-order" style={{ color: '#fff', textDecoration: 'none' }}>Purchase Order</Link>
        </li>
        <li style={{ marginRight: '15px' }}>
          <Link to="/vendor-order" style={{ color: '#fff', textDecoration: 'none' }}>Vendor Order</Link>
        </li>
        <li style={{ marginRight: '15px' }}>
          <Link to="/packing" style={{ color: '#fff', textDecoration: 'none' }}>Packing</Link>
        </li>
        <li>
          <Link to="/invoice" style={{ color: '#fff', textDecoration: 'none' }}>Invoice</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
