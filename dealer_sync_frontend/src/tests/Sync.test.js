import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import Sync from '../views/Sync';
import axios from 'axios';

jest.mock('axios');

describe('Sync Component', () => {
  beforeEach(() => {
    jest.useFakeTimers();
    axios.get.mockClear();
    axios.post.mockClear();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  test('starts sync process', async () => {
    axios.post.mockResolvedValue({ data: { task_id: '123' } });
    axios.get
      .mockResolvedValueOnce({ data: { state: 'PENDING' } })
      .mockResolvedValueOnce({ data: { state: 'IN_PROGRESS' } })
      .mockResolvedValueOnce({ data: { state: 'SUCCESS' } });

    const { getByText } = render(<Sync />);
    
    fireEvent.click(getByText('Start Sync'));
    
    await waitFor(() => expect(getByText('syncing')).toBeInTheDocument());
    
    jest.advanceTimersByTime(10000);
    
    await waitFor(() => expect(getByText('completed')).toBeInTheDocument());
  });
});