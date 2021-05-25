import React, { useEffect } from 'react';
import { parse } from 'query-string';
import { HatTokenValidation } from '@dataswift/hat-js/lib/utils/HatTokenValidation';
import { useHistory, useLocation } from 'react-router-dom';
import { config } from '../../config';
import { useAuth } from '../../hooks/useAuth';
import Loading from '../../components/Loading';

type Query = {
  token?: string | null;
};

const AuthCallbackPage: React.FC = () => {
  const history = useHistory();
  const location = useLocation();
  const { loginPDA } = useAuth();
  const { token } = parse(location.search) as Query;

  useEffect(() => {
    if (!token) return;

    const decodedToken = HatTokenValidation.decodeToken(token);

    if (!HatTokenValidation.isEncodedTokenExpired(token) && decodedToken.application === config.applicationId) {
      window.localStorage.setItem(config.jwtTokenKey, token);
      loginPDA(token);
      history.replace('/pages/customer/basic');
      return;
    }

    history.replace('/');
  }, [token, history, loginPDA]);

  return <Loading />;
};

export default AuthCallbackPage;
