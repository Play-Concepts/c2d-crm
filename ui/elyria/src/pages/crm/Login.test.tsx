import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import { createMemoryHistory } from 'history';
import { Router } from 'react-router-dom';

import CrmLoginPage from './Login';
import { crmLogin } from '../../services/c2dcrm';
import { TEST_DATA_CRM_USER } from '../../testData/crmUser';
import { AuthProvider } from '../../components/AuthProvider';

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
    renderWithProviders(<CrmLoginPage />);

    expect(screen.queryByLabelText('Username')).toBeInTheDocument();
    expect(screen.queryByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
  });

  test('attempting to login with the correct details', async () => {
    const { history } = renderWithProviders(<CrmLoginPage />);

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

    await waitFor(() => expect(history.location.pathname).toEqual('/pages/crm/dashboard'));
  });

  test('attempting to login with not valid details', async () => {
    renderWithProviders(<CrmLoginPage />);

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
