import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { Button, TableHead } from '@material-ui/core';
import { CrmListCustomersResponse } from '../services/c2dcrm.interface';

const useStyles = makeStyles({
  table: {
    minWidth: 500,
  },
  detailsButton: {
    fontSize: '12px',
    marginLeft: '16px',
    padding: 0,
  },
});

type CitizensTableProps = {
  customers: CrmListCustomersResponse[];
  onDataClaim: (customer: CrmListCustomersResponse) => void;
};

const SearchCustomersTable: React.FC<CitizensTableProps> = ({ customers, onDataClaim }) => {
  const classes = useStyles();

  if (customers.length === 0) {
    return null;
  }

  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="custom pagination table">
        <TableHead>
          <TableRow>
            <TableCell align="left">Email</TableCell>
            <TableCell align="left">First Name</TableCell>
            <TableCell align="left">Last Name</TableCell>
            <TableCell align="left">Address</TableCell>
            <TableCell align="left">City</TableCell>
            <TableCell align="left">Status</TableCell>
            <TableCell align="left" />
          </TableRow>
        </TableHead>

        <TableBody>
          {customers.map((row) => (
            <TableRow key={row.id}>
              <>
                <TableCell style={{ width: 160 }} align="left">
                  {row.data.person.contact.email}
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  {row.data.person.profile.first_name}
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  {row.data.person.profile.last_name}
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  {row.data.person.address.address_line_1}
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  {row.data.person.address.city}
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  Unclaimed
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  <Button color="primary" onClick={() => onDataClaim(row)}>
                    Claim
                  </Button>
                </TableCell>
              </>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default SearchCustomersTable;
