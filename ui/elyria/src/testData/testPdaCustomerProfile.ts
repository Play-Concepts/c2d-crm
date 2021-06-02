import { HatRecord } from '@dataswift/hat-js/lib/interfaces/hat-record.interface';
import { CustomerIdentityResponse, PersonInterface } from '../services/c2dcrm.interface';

export const TEST_PERSON: PersonInterface = {
  profile: {
    first_name: 'testFirstName',
    last_name: 'testLastName',
  },
  address: {
    address_line_1: 'testAddress',
    city: 'testCity',
  },
  contact: {
    email: 'test@email.com',
  },
};

export const TEST_PDA_CUSTOMER_PROFILE: HatRecord<CustomerIdentityResponse>[] = [
  {
    endpoint: 'test-endpoint',
    recordId: 'test-record-id',
    data: {
      person: TEST_PERSON,
    },
  },
];
