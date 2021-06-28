import React from 'react';
import { Link, makeStyles, Typography } from '@material-ui/core';
import { config } from '../config';

const useStyles = makeStyles({
  root: {
    borderTop: '1px solid #9a9a9a',
    minHeight: '120px',
    width: '100%',
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  legalsList: {
    marginBottom: '10px',
    listStyle: 'none',
    padding: 0,
    margin: 0,
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-around',

    '& li:not(:last-child)': {
      marginRight: '16px',
    },

    '& a': {
      textDecoration: 'none',
    },
  },
});

export const Footer: React.FC = () => {
  const classes = useStyles();

  return (
    <footer className={classes.root}>
      <div>
        <ul className={classes.legalsList}>
          <li>
            <Link href={config.privacyPolicy} color="primary">
              Privacy Policy
            </Link>
          </li>
          <li>
            <Link href={config.termsOfService} color="primary">
              Terms of Service
            </Link>
          </li>
        </ul>

        <Typography align="center">Copyright &#169; {new Date().getFullYear()} City of Elyria</Typography>
      </div>
    </footer>
  );
};
