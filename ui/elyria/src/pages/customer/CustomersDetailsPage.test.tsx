import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import { createMemoryHistory } from 'history';
import { Router } from 'react-router-dom';

import { getCustomerDetails, updateCustomerDetails } from '../../services/c2dcrm';
import AuthProvider from '../../components/AuthContext';
import { TEST_PDA_CUSTOMER_PROFILE } from '../../testData/testPdaCustomerProfile';
import CustomerDetailsPage from './CustomerDetailsPage';

jest.mock('../../services/c2dcrm');
const mockGetCustomerDetails: jest.Mocked<any> = getCustomerDetails;
const mockUpdateCustomerDetails: jest.Mocked<any> = updateCustomerDetails;

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

describe('Customer Details Page', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test('renders without error', async () => {
    mockGetCustomerDetails.mockResolvedValueOnce({
      parsedBody: TEST_PDA_CUSTOMER_PROFILE,
    });

    renderWithProviders(<CustomerDetailsPage />, { route: '/profile' });

    await waitFor(() => expect(screen.queryByLabelText('Email')).toBeInTheDocument());
    await waitFor(() => expect(screen.queryByLabelText('First name')).toBeInTheDocument());
    await waitFor(() => expect(screen.queryByLabelText('Last name')).toBeInTheDocument());
    await waitFor(() => expect(screen.queryByLabelText('Address')).toBeInTheDocument());
    await waitFor(() => expect(screen.queryByLabelText('City')).toBeInTheDocument());

    await waitFor(() => expect(screen.getByDisplayValue('test@email.com')).toBeInTheDocument());
    await waitFor(() => expect(screen.getByDisplayValue('testFirstName')).toBeInTheDocument());
    await waitFor(() => expect(screen.getByDisplayValue('testLastName')).toBeInTheDocument());
    await waitFor(() => expect(screen.getByDisplayValue('testAddress')).toBeInTheDocument());
    await waitFor(() => expect(screen.getByDisplayValue('testCity')).toBeInTheDocument());

    await waitFor(() => expect(screen.queryByRole('button', { name: 'Save' })).toBeInTheDocument());
  });

  test('updates the profile without error', async () => {
    mockGetCustomerDetails.mockResolvedValueOnce({
      parsedBody: TEST_PDA_CUSTOMER_PROFILE,
    });

    renderWithProviders(<CustomerDetailsPage />, { route: '/profile' });

    await waitFor(() => expect(screen.getByDisplayValue('test@email.com')).toBeInTheDocument());

    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'updatedTest@email.com' } });
    fireEvent.change(screen.getByLabelText('Last name'), { target: { value: 'updatedTestLastName' } });

    await waitFor(() => expect(screen.getByDisplayValue('updatedTest@email.com')).toBeInTheDocument());
    await waitFor(() => expect(screen.getByDisplayValue('updatedTestLastName')).toBeInTheDocument());

    mockUpdateCustomerDetails.mockResolvedValueOnce({
      parsedBody: TEST_PDA_CUSTOMER_PROFILE,
    });

    fireEvent.click(screen.getByRole('button', { name: 'Save' }));

    expect(mockUpdateCustomerDetails).toHaveBeenCalledWith('', {
      endpoint: 'test-endpoint',
      recordId: 'test-record-id',
      data: {
        person: {
          address: {
            address_line_1: 'testAddress',
            city: 'testCity',
          },
          contact: {
            email: 'updatedTest@email.com',
          },
          profile: {
            first_name: 'testFirstName',
            last_name: 'updatedTestLastName',
          },
        },
      },
    });

    await waitFor(() => expect(screen.getByText('Your profile information updated successfully.')).toBeInTheDocument());
  });
});
