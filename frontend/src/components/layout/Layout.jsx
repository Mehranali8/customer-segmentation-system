import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import './Layout.css';

/**
 * Layout Component
 * Provides a responsive dashboard frame containing a Sidebar, Header, Main Content, and Footer.
 * Interoperates with React Router context for navigation highlights.
 */
const Layout = ({ children }) => {
  return (
    <div className="dashboard-container">
      {/* Sidebar Section */}
      <Sidebar />

      {/* Main Wrapper */}
      <div className="dashboard-main">
        {/* Header Section */}
        <Header />

        {/* Main Content Section */}
        <main className="dashboard-content">
          {children || (
            <div className="content-placeholder">
              Main Content Placeholder
            </div>
          )}
        </main>

        {/* Optional Footer Placeholder Section */}
        <footer className="dashboard-footer">
          Footer Placeholder
        </footer>
      </div>
    </div>
  );
};

export default Layout;
