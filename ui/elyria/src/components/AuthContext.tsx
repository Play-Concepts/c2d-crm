import React, { useState } from 'react';
import { HatTokenValidation } from '@dataswift/hat-js/lib/utils/HatTokenValidation';

import { config } from '../config';

export const AuthContext = React.createContext({
  user: {
    isAuthenticated: false,
    token: '',
    role: '',
  },
  loginPDA: (token: string) => {},
  logout: () => {},
  loginCRM: (token: string) => {},
});

const AuthProvider: React.FC = ({ children }) => {
  const [user, setUser] = useState({
    isAuthenticated: false,
    token: '',
    role: '',
  });

  return (
    <AuthContext.Provider
      value={{
        user: user,
        loginPDA: (token: string) => {
          if (token && !HatTokenValidation.isEncodedTokenExpired(token)) {
            localStorage.setItem(config.jwtTokenKey, token);
            localStorage.setItem(config.userRoleKey, 'PDA');

            setUser({
              isAuthenticated: true,
              token,
              role: 'PDA',
            });
          }
        },
        logout: () => {
          localStorage.removeItem(config.jwtTokenKey);
          localStorage.removeItem(config.userRoleKey);

          setUser({
            isAuthenticated: false,
            token: '',
            role: '',
          });
        },
        loginCRM: (token: string) => {
          if (token) {
            localStorage.setItem(config.jwtTokenKey, token);
            localStorage.setItem(config.userRoleKey, 'CRM');

            setUser({
              isAuthenticated: true,
              token,
              role: 'CRM',
            });
          }
        },
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
