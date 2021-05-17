import { useContext } from 'react';
import { AuthContext } from '../components/AuthProvider';

export const useAuth = () => {
  const { user, loginPDA, logoutPDA, loginCRM, logoutCRM } = useContext(AuthContext);

  return {
    ...user,
    loginPDA,
    logoutPDA,
    loginCRM,
    logoutCRM,
  };
};
