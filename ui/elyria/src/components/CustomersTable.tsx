import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableFooter from '@material-ui/core/TableFooter';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { Button, TableHead } from '@material-ui/core';
import TablePaginationActions from './TablePaginationActions';
import { CrmListCustomersResponse } from '../services/c2dcrm.interface';
import { useModalContext } from './ModalContext';
import CrmClaimedCustomerDetails from './modals/CrmClaimedCustomerDetails';

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
  onPageChange: (page: number, pageCount: number) => void;
};

const CustomersTable: React.FC<CitizensTableProps> = ({ customers, onPageChange }) => {
  const classes = useStyles();
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const { openModal } = useModalContext();

  const emptyRows = rowsPerPage - customers.length;

  const handleChangePage = (event: React.MouseEvent<HTMLButtonElement> | null, newPage: number) => {
    setPage(newPage);
    onPageChange(newPage + 1, rowsPerPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
    onPageChange(1, parseInt(event.target.value, 10));
  };

  const showModal = (rowData: CrmListCustomersResponse) => {
    openModal({
      open: true,
      component: CrmClaimedCustomerDetails,
      componentProps: {
        customerData: rowData,
      },
    });
  };

  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="citizens table">
        <TableHead>
          <TableRow>
            <TableCell align="left">Email</TableCell>
            <TableCell align="left">First Name</TableCell>
            <TableCell align="left">Last Name</TableCell>
            <TableCell align="left">Address</TableCell>
            <TableCell align="left">City</TableCell>
            <TableCell align="left">Status</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {customers.map((row) => (
            <TableRow key={row.id}>
              {row.status === 'claimed' ? (
                <>
                  <TableCell style={{ width: 160 }} align="left">
                    {row.pda_url}
                  </TableCell>
                  <TableCell colSpan={4} style={{ width: 160 }} align="left">
                    <Button className={classes.detailsButton} onClick={() => showModal(row)} color="primary">
                      Details
                    </Button>
                  </TableCell>
                  <TableCell style={{ width: 160 }} align="left">
                    Claimed
                  </TableCell>
                </>
              ) : (
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
                </>
              )}
            </TableRow>
          ))}
          {emptyRows > 0 && (
            <TableRow style={{ height: 53 * emptyRows }}>
              <TableCell colSpan={6} />
            </TableRow>
          )}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TablePagination
              rowsPerPageOptions={[10, 25, 100]}
              colSpan={8}
              count={customers.length > 0 ? customers[0].total_count : 0}
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
