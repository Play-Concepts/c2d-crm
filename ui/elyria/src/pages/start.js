import React, {Fragment} from 'react';
import SingleLayout from "../layout/single";
import { sign_in} from "../services/hatters";
import {CALLBACK_URL} from "../services/constants";

const StartPage = () => {
    const [application_id, set_application_id] = React.useState('');

    const handleChange = (e, { value}) => set_application_id(value);

    const handleClick = () => {
        localStorage.setItem('application_id', application_id);
        sign_in(application_id, CALLBACK_URL);
    }

    return (
        <SingleLayout>
            <Fragment>
                Start Page
            </Fragment>
        </SingleLayout>
    )
}

export default StartPage;
