import React, {Fragment} from 'react';
import { Route, Redirect} from 'react-router-dom';
import StartPage from "./start";
import CrmLoginPage from "./crm/login";
import CrmDashboardPage from "./crm/dashboard";
import CustomerLoginPage from "./customer/login";
import CustomerClaimPage from "./customer/claim";
import CustomerBasicPage from "./customer/basic";
import CustomerDetailsPage from "./customer/details";
import CustomerEditDetailsPage from "./customer/edit_details";
const MainPage = () => {
    return (
        <Fragment>
            <Route path="/pages/start" component={StartPage} />
            <Route path="/pages/crm/login" component={CrmLoginPage} />
            <Route path="/pages/crm/dashboard" component={CrmDashboardPage} />
            <Route path="/pages/customer/login" component={CustomerLoginPage} />
            <Route path="/pages/customer/claim" component={CustomerClaimPage} />
            <Route path="/pages/customer/basic" component={CustomerBasicPage} />
            <Route path="/pages/customer/details" component={CustomerDetailsPage} />
            <Route path="/pages/customer/details/edit" component={CustomerEditDetailsPage} />
            <Route exact path="/" render={() => (
                <Redirect to="/pages/start"/>
            )}/>
        </Fragment>
    );
};

export default MainPage;