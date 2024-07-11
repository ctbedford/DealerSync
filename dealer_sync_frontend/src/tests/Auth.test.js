import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Auth from '../views/Auth';
import axios from 'axios';

jest.mock('axios');
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn(),
}));

describe('Auth Component', () => {
  test('renders login form by default', () => {
    const { getByText, getByPlaceholderText } = render(
      <Router>
        <Auth onAuth={() => {}} />
      </Router>
    );
    expect(getByText('Login')).toBeInTheDocument();
    expect(getByPlaceholderText('Username')).toBeInTheDocument();
    expect(getByPlaceholderText('Password')).toBeInTheDocument();
  });

  test('switches to registration form', () => {
    const { getByText, getByPlaceholderText } = render(
      <Router>
        <Auth onAuth={() => {}} />
      </Router>
    );
    fireEvent.click(getByText('Need an account? Register'));
    expect(getByText('Register')).toBeInTheDocument();
    expect(getByPlaceholderText('Email')).toBeInTheDocument();
  });

  test('submits login form', async () => {
    axios.post.mockResolvedValue({ data: { access: 'token', refresh: 'refresh_token' } });
    const mockOnAuth = jest.fn();
    const { getByPlaceholderText, getByText } = render(
      <Router>
        <Auth onAuth={mockOnAuth} />
      </Router>
    );
    
    fireEvent.change(getByPlaceholderText('Username'), { target: { value: 'testuser' } });
    fireEvent.change(getByPlaceholderText('Password'), { target: { value: 'password123' } });
    fireEvent.click(getByText('Login'));
    
    await waitFor(() => expect(mockOnAuth).toHaveBeenCalled());
    expect(axios.post).toHaveBeenCalledWith('http://localhost:8000/api/auth/token/', {
      username: 'testuser',
      password: 'password123'
    });
  });
});