import React from 'react';
import { PageHeader } from '../styles/templates/PageTemplates';
import { Typography } from '@material-ui/core';

export const Header: React.FC = () => {
  return (
    <PageHeader>
      <Typography variant="h1">City of Elyria Citizens Portal</Typography>
    </PageHeader>
  );
};
