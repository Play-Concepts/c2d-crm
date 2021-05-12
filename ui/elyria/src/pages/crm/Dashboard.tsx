import React, { Fragment } from 'react';
import Layout from '../../layout/Layout';

const CrmDashboardPage: React.FC = () => {
  return (
    <Layout>
      <Fragment>
        <p>Shows Paginated List of All citizens. List should differentiate between Claimed and Not Claimed data.</p>
        <p>Page to Handle Upload of CSV file</p>
      </Fragment>
    </Layout>
  );
};

export default CrmDashboardPage;
