import { CrmListCustomersResponse } from '../services/c2dcrm.interface';

export const TEST_DATA_CRM_CUSTOMERS: CrmListCustomersResponse[] = [
  {
    id: 'this-is-a-test-uuid-1',
    pda_url: '',
    status: 'claimed',
    total_count: 104,
    data: {
      person: {
        profile: {
          first_name: 'test firstName',
          last_name: 'test lastName',
        },
        address: {
          address_line_1: 'Test Flat, Test Address',
          city: 'Test City',
        },
        contact: {
          email: 'testEmail@test.com',
        },
      },
    },
  },
  {
    id: 'this-is-a-test-uuid-2',
    pda_url: '',
    status: 'new',
    total_count: 104,
    data: {
      person: {
        profile: {
          first_name: 'test firstName',
          last_name: 'test lastName',
        },
        address: {
          address_line_1: 'Test Flat, Test Address',
          city: 'Test City',
        },
        contact: {
          email: 'testEmail@test.com',
        },
      },
    },
  },
  {
    id: 'this-is-a-test-uuid-3',
    pda_url: '',
    status: 'new',
    total_count: 104,
    data: {
      person: {
        profile: {
          first_name: 'test firstName',
          last_name: 'test lastName',
        },
        address: {
          address_line_1: 'Test Flat, Test Address',
          city: 'Test City',
        },
        contact: {
          email: 'testEmail@test.com',
        },
      },
    },
  },
];
