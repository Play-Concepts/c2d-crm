import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import { createMemoryHistory } from 'history';
import { Router } from 'react-router-dom';

import CrmLoginPage from './CrmLoginPage';
import { crmLogin } from '../../services/c2dcrm';
import { TEST_DATA_CRM_USER } from '../../testData/crmUser';
import AuthProvider from '../../components/AuthContext';

jest.mock('../../services/c2dcrm');
const mockCrmLogin: jest.Mocked<any> = crmLogin;

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

describe('Crm Login Page', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test('renders without error', () => {
    renderWithProviders(<CrmLoginPage />, { route: '/admin/login' });

    expect(screen.queryByLabelText('Username')).toBeInTheDocument();
    expect(screen.queryByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
  });

  test('attempting to login with the correct details', async () => {
    const { history } = renderWithProviders(<CrmLoginPage />, { route: '/admin/login' });

    mockCrmLogin.mockResolvedValueOnce({
      data: TEST_DATA_CRM_USER,
    });

    fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'testUsername' } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'testPassword' } });

    fireEvent.click(screen.getByRole('button', { name: 'Login' }));

    expect(mockCrmLogin).toHaveBeenCalledWith({
      username: 'testUsername',
      password: 'testPassword',
    });

    await waitFor(() => expect(history.location.pathname).toEqual('/admin'));
  });

  test('attempting to login with not valid details', async () => {
    renderWithProviders(<CrmLoginPage />, { route: '/admin/login' });

    mockCrmLogin.mockRejectedValueOnce({});

    fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'testUsername' } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'testPassword' } });

    fireEvent.click(screen.getByRole('button', { name: 'Login' }));

    expect(mockCrmLogin).toHaveBeenCalledWith({
      username: 'testUsername',
      password: 'testPassword',
    });

    await waitFor(() => expect(screen.getByText('Incorrect username or password.')).toBeInTheDocument());
  });
});
