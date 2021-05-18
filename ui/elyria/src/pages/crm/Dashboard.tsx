import React, { useEffect, useState } from 'react';
import Alert from '@material-ui/lab/Alert';
import { Typography } from '@material-ui/core';
import { useHistory } from 'react-router';

import Layout from '../../layout/Layout';
import CustomersTable from '../../components/CustomersTable';
import { listCrmCustomers } from '../../services/c2dcrm';
import { useAuth } from '../../hooks/useAuth';
import { CrmListCustomersResponse } from '../../services/c2dcrm.interface';
import UploadFilePopover from '../../components/UploadFile';

const CrmDashboardPage: React.FC = () => {
  const history = useHistory();
  const { token, isAuthenticated } = useAuth();
  const [error, setError] = useState('');
  const [customers, setCustomers] = useState<CrmListCustomersResponse[]>([]);

  if (!isAuthenticated) history.push('/pages/crm/login');

  const listAvailableCrmCustomers = async () => {
    try {
      if (!isAuthenticated) return;

      const res = await listCrmCustomers(token);
      if (res.data) {
        setCustomers(res.data);
      }
    } catch (e) {
      setError('Something went wrong. Please refresh to try again.');
    }
  };

  useEffect(() => {
    listAvailableCrmCustomers();
  }, []);

  return (
    <Layout>
      {error && (
        <Alert severity="error" style={{ marginBottom: '20px' }}>
          {error}
        </Alert>
      )}
      <UploadFilePopover onFileUploadCompleted={() => listAvailableCrmCustomers()} />
      {customers.length > 0 ? (
        <CustomersTable customers={customers} />
      ) : (
        <Typography variant="body2" color="textSecondary">
          There is no data records, please upload a file to get started
        </Typography>
      )}
    </Layout>
  );
};

export default CrmDashboardPage;
