import React, { Fragment } from 'react';
import Layout from '../../layout/Layout';
import CustomersTable from '../../components/CustomersTable';
import { TEST_DATA_CRM_CUSTOMERS } from '../../testData/crmCustomers';
import UploadFile from '../../components/UploadFile';

const CrmDashboardPage: React.FC = () => {
  return (
    <Layout>
      <UploadFile />
      <CustomersTable customers={TEST_DATA_CRM_CUSTOMERS} />
      <Fragment>
        <p>Shows Paginated List of All citizens. List should differentiate between Claimed and Not Claimed data.</p>
        <p>Page to Handle Upload of CSV file</p>
      </Fragment>
    </Layout>
  );
};

export default CrmDashboardPage;
