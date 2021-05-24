import { useContext, useEffect } from 'react';
import { AuthContext } from '../components/AuthContext';
import { config } from '../config';

export const useAuth = () => {
  const { user, loginPDA, logout, loginCRM } = useContext(AuthContext);

  useEffect(() => {
    const token = localStorage.getItem(config.jwtTokenKey);
    const userRole = localStorage.getItem(config.userRoleKey);

    if (!token) return;

    if (userRole === 'CRM') {
      loginCRM(token);
    } else {
      loginPDA(token);
    }
  }, []);
  return {
    ...user,
    loginPDA,
    logout,
    loginCRM,
  };
};
