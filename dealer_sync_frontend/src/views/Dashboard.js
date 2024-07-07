import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Card from '../components/Card';
import CardContent from '../components/CardContent';
import CardHeader from '../components/CardHeader';
import CardTitle from '../components/CardTitle';
import { Car, Activity, Clock, Eye } from 'lucide-react';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/api/dashboard/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setDashboardData(response.data);
      } catch (err) {
        setError('Failed to fetch dashboard data');
        console.error('Dashboard fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!dashboardData) return null;

  const { stats, recentActivity, chartData } = dashboardData;

  return (
    <div className="bg-background min-h-screen text-text p-6">
      <h1 className="text-4xl font-bold mb-6 text-primary pb-2 border-b-2 border-primary">DealerSync Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <Card key={index} className="bg-background-light">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium text-text">{stat.title}</CardTitle>
              {stat.icon === 'Car' && <Car className="h-4 w-4 text-secondary" />}
              {stat.icon === 'Activity' && <Activity className="h-4 w-4 text-secondary" />}
              {stat.icon === 'Clock' && <Clock className="h-4 w-4 text-secondary" />}
              {stat.icon === 'Eye' && <Eye className="h-4 w-4 text-secondary" />}
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-primary">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card className="card mb-6">
          <CardHeader>
            <CardTitle className="text-primary">Listings and Views Over Time</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Bar yAxisId="left" dataKey="listings" fill="#d4af37" name="Listings" />
                <Bar yAxisId="right" dataKey="views" fill="#c41e3a" name="Views" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-primary">Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-4">
              {recentActivity.map((activity, index) => (
                <li key={index} className="bg-background p-3 rounded-md border border-secondary">
                  <h4 className="font-semibold text-primary">{activity.title}</h4>
                  <p className="text-sm text-text">{activity.description}</p>
                  <span className="text-xs text-text-light">{activity.time}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;