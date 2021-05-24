import React from 'react';
import { Page, PageContent, PageWrapper } from '../styles/templates/PageTemplates';
import NavBar from '../components/NavBar';

const Layout: React.FC = ({ children }) => {
  return (
    <PageWrapper>
      <NavBar />
      <Page>
        <PageContent>{children}</PageContent>
      </Page>
    </PageWrapper>
  );
};
export default Layout;
