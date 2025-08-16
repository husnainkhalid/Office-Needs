import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // optional for styling

function Navbar() {
  return (
    <nav style={{ padding: '10px', backgroundColor: '#282c34', color: '#fff' }}>
      <Link to="/" style={{ margin: '0 15px', color: '#61dafb' }}>Pricing</Link>
      <Link to="/purchase-order" style={{ margin: '0 15px', color: '#61dafb' }}>Purchase Order</Link>
      <Link to="/vendor-order" style={{ margin: '0 15px', color: '#61dafb' }}>Vendor Order</Link>
      <Link to="/packing" style={{ margin: '0 15px', color: '#61dafb' }}>Packing</Link>
      <Link to="/invoice" style={{ margin: '0 15px', color: '#61dafb' }}>Invoice</Link>
    </nav>
  );
}

export default Navbar;
