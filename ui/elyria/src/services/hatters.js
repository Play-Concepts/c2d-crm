import { AUTH_ROOT } from './constants'

export const sign_in = (application_id, redirect_uri) => {
    let url = AUTH_ROOT.replace('<application_id>', application_id).replace('<redirect_uri>', redirect_uri);
    window.open(url, "_self");
};