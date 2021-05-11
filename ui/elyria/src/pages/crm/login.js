import React, {Fragment} from 'react';
import SingleLayout from "../../layout/single";

const CrmLoginPage = props => {
    return (
        <SingleLayout>
            <Fragment>
                <p>
                    Login Page for CRM.
                </p>
                <p>
                    call the /token endpoint
                </p>
                <p>
                    Uses database auth. Not PDA Auth
                </p>
            </Fragment>
        </SingleLayout>
    )
}

export default CrmLoginPage;
