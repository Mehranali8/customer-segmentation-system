import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import ChartsSection from '../charts/ChartsSection';
import CustomerTable from '../customer/CustomerTable';
import './Dashboard.css';

// SVG Icons for clean, package-free UI design
const UsersIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
    <circle cx="9" cy="7" r="4" />
    <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
    <path d="M16 3.13a4 4 0 0 1 0 7.75" />
  </svg>
);

const SegmentsIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="12 2 2 7 12 12 22 7 12 2" />
    <polyline points="2 17 12 22 22 17" />
    <polyline points="2 12 12 17 22 12" />
  </svg>
);

const RecencyIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" />
    <polyline points="12 6 12 12 16 14" />
  </svg>
);

const MonetaryIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="1" x2="12" y2="23" />
    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
  </svg>
);

/**
 * Dashboard Component
 * Integrates with FastAPI `/dashboard` endpoint to render summary metrics,
 * model distribution charts, and customer profile tables.
 */
const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const response = await api.get('/dashboard');
        setData(response.data);
        setError(null);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
        setError('Could not connect to the analytical engine API. Make sure the backend server is running at http://127.0.0.1:8000.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Analyzing customer segmentation data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error-card">
        <div className="card-glass-effect"></div>
        <svg className="error-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <h3>Connection Error</h3>
        <p>{error}</p>
        <button type="button" className="btn btn-primary" onClick={() => window.location.reload()}>
          Retry Connection
        </button>
      </div>
    );
  }

  // Map API values to card config
  const cards = [
    {
      title: 'Total Customers',
      value: data ? data.total_customers.toLocaleString() : '0',
      desc: 'Active customers analyzed',
      icon: <UsersIcon />,
      color: 'blue'
    },
    {
      title: 'Total Segments',
      value: data ? data.total_segments.toString() : '0',
      desc: 'K-Means clusters identified',
      icon: <SegmentsIcon />,
      color: 'purple'
    },
    {
      title: 'Average Recency',
      value: data ? `${data.average_recency} days` : '0 days',
      desc: 'Days since last purchase',
      icon: <RecencyIcon />,
      color: 'amber'
    },
    {
      title: 'Average Monetary Value',
      value: data ? `£${data.average_monetary.toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : '£0.00',
      desc: 'Lifetime customer spend',
      icon: <MonetaryIcon />,
      color: 'green'
    }
  ];

  return (
    <div className="dashboard-home">
      {/* Welcome Banner */}
      <section className="welcome-banner">
        <div className="welcome-content">
          <h1>Welcome to Customer Segmentation System</h1>
          <p>
            An intelligent analytical engine leveraging machine learning to cluster and explore 
            customer behavior through Recency, Frequency, and Monetary (RFM) statistics.
          </p>
        </div>
        <div className="welcome-badge">
          <span>ML Model Active</span>
        </div>
      </section>

      {/* Summary Cards Grid */}
      <section className="cards-grid">
        {cards.map((card, idx) => (
          <div key={idx} className={`summary-card ${card.color}`}>
            <div className="card-glass-effect"></div>
            <div className="card-header">
              <span className="card-title">{card.title}</span>
              <span className="card-icon">{card.icon}</span>
            </div>
            <div className="card-body">
              <h3 className="card-value">{card.value}</h3>
              <p className="card-desc">{card.desc}</p>
            </div>
          </div>
        ))}
      </section>

      {/* Model Insight Charts Section */}
      <ChartsSection segmentDistribution={data?.segment_distribution} />

      {/* Recent Customer Profiles Table Section */}
      <CustomerTable />
      
      {/* Model Insights Summary */}
      <section className="dashboard-insights">
        <div className="insight-card">
          <h4>Segmentation Model Status</h4>
          <div className="status-grid">
            <div className="status-item">
              <span className="status-label">Algorithm:</span>
              <span className="status-value">K-Means Clustering</span>
            </div>
            <div className="status-item">
              <span className="status-label">Feature Scaling:</span>
              <span className="status-value">StandardScaler</span>
            </div>
            <div className="status-item">
              <span className="status-label">Optimal Clusters (k):</span>
              <span className="status-value">4 (Elbow Method validated)</span>
            </div>
            <div className="status-item">
              <span className="status-label">Dataset:</span>
              <span className="status-value">customer_rfm.csv</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
