import React from 'react';
import logo from '../assets/images/dataswift-logo.png';
import { useAuth } from '../hooks/useAuth';
import { Button, makeStyles, useMediaQuery } from '@material-ui/core';
import { useHistory } from 'react-router-dom';

type NavBarProps = {
  claimed?: boolean;
  isBusiness?: boolean;
};

const useStyles = makeStyles({
  root: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    height: '81px',
    borderBottom: '1px solid #9a9a9a',
    alignItems: 'center',
    padding: '0 16px',
  },
  navLogoWrapper: {
    display: 'flex',
    cursor: 'pointer',
    flexDirection: 'row',
    alignItems: 'center',
    fontSize: '14px',
    fontWeight: 700,

    '@media(max-width: 600px)': {
      fontSize: '12px',
    },

    '& img': {
      marginRight: '18px',
    },
  },
  actionsWrapper: {
    display: 'flex',
    flexDirection: 'row',

    '& button': {
      fontSize: '14px',

      '@media(max-width: 600px)': {
        fontSize: '12px',
      },
    },
  },
});

const NavBar: React.FC<NavBarProps> = ({ claimed, isBusiness }) => {
  const classes = useStyles();
  const history = useHistory();
  const matches = useMediaQuery('(min-width:350px)');
  const { isAuthenticated, role, logout } = useAuth();

  return (
    <header className={classes.root}>
      <div className={classes.navLogoWrapper} onClick={() => history.push('/')}>
        <img src={logo} height="16" alt={'Dataswift logo'} />
          {matches && isBusiness && <div>Business Data Passport</div>}
          {matches && !isBusiness && <div>Personal Data Passport</div>}
      </div>
      {isAuthenticated && (
        <div className={classes.actionsWrapper}>
          {role === 'PDA' && claimed && (
            <Button onClick={() => history.push('/profile')} color="primary" style={{ marginRight: '16px' }}>
              Profile
            </Button>
          )}
          <Button onClick={logout} color="primary" variant="contained">
            Sign out
          </Button>
        </div>
      )}
    </header>
  );
};

export default NavBar;
