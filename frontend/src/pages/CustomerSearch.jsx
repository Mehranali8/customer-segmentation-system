import React, { useState } from 'react';
import api from '../services/api';
import './CustomerSearch.css';

// SVG Search Icon for table search bar
const TableSearchIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="input-icon">
    <circle cx="11" cy="11" r="8" />
    <line x1="21" y1="21" x2="16.65" y2="16.65" />
  </svg>
);

/**
 * CustomerSearch Component
 * Renders the Customer Profile Lookup page. Connects with the FastAPI /customer/{id}
 * endpoint to fetch live customer records and display segments and RFM statistics.
 */
const CustomerSearch = () => {
  const [customerId, setCustomerId] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [result, setResult] = useState(null);

  // Helper to resolve customer status based on unscaled Recency days
  const resolveStatus = (recency) => {
    if (recency <= 30) return 'Active';
    if (recency <= 90) return 'Recent';
    if (recency <= 180) return 'Inactive';
    return 'Dormant';
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    const queryId = customerId.trim();
    if (queryId === '') return;

    // Validate Customer ID format
    const parsedId = parseInt(queryId, 10);
    if (isNaN(parsedId) || parsedId <= 0 || parsedId.toString() !== queryId) {
      setError('Please enter a valid positive integer Customer ID.');
      setShowResult(false);
      setSuccessMessage(null);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setSuccessMessage(null);

      // GET request to FastAPI customer search endpoint
      const response = await api.get(`/customer/${parsedId}`);
      setResult(response.data);
      setSuccessMessage(`Found customer profile #${parsedId}.`);
      setShowResult(true);
    } catch (err) {
      console.error('Customer query failed:', err);
      setShowResult(false);
      setResult(null);

      if (err.status === 404) {
        setError('No customer found matching the specified ID.');
      } else if (err.data && err.data.detail) {
        setError(`API Error: ${err.data.detail}`);
      } else {
        setError('Unable to reach search service. Please check if backend server is online.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setCustomerId('');
    setShowResult(false);
    setError(null);
    setSuccessMessage(null);
    setResult(null);
  };

  const status = result ? resolveStatus(result.recency) : '';

  return (
    <div className="customer-search-page">
      <div className="search-page-header">
        <h2 className="search-page-title">Customer Profile Lookup</h2>
        <p className="search-page-subtitle">
          Enter a Customer ID to retrieve segment classification, recency, frequency, and monetary statistics.
        </p>
      </div>

      {/* Alert Banners */}
      {error && <div className="search-alert error">{error}</div>}
      {successMessage && <div className="search-alert success">{successMessage}</div>}

      {/* Search Input Card */}
      <div className="search-card">
        <div className="card-glass-effect"></div>
        <form onSubmit={handleSearch} className="search-form">
          <div className="form-group">
            <label htmlFor="customerId" className="form-label">Customer ID</label>
            <div className="input-wrapper">
              <TableSearchIcon />
              <input
                type="text"
                id="customerId"
                className="form-input"
                placeholder="e.g., 17850"
                value={customerId}
                onChange={(e) => setCustomerId(e.target.value)}
                disabled={loading}
                required
              />
            </div>
          </div>
          
          <div className="form-actions">
            <button 
              type="submit" 
              className="btn btn-primary" 
              disabled={loading || customerId.trim() === ''}
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={handleReset}
              disabled={loading}
            >
              Reset
            </button>
          </div>
        </form>
      </div>

      {/* Search Result Card */}
      {showResult && result && (
        <div className="result-card fade-in">
          <div className="card-glass-effect"></div>
          
          <div className="result-header">
            <div className="result-title-group">
              <span className="result-badge">Profile Match</span>
              <h3 className="result-customer-id">Customer #{result.customer_id}</h3>
            </div>
            <span className={`status-indicator ${status.toLowerCase()}`}>
              {status}
            </span>
          </div>

          <div className="result-grid">
            <div className="result-item highlight">
              <span className="result-label">Assigned Segment</span>
              <span className="result-value segment-premium">{result.segment}</span>
            </div>
            <div className="result-item">
              <span className="result-label">Recency</span>
              <span className="result-value">{result.recency} Days ago</span>
            </div>
            <div className="result-item">
              <span className="result-label">Frequency</span>
              <span className="result-value">{result.frequency} Orders</span>
            </div>
            <div className="result-item">
              <span className="result-label">Monetary Value</span>
              <span className="result-value value-monetary">
                £{result.monetary.toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </span>
            </div>
          </div>

          <div className="result-footer-notes">
            <p>
              <strong>Note:</strong> Customer belongs to Cluster {result.cluster} ({result.segment}).
              Model properties indicate targeted campaigns can be tailored to this RFM score.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomerSearch;
