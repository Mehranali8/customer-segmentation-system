import React from 'react';
import { useLocation } from 'react-router-dom';
import { useTheme } from '../../context/ThemeContext';
import './Header.css';

// SVG Icons for clean, package-free UI design
const SearchIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="search-icon">
    <circle cx="11" cy="11" r="8" />
    <line x1="21" y1="21" x2="16.65" y2="16.65" />
  </svg>
);

const BellIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
    <path d="M13.73 21a2 2 0 0 1-3.46 0" />
  </svg>
);

const SunIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="5" />
    <line x1="12" y1="1" x2="12" y2="3" />
    <line x1="12" y1="21" x2="12" y2="23" />
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
    <line x1="1" y1="12" x2="3" y2="12" />
    <line x1="21" y1="12" x2="23" y2="12" />
    <line x1="4.22" y1="19.22" x2="5.64" y2="17.78" />
    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
  </svg>
);

const MoonIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
  </svg>
);

/**
 * Header Component
 * Provides a responsive top dashboard navigation bar. Dynamically resolves
 * the current page breadcrumb title and handles light/dark theme toggling.
 */
const Header = () => {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();

  const getPageTitle = () => {
    switch (location.pathname) {
      case '/':
        return 'Dashboard';
      case '/search':
        return 'Customer Search';
      case '/prediction':
        return 'Prediction';
      case '/customer-details':
        return 'Customer Details';
      case '/analytics':
        return 'Analytics';
      default:
        return 'Dashboard';
    }
  };

  const pageTitle = getPageTitle();

  return (
    <header className="header">
      <div className="header-left">
        <div className="page-title-container">
          <span className="project-title">Customer Segmentation</span>
          <span className="breadcrumb-separator">/</span>
          <h1 className="page-title">{pageTitle}</h1>
        </div>
      </div>

      <div className="header-right">
        {/* Search Bar Placeholder (UI Only) */}
        <div className="search-bar">
          <SearchIcon />
          <input
            type="text"
            placeholder="Search customers, segments..."
            className="search-input"
            disabled
          />
        </div>

        {/* Notification Button Placeholder (UI Only) */}
        <button type="button" className="notification-btn" aria-label="Notifications">
          <BellIcon />
          <span className="notification-badge" />
        </button>

        {/* Theme Toggle Button */}
        <button
          type="button"
          className="theme-toggle-btn"
          onClick={toggleTheme}
          aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
        >
          {theme === 'light' ? <MoonIcon /> : <SunIcon />}
        </button>

        {/* User Profile Info & Avatar (UI Only) */}
        <div className="user-profile-header">
          <div className="avatar-header">MA</div>
          <span className="user-name-header">Mehran Ali</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
