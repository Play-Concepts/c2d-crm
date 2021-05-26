import React from 'react';
import { Button, makeStyles } from '@material-ui/core';
import { config } from '../config';
import { useAuth } from '../hooks/useAuth';
import { useHistory } from 'react-router-dom';
import backgroundImage from '../assets/images/background-elyria-city-hall.jpg';
import NavBar from '../components/NavBar';

const useStyles = makeStyles({
  root: {
    height: 'calc(100vh - 82px)',
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundImage: `linear-gradient(rgb(235 1 165 / 12%), rgb(193 153 152 / 72%)), url(${backgroundImage})`,
    backgroundRepeat: 'no-repeat',
    backgroundAttachment: 'fixed',
    backgroundPosition: 'center',
    backgroundSize: 'cover',
  },
});

const StartPage: React.FC = () => {
  const history = useHistory();
  const { isAuthenticated, role } = useAuth();
  const classes = useStyles();

  const onLogin = () => {
    window.location.assign(config.pdaAuth.login);
  };

  if (isAuthenticated) history.push(role === 'CRM' ? '/admin' : '/app');

  return (
    <div>
      <NavBar />
      <div className={classes.root}>
        <Button color="secondary" onClick={onLogin} variant="contained" style={{ marginTop: '100px' }}>
          Sign in with a Personal Data Account
        </Button>
      </div>
    </div>
  );
};

export default StartPage;
