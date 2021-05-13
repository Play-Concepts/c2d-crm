import React, { FormEvent } from 'react';
import Layout from '../../layout/Layout';
import { TextField } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import useForm from '../../hooks/useForm';
import { crmLogin } from '../../services/c2dcrm';
import { useHistory } from 'react-router';

export interface CrmLoginForm {
  username: string;
  password: string;
}

const CrmLoginPage = () => {
  const history = useHistory();
  const { handleChange, inputs } = useForm<CrmLoginForm>({
    username: '',
    password: '',
  });

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const res = await crmLogin(inputs);
      if (res) {
        // TODO: Implement authentication
        history.push('/pages/crm/dashboard');
      }
    } catch (e) {
      // TODO: Add error handling
      console.log(e);
    }
  };

  return (
    <Layout>
      <form className="ds-signup-form" onSubmit={handleSubmit}>
        <Grid container direction="column" justify="space-around" alignItems="center" spacing={2}>
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

          <Grid item xs={12} sm={3}>
            <Button type="submit">Login</Button>
          </Grid>
        </Grid>
      </form>
      {/*<Fragment>*/}
      {/*  <p>Login Page for CRM.</p>*/}
      {/*  <p>call the /token endpoint</p>*/}
      {/*  <p>Uses database auth. Not PDA Auth</p>*/}
      {/*</Fragment>*/}
    </Layout>
  );
};

export default CrmLoginPage;
