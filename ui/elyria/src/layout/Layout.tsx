import React from 'react';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';

const Layout: React.FC = ({ children }) => {
  return (
    <div>
      <Header />
      <div>This is where you code your Layout</div>
      {children}
      <Footer />
    </div>
  );
};
export default Layout;
