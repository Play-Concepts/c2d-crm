import React, {Fragment} from 'react';
import { Route, Redirect} from 'react-router-dom';
import StartPage from "./start";
import IngestPage from "./ingest";
import ConfirmPage from "./confirm";
const MainPage = () => {
    return (
        <Fragment>
            <Route path="/pages/start" component={StartPage} />
            <Route path="/pages/ingest" component={IngestPage} />
            <Route path="/pages/confirm" component={ConfirmPage} />
            <Route exact path="/" render={() => (
                <Redirect to="/pages/start"/>
            )}/>
        </Fragment>
    );
};

export default MainPage;