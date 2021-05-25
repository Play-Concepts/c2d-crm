import Axios from 'axios';
import { CrmLoginForm } from '../pages/crm/CrmLoginPage';
import { CrmListCustomersResponse, CrmTokenResponse, CustomerIdentityResponse } from './c2dcrm.interface';
import { HatClient } from '@dataswift/hat-js';
import { config } from '../config';
import { HatRecord } from '@dataswift/hat-js/lib/interfaces/hat-record.interface';
import { CustomerSearchForm } from '../components/CustomerClaimForm';

export const uploadCsvFile = (file: File, token: string, onUploadProgress: (progressEvent: any) => void) => {
  let formData = new FormData();

  formData.append('customers_file', file);

  return Axios.post('/crm/upload', formData, {
    headers: { 'content-type': 'multipart/form-data', accept: 'application/json', Authorization: `Bearer ${token}` },
    onUploadProgress,
  });
};

export const listCrmCustomers = (token: string, page = 1, pageCount = 10) => {
  return Axios.get<CrmListCustomersResponse[]>(`/crm/customers?page=${page}&page_count=${pageCount}`, {
    headers: { 'content-type': 'application/json', accept: 'application/json', Authorization: `Bearer ${token}` },
  });
};

export const crmLogin = ({ username, password }: CrmLoginForm) => {
  let formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  return Axios.post<CrmTokenResponse>('/token', formData, {
    headers: { 'content-type': 'multipart/form-data' },
  });
};

export const getCustomerBasic = (token: string) => {
  return Axios.get<{ id: string }>('/customer/basic', {
    headers: { 'content-type': 'application/json', accept: 'application/json', Authorization: `Bearer ${token}` },
  });
};

export const searchCustomer = (token: string, data: CustomerSearchForm) => {
  return Axios.post<CrmListCustomersResponse[]>('/customer/search', data, {
    headers: { 'content-type': 'application/json', accept: 'application/json', Authorization: `Bearer ${token}` },
  });
};

export const claimCustomerData = (token: string, data: { id: string }) => {
  return Axios.post<CrmListCustomersResponse>('/customer/claim', data, {
    headers: { 'content-type': 'application/json', accept: 'application/json', Authorization: `Bearer ${token}` },
  });
};

export const getCustomerDetails = (token: string) => {
  const hat = new HatClient({
    token: token,
    secure: true,
    apiVersion: 'v2.6',
  });

  return hat.hatData().getAllDefault<CustomerIdentityResponse>(config.namespace, config.endpoint);
};

export const updateCustomerDetails = (token: string, data: HatRecord<CustomerIdentityResponse>) => {
  const hat = new HatClient({
    token: token,
    secure: true,
    apiVersion: 'v2.6',
  });

  return hat.hatData().update<CustomerIdentityResponse>([data]);
};
