import React from 'react';
import { Page, PageContent, PageWrapper } from '../styles/templates/PageTemplates';
import NavBar from '../components/NavBar';

type LayoutProps = {
  claimed?: boolean;
};

const Layout: React.FC<LayoutProps> = ({ children, claimed = false }) => {
  return (
    <PageWrapper>
      <NavBar claimed={claimed} />
      <Page>
        <PageContent>{children}</PageContent>
      </Page>
    </PageWrapper>
  );
};
export default Layout;
