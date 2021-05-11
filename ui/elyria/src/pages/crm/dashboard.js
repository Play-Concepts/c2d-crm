import React, {Fragment} from 'react';
import SingleLayout from "../../layout/single";

const CrmDashboardPage = props => {
    return (
        <SingleLayout>
            <Fragment>
                <p>
                    Shows Paginated List of All citizens.
                    List should differentiate between Claimed and Not Claimed data.
                </p>
                <p>
                    Page to Handle Upload of CSV file
                </p>
            </Fragment>
        </SingleLayout>
    )
}

export default CrmDashboardPage;
