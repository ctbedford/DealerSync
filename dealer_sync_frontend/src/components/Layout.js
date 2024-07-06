import React, { useState } from 'react';
import { Link, useLocation, useNavigate, Outlet } from 'react-router-dom';
import { Home, List, Repeat, ChevronRight, ChevronLeft, LogOut, User } from 'lucide-react';
import axios from 'axios';

const Layout = ({ onLogout, user }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/listings', label: 'Listings', icon: List },
    { path: '/sync', label: 'Sync', icon: Repeat },
  ];

  const handleLogout = () => {
    onLogout();
    // Clear local storage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user'); // Assuming user data is stored here

    // Clear cookies if any are set (for demonstration, using js-cookie library)
    // import Cookies from 'js-cookie';
    // Cookies.remove('access_token');
    // Cookies.remove('refresh_token');

    // Clear authorization header
    delete axios.defaults.headers.common['Authorization'];
    navigate('/');
  };

  return (
    <div className="flex h-screen bg-background">
      <nav className={`bg-background-light p-4 transition-all duration-300 ${isCollapsed ? 'w-16' : 'w-64'}`}>
        <div className={`text-2xl font-bold text-secondary-light mb-8 ${isCollapsed ? 'hidden' : 'block'}`}>DealerSync</div>
        <ul>
          {navItems.map((item) => (
            <li key={item.path} className="mb-2">
              <Link
                to={item.path}
                className={`flex items-center p-2 rounded-md transition-colors duration-200 ${location.pathname === item.path
                    ? 'bg-primary-light text-secondary-light'
                    : 'text-secondary hover:bg-primary-dark hover:text-secondary-light'
                  }`}
              >
                <item.icon className="h-5 w-5" />
                {!isCollapsed && <span className="ml-2">{item.label}</span>}
              </Link>
            </li>
          ))}
          <li className="mt-auto">
            <div className="flex items-center p-2 text-secondary">
              <User className="h-5 w-5" />
              {!isCollapsed && <span className="ml-2">{user?.username}</span>}
            </div>
          </li>
          <li>
            <button
              onClick={handleLogout}
              className="flex items-center p-2 rounded-md transition-colors duration-200 text-secondary hover:bg-primary-dark hover:text-secondary-light w-full"
            >
              <LogOut className="h-5 w-5" />
              {!isCollapsed && <span className="ml-2">Logout</span>}
            </button>
          </li>
        </ul>
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="absolute bottom-4 left-4 bg-primary-light text-secondary-light p-2 rounded-full"
        >
          {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </nav>
      <main className="flex-1 overflow-y-auto p-8 bg-background"><Outlet /></main>
    </div>
  );
};

export default Layout;
