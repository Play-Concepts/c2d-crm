export interface CrmTokenResponse {
  access_token: string;
  token_type: string;
}

export interface CrmCustomerInterface {
  id: string;
  profile: {
    first_name: string;
    last_name: string;
  };
  address: {
    address_line_1: string;
    city: string;
  };
  contact: {
    email: string;
  };
}
