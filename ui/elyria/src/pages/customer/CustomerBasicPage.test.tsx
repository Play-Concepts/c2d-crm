import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import { createMemoryHistory } from 'history';
import { Router } from 'react-router-dom';

import { claimCustomerData, getCustomerBasic, searchCustomer } from '../../services/c2dcrm';
import AuthProvider from '../../components/AuthContext';
import CustomerBasicPage from './CustomerBasicPage';
import { TEST_DATA_CRM_CUSTOMERS } from '../../testData/crmCustomers';

jest.mock('../../services/c2dcrm');
const mockGetCustomerBasic: jest.Mocked<any> = getCustomerBasic;
const mockSearchCustomer: jest.Mocked<any> = searchCustomer;
const mockClaimCustomerData: jest.Mocked<any> = claimCustomerData;

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

describe('Customer Basic Page', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test('renders the form without error', async () => {
    mockGetCustomerBasic.mockRejectedValueOnce({});

    renderWithProviders(<CustomerBasicPage />, { route: '/app' });

    await waitFor(() => expect(screen.queryByText('Search for your data record')).toBeInTheDocument());
    await waitFor(() => expect(screen.queryByLabelText('Email *')).toBeInTheDocument());
    await waitFor(() => expect(screen.queryByLabelText('Last name *')).toBeInTheDocument());
    await waitFor(() => expect(screen.queryByLabelText('House number *')).toBeInTheDocument());

    await waitFor(() => expect(screen.queryByRole('button', { name: 'Search' })).toBeInTheDocument());
  });

  test('renders the QR Code without error', async () => {
    mockGetCustomerBasic.mockResolvedValueOnce({
      data: TEST_DATA_CRM_CUSTOMERS[0],
    });

    renderWithProviders(<CustomerBasicPage />, { route: '/app' });

    await waitFor(() => expect(screen.queryByTestId('qr-code')).toBeInTheDocument());

    await waitFor(() => expect(screen.queryByText('Search for your data record')).toBeNull());
    await waitFor(() => expect(screen.queryByLabelText('Email *')).toBeNull());
    await waitFor(() => expect(screen.queryByLabelText('Last name *')).toBeNull());
    await waitFor(() => expect(screen.queryByLabelText('House number *')).toBeNull());

    await waitFor(() => expect(screen.queryByRole('button', { name: 'Search' })).toBeNull());
  });

  test('renders the form and then displays the QR Code', async () => {
    mockGetCustomerBasic.mockRejectedValueOnce({});

    renderWithProviders(<CustomerBasicPage />, { route: '/app' });

    await waitFor(() => expect(screen.queryByText('Search for your data record')).toBeInTheDocument());

    fireEvent.change(screen.getByLabelText('Email *'), { target: { value: 'test@email.com' } });
    fireEvent.change(screen.getByLabelText('Last name *'), { target: { value: 'testLastName' } });
    fireEvent.change(screen.getByLabelText('House number *'), { target: { value: 'testHouseNumber' } });

    mockSearchCustomer.mockResolvedValueOnce({
      data: TEST_DATA_CRM_CUSTOMERS,
    });

    fireEvent.click(screen.getByRole('button', { name: 'Search' }));

    expect(mockSearchCustomer).toHaveBeenCalledWith('', {
      email: 'test@email.com',
      last_name: 'testLastName',
      house_number: 'testHouseNumber',
    });

    await waitFor(() => expect(screen.getAllByText('Claim').length).toEqual(3));

    mockClaimCustomerData.mockResolvedValueOnce({
      data: TEST_DATA_CRM_CUSTOMERS[0],
    });
    // Click the first result to proceed
    fireEvent.click(screen.getAllByText('Claim')[0]);

    expect(mockClaimCustomerData).toHaveBeenCalledWith('', {
      id: 'this-is-a-test-uuid-1',
    });

    await waitFor(() => expect(screen.queryByTestId('qr-code')).toBeInTheDocument());
  });
});
