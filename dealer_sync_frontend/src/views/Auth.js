import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Card from '../components/Card';
import CardContent from '../components/CardContent';
import CardHeader from '../components/CardHeader';
import CardTitle from '../components/CardTitle';
import { setUserId } from '../store/syncSlice';
import { User, Lock, Mail, AlertCircle } from 'lucide-react';
import { useDispatch } from 'react-redux';

const Auth = ({ onAuth }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const dispatch = useDispatch(); // Add this line to use dispatch

  const validateForm = () => {
    if (!username || !password) {
      setError('Username and password are required');
      return false;
    }
    if (!isLogin && !email) {
      setError('Email is required for registration');
      return false;
    }
    return true;
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!validateForm()) return;

    try {
      let userData;
      if (isLogin) {
        const response = await axios.post('http://localhost:8000/api/auth/token/', {
          username,
          password
        });
        userData = response.data;
      } else {
        // Handle registration
        await axios.post('http://localhost:8000/api/auth/register/', {
          username,
          email,
          password
        });
        // After successful registration, log the user in
        const loginResponse = await axios.post('http://localhost:8000/api/auth/token/', {
          username,
          password
        });
        userData = loginResponse.data;
      }

      const { access, refresh, user } = userData;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('user', JSON.stringify(user));
      onAuth(user, access);
      dispatch(setUserId(user.id));

      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      console.log('Authentication successful. User ID:', user.id);
      navigate('/');
    } catch (err) {
      console.error('Authentication error:', err.response?.data || err.message);
      setError(err.response?.data?.detail || 'Authentication failed. Please try again.');
    }
  };


  return (
    <div className="bg-background min-h-screen flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-primary text-center">{isLogin ? 'Login' : 'Register'}</CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
              <span className="flex items-center">
                <AlertCircle className="mr-2" size={18} />
                {error}
              </span>
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="flex items-center border-b border-primary py-2">
              <User className="text-primary mr-2" />
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="appearance-none bg-transparent border-none w-full text-text mr-3 py-1 px-2 leading-tight focus:outline-none"
              />
            </div>
            {!isLogin && (
              <div className="flex items-center border-b border-primary py-2">
                <Mail className="text-primary mr-2" />
                <input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none bg-transparent border-none w-full text-text mr-3 py-1 px-2 leading-tight focus:outline-none"
                />
              </div>
            )}
            <div className="flex items-center border-b border-primary py-2">
              <Lock className="text-primary mr-2" />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="appearance-none bg-transparent border-none w-full text-text mr-3 py-1 px-2 leading-tight focus:outline-none"
              />
            </div>
            <button
              type="submit"
              className="w-full bg-primary hover:bg-primary-dark text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              {isLogin ? 'Login' : 'Register'}
            </button>
          </form>
          <div className="mt-4 text-center">
            <button
              onClick={() => {
                setIsLogin(!isLogin);
                setError('');
              }}
              className="text-primary hover:text-primary-dark"
            >
              {isLogin ? 'Need an account? Register' : 'Already have an account? Login'}
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Auth;
