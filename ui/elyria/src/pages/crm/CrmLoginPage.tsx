import React, { FormEvent, useState } from 'react';
import { TextField } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Alert from '@material-ui/lab/Alert';
import { useHistory } from 'react-router';

import Layout from '../../layout/Layout';
import useForm from '../../hooks/useForm';
import { crmLogin } from '../../services/c2dcrm';
import { useAuth } from '../../hooks/useAuth';

export interface CrmLoginForm {
  username: string;
  password: string;
}

const CrmLoginPage = () => {
  const history = useHistory();
  const { loginCRM, isAuthenticated } = useAuth();
  const [error, setError] = useState('');
  const { handleChange, inputs } = useForm<CrmLoginForm>({
    username: '',
    password: '',
  });

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      setError('');
      const res = await crmLogin(inputs);

      if (res?.data?.access_token) {
        loginCRM(res.data.access_token);
        history.push('/admin');
      }
    } catch (e) {
      setError('Incorrect username or password.');
    }
  };

  if (isAuthenticated) history.push('/pages/crm/dashboard');

  return (
    <Layout isBusiness={true}>
      <form className="ds-signup-form" onSubmit={handleSubmit}>
        <Grid container direction="column" justify="space-around" alignItems="center" spacing={3}>
          {error && (
            <Grid item>
              <Alert severity="error">{error}</Alert>
            </Grid>
          )}

          <Grid item>
            <TextField
              id="username"
              name="username"
              label="Username"
              variant="outlined"
              className="wideInput"
              value={inputs.username}
              onChange={handleChange}
            />
          </Grid>

          <Grid item>
            <TextField
              id="password"
              name="password"
              label="Password"
              variant="outlined"
              className="wideInput"
              type="password"
              value={inputs.password}
              onChange={handleChange}
            />
          </Grid>

          <Grid item xs={12} sm={8}>
            <Button type="submit" color="primary" variant="contained">
              Access your Data Passport with an Organisation Data Account
            </Button>
          </Grid>
        </Grid>
      </form>
    </Layout>
  );
};

export default CrmLoginPage;
