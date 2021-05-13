import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';

import CrmLoginPage from './Login';
import { crmLogin } from '../../services/c2dcrm';

jest.mock('../../services/c2dcrm');
const mockCrmLogin: jest.Mocked<any> = crmLogin;

describe('Crm Login Page', () => {
  test('renders without error', () => {
    render(<CrmLoginPage />);

    expect(screen.queryByLabelText('Username')).toBeInTheDocument();
    expect(screen.queryByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
  });

  test('attempting to login with the correct details', () => {
    render(<CrmLoginPage />);

    fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'testUsername' } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'testPassword' } });

    fireEvent.click(screen.getByRole('button', { name: 'Login' }));

    expect(mockCrmLogin).toHaveBeenCalledWith({
      username: 'testUsername',
      password: 'testPassword',
    });
  });
});
