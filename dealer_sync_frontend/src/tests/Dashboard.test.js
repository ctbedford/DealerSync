import React from 'react';
import { render, waitFor } from '@testing-library/react';
import Dashboard from '../views/Dashboard';
import axios from 'axios';

jest.mock('axios');

describe('Dashboard Component', () => {
  test('renders dashboard data', async () => {
    axios.get.mockResolvedValue({
      data: {
        stats: [
          { title: 'Total Listings', value: 100, icon: 'Car' },
          { title: 'Active Syncs', value: 2, icon: 'Activity' },
        ],
        recentActivity: [
          { title: 'New Listing Added', description: '2023 Toyota Camry', time: '2 days ago' },
        ],
        chartData: [
          { name: 'Jan', listings: 50, views: 200 },
          { name: 'Feb', listings: 60, views: 250 },
        ]
      }
    });

    const { getByText } = render(<Dashboard />);
    
    await waitFor(() => {
      expect(getByText('Total Listings')).toBeInTheDocument();
      expect(getByText('100')).toBeInTheDocument();
      expect(getByText('Active Syncs')).toBeInTheDocument();
      expect(getByText('2')).toBeInTheDocument();
      expect(getByText('New Listing Added')).toBeInTheDocument();
      expect(getByText('2023 Toyota Camry')).toBeInTheDocument();
    });
  });
});