import React, {Fragment} from 'react';
import {useLocation} from "react-router-dom";
import SingleLayout from "../layout/single";

const IngestPage = props => {
    const search = useLocation().search;
    const applicationToken = new URLSearchParams(search).get('token');
    const applicationId = localStorage.getItem('application_id');

    return (
        <SingleLayout>
            <Fragment>
                <p>
                    The application token is {applicationToken}.
                </p>
                <p>
                    The application id is {applicationId}
                </p>
            </Fragment>
        </SingleLayout>
    )
}

export default IngestPage;
