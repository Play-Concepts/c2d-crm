import React, { useEffect } from 'react';
import { parse } from 'query-string';
import { HatTokenValidation } from '@dataswift/hat-js/lib/utils/HatTokenValidation';
import { useHistory } from 'react-router-dom';
import { config } from '../../config';
import { useAuth } from '../../hooks/useAuth';

type Query = {
  token?: string | null;
};
const AuthCallbackPage: React.FC = () => {
  const history = useHistory();
  const { loginPDA } = useAuth();
  const { token } = parse(window.location.search) as Query;

  useEffect(() => {
    if (!token) return;

    if (!HatTokenValidation.isEncodedTokenExpired(token)) {
      window.localStorage.setItem(config.jwtTokenKey, token);
      loginPDA(token);
      history.replace('/pages/customer/claim');
      return;
    }

    history.replace('/');
  }, [token, history, loginPDA]);

  return <div>Redirecting...</div>;
};

export default AuthCallbackPage;
