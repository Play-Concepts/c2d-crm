import React from 'react';
import './NavBar.scss';
import { useAuth } from '../hooks/useAuth';
import { Button, useMediaQuery } from '@material-ui/core';
import { useHistory } from 'react-router-dom';
import { Home } from '@material-ui/icons';

type NavBarProps = {
  claimed?: boolean;
};

const NavBar: React.FC<NavBarProps> = ({ claimed }) => {
  const history = useHistory();
  const matches = useMediaQuery('(min-width:600px)');
  const { isAuthenticated, role, logout } = useAuth();

  return (
    <header>
      <div className="nav-logo-wrapper" onClick={() => history.push('/')}>
        {matches ? <div>City of Elyria Citizens Portal</div> : <Home color="secondary" />}
      </div>
      {isAuthenticated && (
        <div>
          {role === 'PDA' && claimed && (
            <Button
              onClick={() => history.push('/pages/customer/details')}
              color="primary"
              style={{ marginRight: '16px' }}
            >
              Edit Profile
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
