import React, { ComponentType } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Route } from 'react-router-dom';
import Loading from './Loading';
import { useHistory } from 'react-router';

export interface ProtectedRouteProps {
  Component: ComponentType;
  accessRole?: 'CRM' | 'PDA';
  path?: string;
  exact?: boolean;
  default?: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ Component, accessRole = 'PDA', ...rest }) => {
  const history = useHistory();
  const { role, loading, isAuthenticated } = useAuth();

  if (loading) {
    return <Loading />;
  }

  if (!isAuthenticated) history.push('/');

  if (role !== accessRole) return <div>Not found</div>;

  return (
    <Route {...rest}>
      <Component {...rest} />
    </Route>
  );
};

export default ProtectedRoute;
