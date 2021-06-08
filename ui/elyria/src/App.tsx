import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
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
              <Route exact path="/" component={StartPage} />
              <Route exact path="/admin/login" component={CrmLoginPage} />
              <ProtectedRoute exact path="/admin" Component={CrmDashboardPage} accessRole="CRM" />
              <ProtectedRoute exact path="/app" Component={CustomerBasicPage} />
              <ProtectedRoute exact path="/profile" Component={CustomerDetailsPage} />
              <Route exact path="/auth/callback" component={AuthCallbackPage} />
            </Switch>
          </Router>
        </AuthProvider>
      </ModalProvider>
    </ThemeProvider>
  );
};

export default App;
