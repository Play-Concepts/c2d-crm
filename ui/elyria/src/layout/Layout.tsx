import React from 'react';
import { Page, PageContent, PageWrapper } from '../styles/templates/PageTemplates';
import NavBar from '../components/NavBar';
import { Footer } from '../components/Footer';

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
      <Footer />
    </PageWrapper>
  );
};
export default Layout;
