const APPLICATION_ID = 'ld-s-cityofelyriaidentitypassport';
const NAMESPACE = 'elyria';
const ENDPOINT = 'identity';
const REDIRECT_URI = `${window.location.origin + '/auth/callback'}`;
const PDA_AUTH_BASE_URL = 'https://hatters.dataswift.io';
const JWT_TOKEN_KEY = 'jwt-token';
const USER_ROLE_KEY = 'user-role';

export const config = {
  pdaAuth: {
    login: `${PDA_AUTH_BASE_URL}/services/login?application_id=${APPLICATION_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}`,
    signup: `${PDA_AUTH_BASE_URL}/services/signup?application_id=${APPLICATION_ID}&redirect_uri=${REDIRECT_URI}`,
  },
  applicationId: APPLICATION_ID,
  namespace: NAMESPACE,
  endpoint: ENDPOINT,
  jwtTokenKey: JWT_TOKEN_KEY,
  userRoleKey: USER_ROLE_KEY,
};
