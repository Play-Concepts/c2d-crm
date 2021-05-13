import { styled } from '@material-ui/core/styles';

export const PageHeader = styled('div')(({ theme }) => ({
  height: '81px',
  maxWidth: '745px',
  color: theme.palette.text.primary,
}));

export const PageWrapper = styled('div')(({ theme }) => ({
  display: 'flex',
  minWidth: theme.breakpoints.values.md,
  minHeight: '100vh',

  background: theme.palette.background.default,
  color: theme.palette.text.primary,
}));

export const Page = styled('div')(() => ({
  display: 'flex',
  flexDirection: 'row',
  maxWidth: '1440px',
  width: '100%',
  justifyContent: 'center',
  alignItems: 'center',
}));

export const PageContent = styled('div')(({ theme }) => ({
  padding: '48px 40px',
  maxWidth: '588px',

  [theme.breakpoints.up('sm')]: {
    padding: '48px 48px 48px 80px',
    minWidth: '145px',
    width: '100%',
    maxWidth: '1118px',
  },

  [theme.breakpoints.up('md')]: {
    padding: '48px 48px 48px 80px',
    minWidth: '645px',
    width: '100%',
    maxWidth: '1118px',
  },
}));
