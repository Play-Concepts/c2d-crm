import React from 'react';
import { BrowserRouter as Router, Redirect, Route, Switch } from 'react-router-dom';
import { ThemeProvider } from '@material-ui/core/styles';

import StartPage from './pages/Start';
import CrmLoginPage from './pages/crm/Login';
import CrmDashboardPage from './pages/crm/Dashboard';
import CustomerClaimPage from './pages/customer/Claim';
import CustomerBasicPage from './pages/customer/Basic';
import CustomerDetailsPage from './pages/customer/Details';
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
              <Route exact path="/pages/start" component={StartPage} />
              <Route exact path="/pages/crm/login" component={CrmLoginPage} />
              <Route exact path="/pages/crm/dashboard" component={CrmDashboardPage} />
              <Route exact path="/pages/customer/claim" component={CustomerClaimPage} />
              <Route exact path="/pages/customer/basic" component={CustomerBasicPage} />
              <Route exact path="/pages/customer/details" component={CustomerDetailsPage} />
              <Route exact path="/auth/callback" component={AuthCallbackPage} />
              <Route exact path="/admin" render={() => <Redirect to="/pages/crm/login" />} />
              <Route exact path="/" render={() => <Redirect to="/pages/start" />} />
            </Switch>
          </Router>
        </AuthProvider>
      </ModalProvider>
    </ThemeProvider>
  );
};

export default App;
