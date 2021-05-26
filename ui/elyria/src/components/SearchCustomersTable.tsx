import React from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { Button, TableHead, useMediaQuery } from '@material-ui/core';
import { CrmListCustomersResponse } from '../services/c2dcrm.interface';

type CitizensTableProps = {
  customers: CrmListCustomersResponse[];
  onDataClaim: (customer: CrmListCustomersResponse) => void;
};

const SearchCustomersTable: React.FC<CitizensTableProps> = ({ customers, onDataClaim }) => {
  const matches = useMediaQuery('(max-width:700px)');

  if (customers.length === 0) {
    return null;
  }

  if (matches) {
    return (
      <TableContainer component={Paper}>
        <Table aria-label="search results table">
          <TableHead>
            <TableRow>
              <TableCell style={{width: 100}}  align="left">Search Result(s)</TableCell>
              <TableCell align="left"/>
            </TableRow>
          </TableHead>

          <TableBody>
            {customers.map((row) => (
              <TableRow key={row.id}>
                <>
                  <TableCell align="left">
                    <ul>
                      <li>{row.data.person.contact.email}</li>
                      <li>{row.data.person.profile.last_name + ' ' + row.data.person.profile.first_name}</li>
                      <li>{row.data.person.address.address_line_1}</li>
                    </ul>
                  </TableCell>
                  <TableCell align="center">
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
  }

  return (
    <TableContainer component={Paper}>
      <Table aria-label="search results table">
        <TableHead>
          <TableRow>
            <TableCell align="left">Email</TableCell>
            <TableCell align="left">First Name</TableCell>
            <TableCell align="left">Last Name</TableCell>
            <TableCell align="left">Address</TableCell>
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
                <TableCell style={{ width: 160 }} align="center">
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
