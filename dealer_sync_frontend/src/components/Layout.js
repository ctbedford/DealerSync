import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Link, useLocation, useNavigate, Outlet } from 'react-router-dom';
import { Home, List, Repeat, ChevronRight, ChevronLeft, LogOut, User, RefreshCw, Loader } from 'lucide-react';
import axios from 'axios';
import { checkSyncStatus } from '../store/syncSlice';

const Layout = ({ onLogout, user }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { syncStatus, progress, taskId, userId, currentItem, totalItems, currentVehicle } = useSelector((state) => state.sync);

  useEffect(() => {
    if (taskId && userId === user.id) {
      const interval = setInterval(() => {
        dispatch(checkSyncStatus({ taskId, userId }));
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [taskId, userId, dispatch, user.id]);

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/listings', label: 'Listings', icon: List },
    { path: '/sync', label: 'Sync', icon: Repeat },
  ];

  const handleLogout = () => {
    onLogout();
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
    navigate('/');
  };

  const renderSyncIcon = () => {
    switch (syncStatus) {
      case 'syncing':
        return <RefreshCw className="h-4 w-4 mr-2 animate-spin" />;
      case 'checking':
        return <Loader className="h-4 w-4 mr-2 animate-spin" />;
      default:
        return null;
    }
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
        {(syncStatus === 'syncing' || syncStatus === 'checking') && userId === user.id && (
          <div className={`mt-4 ${isCollapsed ? 'hidden' : 'block'}`}>
            <div className="flex items-center text-sm text-secondary mb-1">
              {renderSyncIcon()}
              <span>{syncStatus === 'checking' ? 'Checking sync' : 'Sync in progress'}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
              {progress > 0 ? (
                <div
                  className="bg-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                ></div>
              ) : (
                <div className="bg-primary h-2 rounded-full animate-pulse"></div>
              )}
            </div>
            <div className="text-xs text-secondary mt-1">
              {currentItem && totalItems ? (
                <span>Vehicle {currentItem} of {totalItems}</span>
              ) : (
                <span>Processing vehicles...</span>
              )}
            </div>
            {currentVehicle && (
              <div className="text-xs text-secondary mt-1">
                Current: {currentVehicle}
              </div>
            )}
          </div>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="absolute bottom-4 left-4 bg-primary-light text-secondary-light p-2 rounded-full"
        >
          {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </nav>
      <main className="flex-1 overflow-y-auto p-8 bg-background">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
