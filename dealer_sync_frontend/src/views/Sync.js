import React, { useState } from 'react';
import Card from '../components/Card';
import CardContent from '../components/CardContent';
import CardHeader from '../components/CardHeader';
import CardTitle from '../components/CardTitle';
import { RefreshCw, Check, AlertTriangle } from 'lucide-react';

const Sync = () => {
  const [syncStatus, setSyncStatus] = useState('idle');
  const [progress, setProgress] = useState(0);

  const startSync = () => {
    setSyncStatus('syncing');
    setProgress(0);
    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        if (prevProgress >= 100) {
          clearInterval(interval);
          setSyncStatus('completed');
          return 100;
        }
        return prevProgress + 10;
      });
    }, 500);
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
            className="bg-primary text-white px-4 py-2 rounded-md hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed"
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
          <ul className="space-y-2">
            <li>Last successful sync: 2 hours ago</li>
            <li>Total syncs today: 5</li>
            <li>Failed syncs today: 0</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};

export default Sync;
