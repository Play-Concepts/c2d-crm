import React, { FormEvent, useEffect, useState } from 'react';
import Layout from '../../layout/Layout';
import { getCustomerDetails, updateCustomerDetails } from '../../services/c2dcrm';
import { useAuth } from '../../hooks/useAuth';
import Grid from '@material-ui/core/Grid';
import Alert from '@material-ui/lab/Alert';
import { TextField } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import { CustomerIdentityResponse } from '../../services/c2dcrm.interface';
import useForm from '../../hooks/useForm';
import { HatRecord } from '@dataswift/hat-js/lib/interfaces/hat-record.interface';

export interface CustomerDetailsForm {
  email: string;
  firstName: string;
  lastName: string;
  address: string;
  city: string;
}

const CustomerDetailsPage = () => {
  const { token, isAuthenticated } = useAuth();
  const [customer, setCustomer] = useState<HatRecord<CustomerIdentityResponse>[]>([]);
  const [successMessage, setSuccessMessage] = useState('');
  const [error, setError] = useState('');

  const { handleChange, inputs, setValues } = useForm<CustomerDetailsForm>({
    email: '',
    firstName: '',
    lastName: '',
    address: '',
    city: '',
  });

  const getDetails = async () => {
    try {
      const res = await getCustomerDetails(token);

      if (res.parsedBody && res.parsedBody.length > 0) {
        const person = res.parsedBody[0].data.person;

        setCustomer(res.parsedBody);
        setValues({
          email: person?.contact.email || '',
          firstName: person?.profile.first_name || '',
          lastName: person?.profile.last_name || '',
          address: person?.address.address_line_1 || '',
          city: person?.address.city || '',
        });
      }
    } catch (e) {
      setError('Something went wrong. Please try again.');
    }
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSuccessMessage('');
    setError('');

    try {
      const residentToUpdate = Object.assign({}, customer[0]);

      residentToUpdate.data.person = {
        profile: {
          first_name: inputs.firstName,
          last_name: inputs.lastName,
        },
        address: {
          address_line_1: inputs.address,
          city: inputs.city,
        },
        contact: {
          email: inputs.email,
        },
      };

      const res = await updateCustomerDetails(token, residentToUpdate);

      if (res.parsedBody && res.parsedBody.length > 0) {
        const person = res.parsedBody[0].data.person;

        setValues({
          email: person?.contact.email || '',
          firstName: person?.profile.first_name || '',
          lastName: person?.profile.last_name || '',
          address: person?.address.address_line_1 || '',
          city: person?.address.city || '',
        });

        setSuccessMessage('Your profile information updated successfully.');
      }
    } catch (e) {
      setError('Something went wrong. Please try again.');
      setSuccessMessage('');
    }
  };

  useEffect(() => {
    getDetails();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated]);

  return (
    <Layout>
      <form className="ds-signup-form" onSubmit={handleSubmit}>
        <Grid container direction="column" justify="space-around" alignItems="center" spacing={3}>
          {successMessage && (
            <Grid item>
              <Alert severity="success">{successMessage}</Alert>
            </Grid>
          )}
          {error && (
            <Grid item>
              <Alert severity="error">{error}</Alert>
            </Grid>
          )}

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
            />
          </Grid>

          <Grid item>
            <TextField
              id="firstName"
              name="firstName"
              label="First name"
              variant="outlined"
              className="wideInput"
              type="text"
              value={inputs.firstName}
              onChange={handleChange}
            />
          </Grid>

          <Grid item>
            <TextField
              id="lastName"
              name="lastName"
              label="Last name"
              variant="outlined"
              className="wideInput"
              type="text"
              value={inputs.lastName}
              onChange={handleChange}
            />
          </Grid>

          <Grid item>
            <TextField
              id="address"
              name="address"
              label="Address"
              variant="outlined"
              className="wideInput"
              type="text"
              value={inputs.address}
              onChange={handleChange}
            />
          </Grid>

          <Grid item>
            <TextField
              id="city"
              name="city"
              label="City"
              variant="outlined"
              className="wideInput"
              type="text"
              value={inputs.city}
              onChange={handleChange}
            />
          </Grid>

          <Grid item xs={12} sm={3}>
            <Button type="submit" color="primary" variant="contained">
              Save
            </Button>
          </Grid>
        </Grid>
      </form>
    </Layout>
  );
};

export default CustomerDetailsPage;
