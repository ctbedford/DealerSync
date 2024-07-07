import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Card from '../components/Card';
import CardContent from '../components/CardContent';
import CardHeader from '../components/CardHeader';
import CardTitle from '../components/CardTitle';
import { RefreshCw, Check, AlertTriangle } from 'lucide-react';

const Sync = () => {
  const [syncStatus, setSyncStatus] = useState('idle');
  const [progress, setProgress] = useState(0);
  const [syncHistory, setSyncHistory] = useState(null);
  const [error, setError] = useState(null);
  const [taskId, setTaskId] = useState(null);

  useEffect(() => {
    fetchSyncStatus();
    fetchSyncHistory();
  }, []);

  const fetchSyncStatus = async () => {
    const savedTaskId = localStorage.getItem('syncTaskId');
    if (savedTaskId) {
      await checkSyncStatus(savedTaskId);
    }
  };

  const fetchSyncHistory = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/scraper/sync/history/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setSyncHistory(response.data);
    } catch (err) {
      console.error('Sync history fetch error:', err);
      setError('Failed to fetch sync history');
    }
  };

  const checkSyncStatus = async (taskId) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/scraper/status/?task_id=${taskId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      if (response.data.status === 'SUCCESS') {
        setSyncStatus('completed');
        setProgress(100);
        fetchSyncHistory();
        localStorage.removeItem('syncTaskId');
      } else if (response.data.status === 'FAILURE') {
        setSyncStatus('error');
        setError('Sync failed. Please try again.');
        localStorage.removeItem('syncTaskId');
      } else if (response.data.status === 'PENDING' || response.data.status === 'STARTED') {
        setSyncStatus('syncing');
        setProgress((prevProgress) => Math.min(prevProgress + 10, 90));
        setTimeout(() => checkSyncStatus(taskId), 5000);
      } else {
        setSyncStatus('idle');
        localStorage.removeItem('syncTaskId');
      }
    } catch (err) {
      console.error('Sync status check error:', err);
      setError('Failed to check sync status');
      setSyncStatus('idle');
      localStorage.removeItem('syncTaskId');
    }
  };

  const startSync = async () => {
    setSyncStatus('syncing');
    setProgress(0);
    setError(null);
    try {
      const response = await axios.post('http://localhost:8000/api/scraper/run-now/', {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setTaskId(response.data.task_id);
      localStorage.setItem('syncTaskId', response.data.task_id);
      checkSyncStatus(response.data.task_id);
    } catch (err) {
      console.error('Sync error:', err);
      setSyncStatus('error');
      setError('Sync failed to start. Please try again.');
    }
  };



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
              {syncStatus === 'idle' && <RefreshCw size={24} className="text-secondary" />}
              {syncStatus === 'syncing' && <RefreshCw size={24} className="text-primary animate-spin" />}
              {syncStatus === 'completed' && <Check size={24} className="text-green-500" />}
              {syncStatus === 'error' && <AlertTriangle size={24} className="text-red-500" />}
            </div>
            <span className="capitalize text-lg">{syncStatus}</span>
          </div>
          {syncStatus === 'syncing' && (
            <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4 dark:bg-gray-700">
              <div className="bg-primary h-2.5 rounded-full" style={{ width: `${progress}%` }}></div>
            </div>
          )}
          <button
            onClick={startSync}
            disabled={syncStatus === 'syncing'}
            className="btn disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Start Sync
          </button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-primary">Sync History</CardTitle>
        </CardHeader>
        <CardContent>
          {error && <div className="text-red-500 mb-4">{error}</div>}
          {syncHistory ? (
            <ul className="space-y-2">
              <li>Last successful sync: {syncHistory.lastSuccessful || 'N/A'}</li>
              <li>Total syncs today: {syncHistory.totalToday}</li>
              <li>Failed syncs today: {syncHistory.failedToday}</li>
            </ul>
          ) : (
            <div>Loading sync history...</div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Sync;;