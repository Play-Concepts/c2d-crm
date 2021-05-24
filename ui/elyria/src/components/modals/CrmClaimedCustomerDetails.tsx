import React from "react";
import { CrmListCustomersResponse } from "../../services/c2dcrm.interface";
import { Button, Card, CardContent, makeStyles, Typography } from "@material-ui/core";

const useStyles = makeStyles({
  root: {
    minWidth: '400px',
    padding: '10px 20px'
  },
  content: {
    '& p:not(:last-child)': {
      marginBottom: '16px'
    },
    '& h6': {
      fontSize: '16px'
    }
  },
  buttonWrapper: {
    display: 'flex',
    justifyContent: 'center'
  }
});

type CrmClaimedCustomerDetailsProps = {
  customerData: CrmListCustomersResponse;
  onClose: () => void;
}

const CrmClaimedCustomerDetails: React.FC<CrmClaimedCustomerDetailsProps> = ({ customerData, onClose }) => {
  const classes = useStyles();
  const person = customerData.data.person;

  return (
    <Card className={classes.root}>
      <CardContent className={classes.content}>
        <Typography variant='h6'>
          PDA URL
        </Typography>
        <Typography variant='body2'>
          {customerData.pda_url}
        </Typography>

        <Typography variant='h6'>
          Email
        </Typography>
        <Typography variant='body2'>
          {person.contact.email}
        </Typography>

        <Typography variant='h6'>
          First name
        </Typography>
        <Typography variant='body2'>
          {person.profile.first_name}
        </Typography>

        <Typography variant='h6'>
          Last name
        </Typography>
        <Typography variant='body2'>
          {person.profile.last_name}
        </Typography>

        <Typography variant='h6'>
          Address
        </Typography>
        <Typography variant='body2'>
          {person.address.address_line_1}
        </Typography>

        <Typography variant='h6'>
          City
        </Typography>
        <Typography variant='body2'>
          {person.address.city}
        </Typography>

        <Typography variant='h6'>
          Status
        </Typography>
        <Typography variant='body2'>
          Claimed
        </Typography>
        <div className={classes.buttonWrapper}>
          <Button onClick={onClose} color="primary">Close</Button>
        </div>
      </CardContent>
    </Card>
  )
}

export default CrmClaimedCustomerDetails;
