import axios from "axios";

// Base URL of your FastAPI backend
const API_BASE = "http://127.0.0.1:8000";

// Get available stock for a product code
export const getStock = async (code) => {
  try {
    const response = await axios.get(`${API_BASE}/stock/available`, {
      params: { code },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching stock:", error);
    return { status: "error", stock: [] };
  }
};

// Pick stock (decrement inventory)
export const pickStock = async (payload) => {
  try {
    const response = await axios.post(`${API_BASE}/stock/pick`, payload);
    return response.data;
  } catch (error) {
    console.error("Error picking stock:", error);
    return { status: "error" };
  }
};
try { 
const res = await axios.get(`${API_URL}/stock/available?code=${code}`); 
return res.data; 
} catch (err) { 
console.error(err); 
return null; 
} 
}; 
