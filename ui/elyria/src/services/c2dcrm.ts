import Axios from 'axios';
import { CrmLoginForm } from '../pages/crm/Login';
import { CrmTokenResponse } from './c2dcrm.interface';

export const upload = (file: any, token: string, namespace: string, data_path: string) => {
  let formData = new FormData();
  formData.append('customers_file', file[0]);
  formData.append('token', token);
  formData.append('namespace', namespace);
  formData.append('data_path', data_path);
  return Axios.post('/crm/upload', formData, { headers: { 'content-type': 'multipart/form-data' } });
};

export const crmLogin = ({ username, password }: CrmLoginForm) => {
  let formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  return Axios.post<CrmTokenResponse>('/token', formData, {
    headers: { 'content-type': 'multipart/form-data' },
  });
};
