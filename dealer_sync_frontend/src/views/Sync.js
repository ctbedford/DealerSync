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

  useEffect(() => {
    fetchSyncHistory();
  }, []);

  const fetchSyncHistory = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/sync/history/', {
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

  const startSync = async () => {
    setSyncStatus('syncing');
    setProgress(0);
    try {
      const response = await axios.post('http://localhost:8000/api/sync/start/', {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });

      // Simulating progress updates
      const interval = setInterval(() => {
        setProgress((prevProgress) => {
          if (prevProgress >= 100) {
            clearInterval(interval);
            setSyncStatus('completed');
            fetchSyncHistory();
            return 100;
          }
          return prevProgress + 10;
        });
      }, 500);
    } catch (err) {
      console.error('Sync error:', err);
      setSyncStatus('error');
      setError('Sync failed. Please try again.');
    }
  };

  const runScraperNow = async () => {
    setSyncStatus('syncing');
    setProgress(0);
    try {
      const response = await axios.post('http://localhost:8000/api/scraper/run-now/', {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setSyncStatus('completed');
      setProgress(100);
      fetchSyncHistory();
    } catch (err) {
      console.error('Run scraper now error:', err);
      setSyncStatus('error');
      setError('Failed to run scraper. Please try again.');
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
            className="btn disabled:opacity-50 disabled:cursor-not-allowed mr-4"
          >
            Start Scheduled Sync
          </button>
          <button
            onClick={runScraperNow}
            disabled={syncStatus === 'syncing'}
            className="btn disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Run Scraper Now
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
              <li>Last successful sync: {syncHistory.lastSuccessful}</li>
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

export default Sync;