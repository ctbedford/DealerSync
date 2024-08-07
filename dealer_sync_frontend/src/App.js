import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store/store';
import axios from 'axios';
import Layout from './components/Layout';
import Dashboard from './views/Dashboard';
import Listings from './views/Listings';
import Sync from './views/Sync';
import Auth from './views/Auth';
import ProtectedRoute from './components/ProtectedRoute';

axios.defaults.baseURL = 'http://localhost:8000';
axios.defaults.withCredentials = true;

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const checkUserSession = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          const response = await axios.get('/api/auth/user/');
          setUser(response.data);
        } catch (error) {
          console.error('Failed to fetch user session:', error);
          // Clear invalid token
          localStorage.removeItem('access_token');
          delete axios.defaults.headers.common['Authorization'];
        }
      }
    };

    checkUserSession();

    const interceptor = axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            const response = await axios.post('/api/auth/token/refresh/', {
              refresh: refreshToken
            });
            const newToken = response.data.access;
            localStorage.setItem('access_token', newToken);
            axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
            return axios(originalRequest);
          } catch (err) {
            handleLogout();
          }
        }
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.response.eject(interceptor);
    };
  }, []);

  const handleAuth = (userData, token) => {
    setUser(userData);
    localStorage.setItem('access_token', token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete axios.defaults.headers.common['Authorization'];
  };

  return (
    <Provider store={store}>
      <Router>
        <Routes>
          <Route path="/login" element={user ? <Navigate to="/" replace /> : <Auth onAuth={handleAuth} />} />
          <Route element={<ProtectedRoute user={user} />}>
            <Route element={<Layout user={user} onLogout={handleLogout} />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/listings" element={<Listings />} />
              <Route path="/sync" element={<Sync />} />
            </Route>
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </Provider>
  );
}

export default App;
