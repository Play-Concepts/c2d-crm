import Axios from 'axios';
import { CrmLoginForm } from '../pages/crm/Login';
import { CrmListCustomersResponse, CrmTokenResponse } from './c2dcrm.interface';

export const uploadCsvFile = (file: File, token: string, onUploadProgress: (progressEvent: any) => void) => {
  let formData = new FormData();

  formData.append('customers_file', file);

  return Axios.post('/crm/upload', formData, {
    headers: { 'content-type': 'multipart/form-data', accept: 'application/json', Authorization: `Bearer ${token}` },
    onUploadProgress,
  });
};

export const listCrmCustomers = (token: string) => {
  return Axios.get<CrmListCustomersResponse[]>('/crm/customers', {
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
