import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import Layout from './components/Layout';
import Dashboard from './views/Dashboard';
import Listings from './views/Listings';
import Sync from './views/Sync';
import Auth from './views/Auth';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }

    // Set up axios interceptor for token refresh
    axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            const response = await axios.post('http://localhost:8000/api/token/refresh/', {
              refresh: refreshToken
            });
            localStorage.setItem('access_token', response.data.access);
            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
            return axios(originalRequest);
          } catch (err) {
            // If refresh fails, logout the user
            handleLogout();
          }
        }
        return Promise.reject(error);
      }
    );
  }, []);

  const handleAuth = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };
  return (
    <Router>
      <Routes>
        <Route path="/login" element={user ? <Navigate to="/" replace /> : <Auth onAuth={handleAuth} />} />

        <Route element={<ProtectedRoute user={user} />}>
          <Route element={<Layout onLogout={handleLogout} />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/listings" element={<Listings />} />
            <Route path="/sync" element={<Sync />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
