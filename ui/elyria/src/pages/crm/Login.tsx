import React, { Fragment } from 'react';
import Layout from '../../layout/Layout';

const CrmLoginPage = () => {
  return (
    <Layout>
      <Fragment>
        <p>Login Page for CRM.</p>
        <p>call the /token endpoint</p>
        <p>Uses database auth. Not PDA Auth</p>
      </Fragment>
    </Layout>
  );
};

export default CrmLoginPage;
