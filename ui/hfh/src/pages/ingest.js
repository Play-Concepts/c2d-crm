import React from 'react';
import {useLocation} from "react-router-dom";

const IngestPage = () => {
    const search = useLocation().search;
    const applicationToken = new URLSearchParams(search).get('token');

    return (
        <div>Ingest Page {applicationToken}</div>
    )
}

export default IngestPage;
