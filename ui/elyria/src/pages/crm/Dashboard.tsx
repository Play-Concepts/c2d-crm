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

const customers: Map<string, CrmListCustomersResponse[]> = new Map();

const CrmDashboardPage: React.FC = () => {
  const history = useHistory();
  const { token, isAuthenticated } = useAuth();
  const [error, setError] = useState('');
  const [displayCustomers, setDisplayCustomers] = useState<CrmListCustomersResponse[]>([]);

  if (!isAuthenticated) history.push('/pages/crm/login');

  const listAvailableCrmCustomers = async (page = 1, pageCount = 10) => {
    try {
      if (!isAuthenticated) return;

      const maybeCached = customers.get(`page=${page}&page_count=${pageCount}`);

      if (maybeCached) {
        setDisplayCustomers(maybeCached || []);

        return;
      }

      const res = await listCrmCustomers(token, page, pageCount);

      if (res.data && res.data.length > 0) {
        customers.set(`page=${page}&page_count=${pageCount}`, res.data);
        setDisplayCustomers(res.data);
      }
    } catch (e) {
      setError('Something went wrong. Please refresh to try again.');
    }
  };

  useEffect(() => {
    listAvailableCrmCustomers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Layout>
      {error && (
        <Alert severity="error" style={{ marginBottom: '20px' }}>
          {error}
        </Alert>
      )}
      <UploadFilePopover onFileUploadCompleted={listAvailableCrmCustomers} />
      {displayCustomers.length > 0 ? (
        <CustomersTable customers={displayCustomers} onPageChange={listAvailableCrmCustomers} />
      ) : (
        <Typography variant="body2" color="textSecondary">
          There is no data records, please upload a file to get started
        </Typography>
      )}
    </Layout>
  );
};

export default CrmDashboardPage;
