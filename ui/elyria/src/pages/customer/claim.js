import React, {Fragment} from 'react';
import SingleLayout from "../../layout/single";

const CustomerClaimPage = props => {
    return (
        <SingleLayout>
            <Fragment>
                <p>
                    Claim Page for Customers.
                </p>
                <p>
                    Use endpoint to Search CRM for citizen data.
                </p>
                <p>
                    Present this data and Write to PDA.

                    Call another endpoint to Flag done.
                </p>
            </Fragment>
        </SingleLayout>
    )
}

export default CustomerClaimPage;
