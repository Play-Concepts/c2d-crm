export const APPLICATION_ID = 'ld-s-cityofelyriaidentitypassport'

export const ROOT_URL = 'https://hackfromhome.com';
export const BASE_URL = 'https://data.hackfromhome.com';
export const CALLBACK_URL = '<base_url>/auth/callback'.replace('<base_url>', BASE_URL);
export const FALLBACK_URL = '<base_url>/auth/fallback'.replace('<base_url>', BASE_URL);

export const AUTH_ROOT = 'https://auth.dataswift.io/services/login?application_id=<application_id>&redirect_uri=<redirect_uri>'
    .replace('<application_id>', APPLICATION_ID)
    .replace('<redirect_uri>', CALLBACK_URL);
