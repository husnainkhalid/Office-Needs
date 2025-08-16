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
      <Routes>
        <Route path="/" element={<Pricing />} />
        <Route path="/purchase-order" element={<PurchaseOrder />} />
        <Route path="/vendor-order" element={<VendorOrder />} />
        <Route path="/packing" element={<Packing />} />
        <Route path="/invoice" element={<Invoice />} />
      </Routes>
    </Router>
  );
}

export default App;
