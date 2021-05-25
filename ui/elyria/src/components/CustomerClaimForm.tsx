import React, { FormEvent, useState } from 'react';
import Grid from '@material-ui/core/Grid';
import Alert from '@material-ui/lab/Alert';
import { TextField, Typography } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import { useHistory } from 'react-router';
import { useAuth } from '../hooks/useAuth';
import useForm from '../hooks/useForm';
import { claimCustomerData, searchCustomer } from '../services/c2dcrm';
import SearchCustomersTable from './SearchCustomersTable';
import { CrmListCustomersResponse } from '../services/c2dcrm.interface';

export interface CustomerSearchForm {
  email: string;
  last_name: string;
  house_number: string;
}

type CustomerClaimFormProps = {
  onCustomerClaim: (claimedCustomer: CrmListCustomersResponse) => void;
};

const CustomerClaimForm: React.FC<CustomerClaimFormProps> = ({ onCustomerClaim }) => {
  const history = useHistory();
  const [customers, setCustomers] = useState<CrmListCustomersResponse[]>([]);
  const { isAuthenticated, token } = useAuth();
  const [error, setError] = useState('');
  const { handleChange, inputs } = useForm<CustomerSearchForm>({
    email: '',
    last_name: '',
    house_number: '',
  });

  if (!isAuthenticated) history.push('/');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      setError('');
      const res = await searchCustomer(token, inputs);

      if (res.data.length > 0) {
        setCustomers(res?.data);
      } else {
        setError('Records with such details not found.');
        setCustomers([]);
      }
    } catch (e) {
      setCustomers([]);
      setError('Something went wrong. Please try again.');
    }
  };

  const handleCustomerClaim = async (customer: CrmListCustomersResponse) => {
    try {
      setError('');
      const res = await claimCustomerData(token, { id: customer.id });

      if (res.data) {
        onCustomerClaim(res.data);
      } else {
        setCustomers([]);
      }
    } catch (e) {
      setCustomers([]);
      setError('Something went wrong. Please try again.');
    }
  };

  return (
    <form className="ds-signup-form" onSubmit={handleSubmit}>
      <Grid container direction="column" justify="space-around" alignItems="center" spacing={3}>
        {error && (
          <Grid item>
            <Alert severity="error">{error}</Alert>
          </Grid>
        )}

        <Grid item>
          <Typography variant="h6">Search for your data record and claim your data</Typography>
        </Grid>

        <Grid item>
          <TextField
            id="email"
            name="email"
            label="Email"
            variant="outlined"
            className="wideInput"
            type="email"
            value={inputs.email}
            onChange={handleChange}
            required
          />
        </Grid>

        <Grid item>
          <TextField
            id="last_name"
            name="last_name"
            label="Last name"
            variant="outlined"
            className="wideInput"
            type="text"
            value={inputs.last_name}
            onChange={handleChange}
            required
          />
        </Grid>

        <Grid item>
          <TextField
            id="house_number"
            name="house_number"
            label="House number"
            variant="outlined"
            className="wideInput"
            type="text"
            value={inputs.house_number}
            onChange={handleChange}
            required
          />
        </Grid>

        <Grid item xs={12} sm={3}>
          <Button type="submit" color="primary" variant="contained">
            Search
          </Button>
        </Grid>

        <Grid item>
          <SearchCustomersTable customers={customers} onDataClaim={handleCustomerClaim} />
        </Grid>
      </Grid>
    </form>
  );
};

export default CustomerClaimForm;
