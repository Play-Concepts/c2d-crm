import React from 'react';
import { BrowserRouter as Router, Redirect, Route, Switch } from 'react-router-dom';
import { ThemeProvider } from '@material-ui/core/styles';

import StartPage from './pages/Start';
import CrmLoginPage from './pages/crm/CrmLoginPage';
import CrmDashboardPage from './pages/crm/Dashboard';
import CustomerBasicPage from './pages/customer/CustomerBasicPage';
import CustomerDetailsPage from './pages/customer/CustomerDetailsPage';
import theme from './styles/theme';
import AuthProvider from './components/AuthContext';
import AuthCallbackPage from './pages/AuthCallbackPage/AuthCallbackPage';
import ModalProvider from './components/ModalContext';
import ProtectedRoute from './components/ProtectedRoute';

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <ModalProvider>
        <AuthProvider>
          <Router>
            <Switch>
              <Route exact path="/pages/start" component={StartPage} />
              <Route exact path="/pages/crm/login" component={CrmLoginPage} />
              <ProtectedRoute exact path="/pages/crm/dashboard" Component={CrmDashboardPage} accessRole="CRM" />
              <ProtectedRoute exact path="/pages/customer/basic" Component={CustomerBasicPage} />
              <ProtectedRoute exact path="/pages/customer/details" Component={CustomerDetailsPage} />
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
