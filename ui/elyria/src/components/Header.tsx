import React from 'react';
// @ts-ignore
import logo from '../assets/images/logo.png';
import { ROOT_URL } from '../services/constants';

export const Header: React.FC = () => {
  const handleLogoClick = () => (window.location.href = ROOT_URL);

  return (
    <div>
      Put your header here.
      <img src={logo} alt="logo" onClick={handleLogoClick} />
    </div>
  );
};
