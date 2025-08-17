import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000', // your backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Optional: add interceptors for logging or error handling
API.interceptors.response.use(
  response => response,
  error => {
    console.error('API error:', error.response || error.message);
    return Promise.reject(error);
  }
);

export default API;
