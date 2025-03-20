import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',  // your Django backend URL
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true,
  timeout: 5000 // Add a timeout to better handle connection issues
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    throw error;
  }
);

export default api; 