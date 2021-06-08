import React from 'react';
import './NavBar.scss';
import logo from '../assets/images/elyria-logo.png';
import { useAuth } from '../hooks/useAuth';
import { Button, useMediaQuery } from '@material-ui/core';
import { useHistory } from 'react-router-dom';

type NavBarProps = {
  claimed?: boolean;
  isBusiness?: boolean;
};

const NavBar: React.FC<NavBarProps> = ({ claimed, isBusiness }) => {
  const history = useHistory();
  const matches = useMediaQuery('(min-width:600px)');
  const { isAuthenticated, role, logout } = useAuth();

  return (
    <header>
      <div className="nav-logo-wrapper" onClick={() => history.push('/')}>
        <img src={logo} height="50" width="50" alt={'Elyria logo'} />
          {matches && isBusiness && <div>Elyria Business Data Passport</div>}
          {matches && !isBusiness && <div>Elyria Personal Data Passport</div>}
      </div>
      {isAuthenticated && (
        <div>
          {role === 'PDA' && claimed && (
            <Button onClick={() => history.push('/profile')} color="primary" style={{ marginRight: '16px' }}>
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
