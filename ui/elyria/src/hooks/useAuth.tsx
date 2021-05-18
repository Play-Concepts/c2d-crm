import { useContext } from 'react';
import { AuthContext } from '../components/AuthProvider';

export const useAuth = () => {
  const { user, loginPDA, logout, loginCRM } = useContext(AuthContext);

  return {
    ...user,
    loginPDA,
    logout,
    loginCRM,
  };
};
