import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Layout from './components/layout/Layout';
import Dashboard from './components/dashboard/Dashboard';
import CustomerSearch from './pages/CustomerSearch';
import Prediction from './pages/Prediction';
import CustomerDetails from './pages/CustomerDetails';
import Analytics from './pages/Analytics';
import './App.css';

/**
 * Main App Component
 * Configures the ThemeProvider and React Router routing structure inside the Layout wrapper.
 */
function App() {
  return (
    <ThemeProvider>
      <Router>
        <Layout>
        <Routes>
          {/* Main Dashboard Landing Page */}
          <Route path="/" element={<Dashboard />} />

          {/* Customer Search Lookup Page */}
          <Route path="/search" element={<CustomerSearch />} />

          {/* Customer Segment Prediction Page */}
          <Route path="/prediction" element={<Prediction />} />

          {/* Customer Details Page */}
          <Route path="/customer-details" element={<CustomerDetails />} />

          {/* Analytics Page */}
          <Route path="/analytics" element={<Analytics />} />

          {/* Fallback Catch-All Route */}
          <Route path="*" element={
            <div className="content-placeholder">
              <h3>Module Not Found</h3>
              <p>The requested page is currently under development.</p>
            </div>
          } />
        </Routes>
      </Layout>
    </Router>
  </ThemeProvider>
  );
}

export default App;
