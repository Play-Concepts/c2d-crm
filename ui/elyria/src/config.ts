const APPLICATION_ID = 'ld-s-cityofelyriaidentitypassport';
const NAMESPACE = '';
const REDIRECT_URI = `${window.location.origin + '/auth/callback'}`;
const PDA_AUTH_BASE_URL = 'https://hatters.dataswift.io';
const JWT_TOKEN_KEY = 'jwt-token';
const USER_ROLE_KEY = 'user-role';

export const config = {
  pdaAuth: {
    login: `${PDA_AUTH_BASE_URL}/services/login?application_id=${APPLICATION_ID}&redirect_uri=${REDIRECT_URI}`,
    signup: `${PDA_AUTH_BASE_URL}/services/signup?application_id=${APPLICATION_ID}&redirect_uri=${REDIRECT_URI}`,
  },
  namespace: NAMESPACE,
  jwtTokenKey: JWT_TOKEN_KEY,
  userRoleKey: USER_ROLE_KEY,
};
