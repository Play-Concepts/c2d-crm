import React, { useState } from 'react';
import { HatTokenValidation } from '@dataswift/hat-js/lib/utils/HatTokenValidation';

import { config } from '../config';

export const AuthContext = React.createContext({
  user: {
    isAuthenticated: false,
    token: '',
  },
  logoutPDA: () => {},
  loginPDA: (token: string) => {},
  logoutCRM: () => {},
  loginCRM: (token: string) => {},
});

export const AuthProvider: React.FC = ({ children }) => {
  const [user, setUser] = useState({
    isAuthenticated: false,
    token: '',
    role: '',
  });

  return (
    <AuthContext.Provider
      value={{
        user: user,
        logoutPDA: () => {
          localStorage.removeItem(config.jwtTokenKey);

          setUser({
            isAuthenticated: false,
            token: '',
            role: '',
          });
        },
        loginPDA: (token: string) => {
          if (token && !HatTokenValidation.isEncodedTokenExpired(token)) {
            setUser({
              isAuthenticated: true,
              token,
              role: 'PDA',
            });
          }
        },
        logoutCRM: () => {
          localStorage.removeItem(config.jwtTokenKey);

          setUser({
            isAuthenticated: false,
            token: '',
            role: '',
          });
        },
        loginCRM: (token: string) => {
          if (token) {
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
