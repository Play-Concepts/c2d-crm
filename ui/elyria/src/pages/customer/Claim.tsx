import React from 'react';
import Layout from '../../layout/Layout';

const CustomerClaimPage: React.FC = () => {
  return (
    <Layout>
      <>
        <p>Claim Page for Customers.</p>
        <p>Use endpoint to Search CRM for citizen data.</p>
        <p>Present this data and Write to PDA. Call another endpoint to Flag done.</p>
      </>
    </Layout>
  );
};

export default CustomerClaimPage;
