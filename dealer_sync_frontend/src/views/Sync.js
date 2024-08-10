import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import axios from 'axios';
import { setSyncStatus, setProgress, setTaskId, setError, resetSync, setUserId, updateSyncProgress } from '../store/syncSlice';
import { RefreshCw, Check, AlertTriangle, Loader } from 'lucide-react';
import Card from '../components/Card';
import CardHeader from '../components/CardHeader';
import CardTitle from '../components/CardTitle';
import CardContent from '../components/CardContent';

const Sync = () => {
  const dispatch = useDispatch();
  const { syncStatus, progress, taskId, error, totalItems, currentItem, userId, currentVehicle } = useSelector((state) => state.sync);
  const [syncHistory, setSyncHistory] = useState(null);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const webSocket = useRef(null);

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
      dispatch(setUserId(user.id));
      connectWebSocket(user.id);
    }
  }, [dispatch]);

  useEffect(() => {
    console.log('Sync component state updated:', { syncStatus, progress, taskId, error, totalItems, currentItem, userId, currentVehicle });
  }, [syncStatus, progress, taskId, error, totalItems, currentItem, userId, currentVehicle]);

  const connectWebSocket = useCallback((userId) => {
    if (webSocket.current?.readyState === WebSocket.OPEN) return;

    webSocket.current = new WebSocket(`ws://localhost:8000/ws/sync/?user_id=${userId}`);

    webSocket.current.onopen = () => {
      console.log('WebSocket connected');
    };

    webSocket.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('WebSocket message received:', data);
        if (data.message) {
          const message = JSON.parse(data.message);
          dispatch(updateSyncProgress(message));
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    webSocket.current.onclose = (event) => {
      console.log('WebSocket disconnected:', event.code, event.reason);
      setTimeout(() => connectWebSocket(userId), 5000);
    };

    webSocket.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }, [dispatch]);

  useEffect(() => {
    return () => {
      if (webSocket.current) {
        webSocket.current.close();
      }
    };
  }, []);

  const fetchSyncHistory = useCallback(async () => {
    try {
      setIsLoadingHistory(true);
      const response = await axios.get('http://localhost:8000/api/scraper/sync/history/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setSyncHistory(response.data);
    } catch (err) {
      console.error('Failed to fetch sync history:', err);
    } finally {
      setIsLoadingHistory(false);
    }
  }, []);

  useEffect(() => {
    fetchSyncHistory();
  }, [fetchSyncHistory]);

  const startSync = async () => {
    if (!userId) {
      console.error('User ID not set. Cannot start sync.');
      dispatch(setError('User not authenticated. Please log in again.'));
      return;
    }
    try {
      dispatch(setSyncStatus('syncing'));
      dispatch(setProgress(0));
      dispatch(setError(null));
      const response = await axios.post('http://localhost:8000/api/scraper/run-now/', { userId }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      dispatch(setTaskId(response.data.task_id));
    } catch (err) {
      dispatch(setSyncStatus('error'));
      dispatch(setError('Sync failed to start. Please try again.'));
    }
  };

  const renderSyncStatus = () => {
    switch (syncStatus) {
      case 'idle':
        return <RefreshCw size={24} className="text-secondary" />;
      case 'syncing':
        return <RefreshCw size={24} className="text-primary animate-spin" />;
      case 'checking':
        return <Loader size={24} className="text-primary animate-spin" />;
      case 'completed':
        return <Check size={24} className="text-green-500" />;
      case 'error':
        return <AlertTriangle size={24} className="text-red-500" />;
      default:
        return null;
    }
  };

  const renderProgressBar = () => (
    <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4 dark:bg-gray-700">
      {progress > 0 ? (
        <div
          className="bg-primary h-2.5 rounded-full transition-all duration-300"
          style={{ width: `${progress}%` }}
        ></div>
      ) : (
        <div className="bg-primary h-2.5 rounded-full animate-pulse"></div>
      )}
    </div>
  );

  const renderSyncDetails = () => (
    <>
      {renderProgressBar()}
      <div className="text-sm text-secondary">
        {totalItems ? (
          <span>{currentItem} of {totalItems} vehicles processed</span>
        ) : (
          <span>{currentItem} vehicles processed</span>
        )}
      </div>
      {currentVehicle && (
        <div className="text-sm text-secondary mt-1">
          Current vehicle: {currentVehicle}
        </div>
      )}
    </>
  );

  const renderSyncHistory = () => (
    <Card>
      <CardHeader>
        <CardTitle className="text-primary">Sync History</CardTitle>
      </CardHeader>
      <CardContent>
        {syncStatus === "error" && error && <div className="text-red-500 mb-4">{error}</div>}
        {isLoadingHistory ? (
          <div>Loading sync history...</div>
        ) : syncHistory ? (
          <ul className="space-y-2">
            <li>Last successful sync: {syncHistory.lastSuccessful || 'N/A'}</li>
            <li>Total syncs today: {syncHistory.totalToday}</li>
            <li>Failed syncs today: {syncHistory.failedToday}</li>
          </ul>
        ) : (
          <div>No sync history available.</div>
        )}
      </CardContent>
    </Card>
  );

  return (
    <div className="bg-background min-h-screen text-text p-6">
      <h1 className="text-4xl font-bold mb-6 text-primary pb-2 border-b-2 border-primary">Sync Dashboard</h1>

      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-primary">Sync Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center mb-4">
            <div className="mr-4">
              {renderSyncStatus()}
            </div>
            <span className="capitalize text-lg">{syncStatus}</span>
          </div>
          {(syncStatus === 'syncing' || syncStatus === 'checking') && renderSyncDetails()}
          <button
            onClick={startSync}
            disabled={syncStatus === 'syncing' || syncStatus === 'checking'}
            className="btn mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Start Sync
          </button>
        </CardContent>
      </Card>

      {renderSyncHistory()}
    </div>
  );
};

export default Sync;
