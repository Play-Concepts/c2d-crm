import React from 'react';
import { config } from '../config';
import './NavBar.scss';
import { useAuth } from '../hooks/useAuth';

const NavBar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();

  return (
    <header>
      <div className="nav-logo-wrapper">
        <div>City of Elyria Citizens Portal</div>
      </div>
      {isAuthenticated && (
        <button className="nav-button-sign-out" onClick={logout}>
          Sign out
        </button>
      )}
    </header>
  );
};

export default NavBar;
