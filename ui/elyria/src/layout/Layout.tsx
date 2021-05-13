import React from 'react';
import { Page, PageContent, PageWrapper } from '../styles/templates/PageTemplates';

const Layout: React.FC = ({ children }) => {
  return (
    <PageWrapper>
      <Page>
        <PageContent>{children}</PageContent>
      </Page>
    </PageWrapper>
  );
};
export default Layout;
