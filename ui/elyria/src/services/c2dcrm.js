import Axios from "axios";

export const upload = (file, token, namespace, data_path, onSuccess, onFailure) => {
    let formData = new FormData();
    formData.append('customers_file', file[0]);
    formData.append('token', token);
    formData.append('namespace', namespace);
    formData.append('data_path', data_path);
    Axios.post('/crm/upload', formData, {headers: {'content-type': 'multipart/form-data'}})
        .then(response => onSuccess(response))
        .catch(error => onFailure(error));
};
