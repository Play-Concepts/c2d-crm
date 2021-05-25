import React, { useEffect, useState } from 'react';
import Layout from '../../layout/Layout';
import { Button, makeStyles } from '@material-ui/core';
import QRCode from 'qrcode.react';
import { getCustomerBasic } from '../../services/c2dcrm';
import { useAuth } from '../../hooks/useAuth';
import { useHistory } from 'react-router-dom';

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
  const history = useHistory();
  const { isAuthenticated, token } = useAuth();
  const classes = useStyles();

  if (!isAuthenticated) history.push('/');

  useEffect(() => {
    const fetchCustomerQrCode = async () => {
      try {
        const res = await getCustomerBasic(token);
        if (res.data.id) {
          setQrCode(res.data.id);
        }
      } catch (e) {
        setQrCode('');
      }
    };

    fetchCustomerQrCode();
  }, []);

  return (
    <Layout>
      <div className={classes.root}>
        {qrCode ? (
          <>
            <QRCode value={qrCode} />
            <Button color="primary" onClick={() => history.push('/pages/customer/details')}>
              Update your details here!
            </Button>
          </>
        ) : (
          <Button color="primary" onClick={() => history.push('/pages/customer/claim')}>
            Claim your data now!
          </Button>
        )}
      </div>
    </Layout>
  );
};

export default CustomerBasicPage;
