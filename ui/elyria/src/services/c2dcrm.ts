import Axios from 'axios';
import { CrmLoginForm } from '../pages/crm/Login';
import { CrmTokenResponse } from './c2dcrm.interface';

export const uploadCsvFile = (
  file: File,
  token: string,
  onUploadProgress: (progressEvent: any) => void,
) => {
  let formData = new FormData();
  formData.append('customers_file', file);
  formData.append('token', token);
  return Axios.post('/crm/upload', formData, { headers: { 'content-type': 'multipart/form-data' }, onUploadProgress });
};

export const crmLogin = ({ username, password }: CrmLoginForm) => {
  let formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  return Axios.post<CrmTokenResponse>('/token', formData, {
    headers: { 'content-type': 'multipart/form-data' },
  });
};
