const APPLICATION_ID = '';
const NAMESPACE = '';
const REDIRECT_URI = `${window.location.origin + '/#/auth/callback'}`;
const PDA_AUTH_BASE_URL = '';
const JWT_TOKEN_KEY = 'jwt-token';

export const config = {
  pdaAuth: {
    login: `${PDA_AUTH_BASE_URL}/services/login?application_id=${APPLICATION_ID}&redirect_uri=${REDIRECT_URI}`,
    signup: `${PDA_AUTH_BASE_URL}/services/signup?application_id=${APPLICATION_ID}&redirect_uri=${REDIRECT_URI}`,
  },
  namespace: NAMESPACE,
  jwtTokenKey: JWT_TOKEN_KEY,
};
