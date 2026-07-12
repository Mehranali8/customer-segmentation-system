import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './CustomerDetails.css';

/**
 * CustomerDetails Component
 * Renders the Customer Profile details page. Dynamically fetches customer
 * profile parameters, unscaled RFM properties, cluster assignments, and recency-based status
 * from the FastAPI /customer-details/{id} backend endpoint.
 */
const CustomerDetails = () => {
  const [searchId, setSearchId] = useState('14911');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Core profile loading function
  const fetchProfile = async (idToFetch) => {
    const queryId = idToFetch.toString().trim();
    if (queryId === '') return;

    // Validate Customer ID format
    const parsedId = parseInt(queryId, 10);
    if (isNaN(parsedId) || parsedId <= 0 || parsedId.toString() !== queryId) {
      setError('Please enter a valid positive integer Customer ID.');
      setData(null);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // GET request to backend customer details profile endpoint
      const response = await api.get(`/customer-details/${parsedId}`);
      setData(response.data);
    } catch (err) {
      console.error('Failed to load profile details:', err);
      setData(null);

      if (err.status === 404) {
        setError('No customer profile found matching the specified ID.');
      } else if (err.data && err.data.detail) {
        setError(`API Error: ${err.data.detail}`);
      } else {
        setError('Connection timed out. Please verify that the FastAPI backend is running.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Load VIP Customer 14911 as default profile on mount
  useEffect(() => {
    fetchProfile('14911');
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchProfile(searchId);
  };

  // Helper to extract avatar initials
  const getAvatarInitials = (segment) => {
    if (!segment) return 'JD';
    const words = segment.split(' ');
    if (words.length >= 2) {
      return `${words[0][0]}${words[1][0]}`.toUpperCase();
    }
    return segment.substring(0, 2).toUpperCase();
  };

  // Dynamic behaviors mapping based on segment classification
  const getBehaviors = (segment) => {
    switch (segment) {
      case 'VIP Customers':
        return [
          'Highly active customer',
          'Frequently purchases products',
          'High spending customer',
          'Recommended for loyalty campaigns'
        ];
      case 'Premium Customers':
        return [
          'Steady buyer with high order averages',
          'Sustained frequency patterns',
          'High-value lifetime spend contributor',
          'Recommended for premier upgrade offerings'
        ];
      case 'Regular Customers':
        return [
          'Standard purchase frequency',
          'Average basket spending averages',
          'Normal active transaction window',
          'Recommended for seasonal promotional campaigns'
        ];
      case 'At Risk Customers':
        return [
          'Low engagement frequency detected',
          'Prolonged lapse between transaction history',
          'Dormancy classification boundary risk',
          'Recommended for urgent winback activation discount offers'
        ];
      default:
        return [
          'Standard shopping behavior indexing',
          'Normal transactional frequency',
          'Average cumulative monetary contributions',
          'Target with general digital marketing campaigns'
        ];
    }
  };

  // Dynamic recommendations mapping based on segment classification
  const getRecommendations = (segment) => {
    switch (segment) {
      case 'VIP Customers':
        return [
          'VIP email campaigns',
          'Early access promotions',
          'Loyalty rewards',
          'Personal account management'
        ];
      case 'Premium Customers':
        return [
          'Offer premium discounts',
          'Loyalty rewards',
          'VIP email campaigns',
          'Early access promotions'
        ];
      case 'Regular Customers':
        return [
          'Standard discount coupons',
          'Cross-sell suggestions',
          'Weekly newsletters',
          'Feedback survey emails'
        ];
      case 'At Risk Customers':
        return [
          'Offer high-value winback discounts',
          'Direct reactivation email triggers',
          'Feedback and satisfaction surveys',
          'Product recommendation digests'
        ];
      default:
        return [
          'General discount coupons',
          'Seasonal promotional updates',
          'Standard monthly newsletters',
          'Support portal links'
        ];
    }
  };

  const behaviors = data ? getBehaviors(data.segment) : [];
  const recommendations = data ? getRecommendations(data.segment) : [];
  const avatar = data ? getAvatarInitials(data.segment) : 'JD';

  return (
    <div className="customer-details-page">
      <div className="search-page-header">
        <h2 className="search-page-title">Customer Profile Details</h2>
        <p className="search-page-subtitle">
          Query the analytical data warehouse directly to inspect model outputs, status indicators, and recommendation paths.
        </p>
      </div>

      {/* Customer ID Selector form */}
      <div className="details-search-card">
        <div className="card-glass-effect"></div>
        <form onSubmit={handleSearchSubmit} className="details-search-form">
          <label htmlFor="searchId" className="details-search-label">Select Customer ID Profile:</label>
          <div className="details-search-input-wrapper">
            <input
              type="text"
              id="searchId"
              className="details-search-input"
              placeholder="Enter Customer ID (e.g., 14911)"
              value={searchId}
              onChange={(e) => setSearchId(e.target.value)}
              disabled={loading}
              required
            />
            <button type="submit" className="btn btn-primary" disabled={loading || searchId.trim() === ''}>
              {loading ? 'Loading...' : 'Load Profile'}
            </button>
          </div>
        </form>
      </div>

      {/* Alert Banner */}
      {error && <div className="details-alert error">{error}</div>}

      {/* Loading state display */}
      {loading && (
        <div className="details-loader">
          <div className="details-spinner"></div>
          <p>Fetching profile analytics...</p>
        </div>
      )}

      {/* Profile Breakdown grid (only rendered when data is present) */}
      {!loading && data && (
        <div className="profile-container fade-in">
          {/* Profile Header Banner */}
          <div className="profile-header-card">
            <div className="card-glass-effect"></div>
            <div className="profile-banner-info">
              <div className="profile-avatar">{avatar}</div>
              <div className="profile-title-group">
                <span className="profile-meta">Customer Profile</span>
                <h2 className="profile-name">Customer #{data.customer_id}</h2>
                <div className="profile-badges">
                  <span className="badge-tag segment-vip">{data.segment}</span>
                  <span className="badge-tag status-active">{data.customer_status}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Grid Layout for Profile Details */}
          <div className="details-grid" style={{ marginTop: '24px' }}>
            {/* Info Column */}
            <div className="details-card info-card">
              <div className="card-glass-effect"></div>
              <h3 className="card-heading">Demographics & RFM Metrics</h3>
              <div className="info-list">
                <div className="info-row">
                  <span className="info-label">Customer ID</span>
                  <span className="info-value font-mono">#{data.customer_id}</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Model Cluster Assignment</span>
                  <span className="info-value">Cluster {data.cluster}</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Segment Category</span>
                  <span className="info-value text-accent">{data.segment}</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Recency Index</span>
                  <span className="info-value">{data.recency} Days ago</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Frequency Index</span>
                  <span className="info-value">{data.frequency} Purchases</span>
                </div>
                <div className="info-row">
                  <span className="info-label">Monetary Valuation</span>
                  <span className="info-value font-mono font-bold">
                    £{data.monetary.toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="info-row">
                  <span className="info-label">Relationship Status</span>
                  <span className="info-value status-text-active">{data.customer_status}</span>
                </div>
              </div>
            </div>

            {/* Behavior and Recommendations Column */}
            <div className="analysis-column">
              {/* Behavior Summary Card */}
              <div className="details-card behavior-card">
                <div className="card-glass-effect"></div>
                <h3 className="card-heading">Behavior Summary</h3>
                <ul className="bullet-list behavior-list">
                  {behaviors.map((item, idx) => (
                    <li key={idx} className="bullet-item">
                      <svg className="bullet-icon check" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Recommendations Card */}
              <div className="details-card recommendations-card">
                <div className="card-glass-effect"></div>
                <h3 className="card-heading">Recommended Actions</h3>
                <ul className="bullet-list action-list">
                  {recommendations.map((item, idx) => (
                    <li key={idx} className="bullet-item">
                      <svg className="bullet-icon target" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <circle cx="12" cy="12" r="10" />
                        <circle cx="12" cy="12" r="6" />
                        <circle cx="12" cy="12" r="2" />
                      </svg>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomerDetails;
