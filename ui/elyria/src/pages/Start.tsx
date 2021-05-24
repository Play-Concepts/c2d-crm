import React from 'react';
import Layout from '../layout/Layout';
import { Button, makeStyles } from '@material-ui/core';
import { config } from '../config';
import { useAuth } from '../hooks/useAuth';
import { useHistory } from 'react-router-dom';

const useStyles = makeStyles({
  root: {
    height: '100%',
    minHeight: '70vh',
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
});

const StartPage: React.FC = () => {
  const history = useHistory();
  const { isAuthenticated } = useAuth();
  const classes = useStyles();

  const onLogin = () => {
    window.location.assign(config.pdaAuth.login);
  };

  if (isAuthenticated) history.push('/pages/customer/basic');

  return (
    <Layout>
      <div className={classes.root}>
        <Button color="secondary" onClick={onLogin}>
          Sign in with a PDA
        </Button>
      </div>
    </Layout>
  );
};

export default StartPage;
