import Inventory from './pages/Inventory';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Pricing from './pages/Pricing';
import PurchaseOrder from './pages/PurchaseOrder';
import VendorOrder from './pages/VendorOrder';
import Packing from './pages/Packing';
import Invoice from './pages/Invoice';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container" style={{ padding: '20px' }}>
        <Routes>
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/" element={<Pricing />} />
          <Route path="/purchase-order" element={<PurchaseOrder />} />
          <Route path="/vendor-order" element={<VendorOrder />} />
          <Route path="/packing" element={<Packing />} />
          <Route path="/invoice" element={<Invoice />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
