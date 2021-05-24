import React from 'react';
import { HashRouter as Router, Redirect, Route, Switch } from 'react-router-dom';
import { ThemeProvider } from '@material-ui/core/styles';

import StartPage from './pages/Start';
import CrmLoginPage from './pages/crm/Login';
import CrmDashboardPage from './pages/crm/Dashboard';
import CustomerLoginPage from './pages/customer/Login';
import CustomerClaimPage from './pages/customer/Claim';
import CustomerBasicPage from './pages/customer/Basic';
import CustomerDetailsPage from './pages/customer/Details';
import CustomerEditDetailsPage from './pages/customer/EditDetails';
import theme from './styles/theme';
import AuthProvider from './components/AuthContext';
import AuthCallbackPage from './pages/AuthCallbackPage/AuthCallbackPage';
import ModalProvider from './components/ModalContext';

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <ModalProvider>
        <AuthProvider>
          <Router>
            <Switch>
              <Route path="/pages/start" component={StartPage} />
              <Route path="/pages/crm/login" component={CrmLoginPage} />
              <Route path="/pages/crm/dashboard" component={CrmDashboardPage} />
              <Route path="/pages/customer/login" component={CustomerLoginPage} />
              <Route path="/pages/customer/claim" component={CustomerClaimPage} />
              <Route path="/pages/customer/basic" component={CustomerBasicPage} />
              <Route path="/pages/customer/details" component={CustomerDetailsPage} />
              <Route path="/pages/customer/details/edit" component={CustomerEditDetailsPage} />
              <Route path="/auth/callback" component={AuthCallbackPage} />
              <Route exact path="/" render={() => <Redirect to="/pages/start" />} />
            </Switch>
          </Router>
        </AuthProvider>
      </ModalProvider>
    </ThemeProvider>
  );
};

export default App;
