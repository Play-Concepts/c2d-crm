import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import { createMemoryHistory } from 'history';
import { Router } from 'react-router-dom';

import AuthProvider from '../../components/AuthContext';
import LandingPage from './LandingPage';
import { config } from '../../config';

const mockLoginUrl = jest.fn();

const renderWithProviders = (ui: any, { route = '/' } = {}, locationState?: Object) => {
  const history = createMemoryHistory({ initialEntries: [route] });
  if (locationState) history.location.state = locationState;

  return {
    ...render(
      <AuthProvider>
        <Router history={history}>{ui}</Router>
      </AuthProvider>,
    ),
    history,
  };
};

describe('Landing Page', () => {
  beforeEach(() => {
    Object.defineProperty(window, 'location', { value: { search: '', assign: mockLoginUrl }, writable: true });
    jest.resetAllMocks();
  });

  test('renders without error', () => {
    renderWithProviders(<LandingPage />, { route: '/' });

    expect(screen.queryByText('Sign in with a Personal Data Account')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Sign in with a Personal Data Account' }));

    expect(window.location.assign).toHaveBeenCalledTimes(1);
    expect(window.location.assign).toHaveBeenCalledWith(config.pdaAuth.login);
  });
});
