import React, { createContext, useState } from 'react';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [selectedClient, setSelectedClient] = useState('');
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [purchaseOrders, setPurchaseOrders] = useState([]);
  const [vendorOrders, setVendorOrders] = useState([]);
  const [packingBoxes, setPackingBoxes] = useState([]);
  const [invoices, setInvoices] = useState([]);

  return (
    <AppContext.Provider value={{
      selectedClient,
      setSelectedClient,
      selectedProducts,
      setSelectedProducts,
      purchaseOrders,
      setPurchaseOrders,
      vendorOrders,
      setVendorOrders,
      packingBoxes,
      setPackingBoxes,
      invoices,
      setInvoices
    }}>
      {children}
    </AppContext.Provider>
  );
};
