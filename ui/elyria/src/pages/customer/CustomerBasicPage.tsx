import React, { useEffect, useState } from 'react';
import Layout from '../../layout/Layout';
import { makeStyles } from '@material-ui/core';
import QRCode from 'qrcode.react';
import { getCustomerBasic } from '../../services/c2dcrm';
import { useAuth } from '../../hooks/useAuth';
import CustomerClaimForm from '../../components/CustomerClaimForm';
import Loading from '../../components/Loading';
import qrcode from 'qrcode.react';

const useStyles = makeStyles({
  root: {
    height: '100%',
    width: '100%',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },
});

const CustomerBasicPage: React.FC = () => {
  const [qrCode, setQrCode] = useState('');
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();
  const classes = useStyles();

  useEffect(() => {
    const fetchCustomerQrCode = async () => {
      try {
        setLoading(true);

        const res = await getCustomerBasic(token);

        if (res.data.id) {
          setQrCode(res.data.id);
        }

        setLoading(false);
      } catch (e) {
        setQrCode('');
        setLoading(false);
      }
    };

    fetchCustomerQrCode();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (loading) return <Loading />;

  return (
    <Layout claimed={!!qrcode}>
      <div className={classes.root}>
        {qrCode ? (
          <QRCode value={qrCode} size={200} data-testid="qr-code" />
        ) : (
          <CustomerClaimForm onCustomerClaim={(claimedCustomer) => setQrCode(claimedCustomer.id)} />
        )}
      </div>
    </Layout>
  );
};

export default CustomerBasicPage;
