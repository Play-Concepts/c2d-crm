import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableFooter from '@material-ui/core/TableFooter';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { TableHead } from '@material-ui/core';
import TablePaginationActions from './TablePaginationActions';
import { CrmCustomerInterface } from '../services/c2dcrm.interface';

const useStyles = makeStyles({
  table: {
    minWidth: 500,
  },
});

type CitizensTableProps = {
  customers: CrmCustomerInterface[];
};

const CustomersTable: React.FC<CitizensTableProps> = ({ customers }) => {
  const classes = useStyles();
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);

  const emptyRows = rowsPerPage - Math.min(rowsPerPage, customers.length - page * rowsPerPage);

  const handleChangePage = (event: React.MouseEvent<HTMLButtonElement> | null, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

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
            <TableCell align="left">ID</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {(rowsPerPage > 0 ? customers.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage) : customers).map(
            (row) => (
              <TableRow key={row.id}>
                <TableCell style={{ width: 160 }} align="left">
                  {row.contact.email}
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  {row.profile.first_name}
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  {row.profile.last_name}
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  {row.address.address_line_1}
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  {row.address.city}
                </TableCell>
                <TableCell style={{ width: 160 }} align="left">
                  {row.id}
                </TableCell>
              </TableRow>
            ),
          )}
          {emptyRows > 0 && (
            <TableRow style={{ height: 53 * emptyRows }}>
              <TableCell colSpan={6} />
            </TableRow>
          )}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TablePagination
              rowsPerPageOptions={[5, 10, 25, { label: 'All', value: -1 }]}
              colSpan={3}
              count={customers.length}
              rowsPerPage={rowsPerPage}
              page={page}
              SelectProps={{
                inputProps: { 'aria-label': 'rows per page' },
                native: true,
              }}
              onChangePage={handleChangePage}
              onChangeRowsPerPage={handleChangeRowsPerPage}
              ActionsComponent={TablePaginationActions}
            />
          </TableRow>
        </TableFooter>
      </Table>
    </TableContainer>
  );
};

export default CustomersTable;
