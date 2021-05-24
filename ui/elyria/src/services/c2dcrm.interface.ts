export interface CrmTokenResponse {
  access_token: string;
  token_type: string;
}

export interface CrmListCustomersResponse {
  data: {
    person: PersonInterface;
  };
  id: string;
  pda_url: string;
  status: 'new' | 'claimed';
}

export interface CustomerIdentityResponse {
  person: PersonInterface;
}

export interface PersonInterface {
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
