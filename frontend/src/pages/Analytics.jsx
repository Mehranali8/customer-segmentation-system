import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './Analytics.css';

// SVG Icons for clean, package-free UI design
const MonetaryIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="1" x2="12" y2="23" />
    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
  </svg>
);

const FrequencyIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="9" cy="21" r="1" />
    <circle cx="20" cy="21" r="1" />
    <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" />
  </svg>
);

const ClockIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" />
    <polyline points="12 6 12 12 16 14" />
  </svg>
);

const TrendIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
    <polyline points="17 6 23 6 23 12" />
  </svg>
);

/**
 * Analytics Component
 * Renders K-Means cluster statistics (Recency, Frequency, Monetary averages) and behavioral observations.
 */
const Analytics = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const response = await api.get('/analytics');
        setData(response.data);
        setError(null);
      } catch (err) {
        console.error('Failed to load analytics data:', err);
        setError('Could not connect to the analytical engine API. Make sure the backend server is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="analytics-loading">
        <div className="loading-spinner"></div>
        <p>Calculating behavioral segment analytics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="analytics-error-card">
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

  const { cluster_metrics, insights } = data;

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h2 className="analytics-title">Cluster & Segment Analysis</h2>
        <p className="analytics-subtitle">
          In-depth statistical evaluation and behavioral insights computed from unscaled RFM averages for each K-Means cluster.
        </p>
      </div>

      {/* Cluster Metrics Table */}
      <div className="customer-table-card">
        <div className="card-glass-effect"></div>
        <div className="table-header">
          <h3 className="table-title">K-Means Cluster Performance (Original Scale Averages)</h3>
        </div>
        <div className="table-responsive-container">
          <table className="customer-data-table">
            <thead>
              <tr>
                <th>Cluster</th>
                <th>Segment Name</th>
                <th>Avg Recency</th>
                <th>Avg Frequency</th>
                <th>Avg Monetary Value</th>
                <th>Customer Count</th>
                <th>Percentage</th>
              </tr>
            </thead>
            <tbody>
              {cluster_metrics.map((metric) => (
                <tr key={metric.cluster_id}>
                  <td className="cust-id">Cluster #{metric.cluster_id}</td>
                  <td>
                    <span className={`segment-badge ${metric.segment_name.toLowerCase().replace(' ', '-')}`}>
                      {metric.segment_name}
                    </span>
                  </td>
                  <td>{metric.avg_recency} days</td>
                  <td>{metric.avg_frequency} orders</td>
                  <td className="monetary-val">£{metric.avg_monetary.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                  <td>{metric.count.toLocaleString()}</td>
                  <td className="monetary-val">{metric.percentage}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Behavioral Insights Section */}
      <div className="insights-section">
        <h3 className="insights-section-title">Key Segment Insights & Recommendations</h3>
        <div className="insights-grid">
          
          {/* Highest Spending */}
          <div className="insight-card">
            <div className="card-glass-effect"></div>
            <div className="insight-icon-wrapper purple">
              <MonetaryIcon />
            </div>
            <div className="insight-content">
              <h4 className="insight-card-title">Highest Spending Segment</h4>
              <p className="insight-segment-name">{insights.highest_spending.segment_name} (Cluster {insights.highest_spending.cluster_id})</p>
              <div className="insight-stats">
                <div className="insight-stat"><span className="stat-label">Avg Spend:</span> <span className="stat-val">£{insights.highest_spending.avg_monetary.toLocaleString()}</span></div>
                <div className="insight-stat"><span className="stat-label">Frequency:</span> <span className="stat-val">{insights.highest_spending.avg_frequency} orders</span></div>
                <div className="insight-stat"><span className="stat-label">Size:</span> <span className="stat-val">{insights.highest_spending.count.toLocaleString()} customers ({insights.highest_spending.percentage}%)</span></div>
              </div>
              <p className="insight-recommendation">
                <strong>Marketing Strategy:</strong> Target with exclusive VIP rewards, high-tier early access, and customized loyalty initiatives.
              </p>
            </div>
          </div>

          {/* Most Frequent */}
          <div className="insight-card">
            <div className="card-glass-effect"></div>
            <div className="insight-icon-wrapper blue">
              <FrequencyIcon />
            </div>
            <div className="insight-content">
              <h4 className="insight-card-title">Most Frequent Purchasing Segment</h4>
              <p className="insight-segment-name">{insights.most_frequent.segment_name} (Cluster {insights.most_frequent.cluster_id})</p>
              <div className="insight-stats">
                <div className="insight-stat"><span className="stat-label">Avg Orders:</span> <span className="stat-val">{insights.most_frequent.avg_frequency} orders</span></div>
                <div className="insight-stat"><span className="stat-label">Avg Spend:</span> <span className="stat-val">£{insights.most_frequent.avg_monetary.toLocaleString()}</span></div>
                <div className="insight-stat"><span className="stat-label">Size:</span> <span className="stat-val">{insights.most_frequent.count.toLocaleString()} customers ({insights.most_frequent.percentage}%)</span></div>
              </div>
              <p className="insight-recommendation">
                <strong>Marketing Strategy:</strong> Offer subscription packages, recurring checkout incentives, and volume-based discounts to maintain purchase frequency.
              </p>
            </div>
          </div>

          {/* Least Active (Highest Recency) */}
          <div className="insight-card">
            <div className="card-glass-effect"></div>
            <div className="insight-icon-wrapper amber">
              <ClockIcon />
            </div>
            <div className="insight-content">
              <h4 className="insight-card-title">Least Active (Slipping) Segment</h4>
              <p className="insight-segment-name">{insights.least_active.segment_name} (Cluster {insights.least_active.cluster_id})</p>
              <div className="insight-stats">
                <div className="insight-stat"><span className="stat-label">Avg Recency:</span> <span className="stat-val">{insights.least_active.avg_recency} days ago</span></div>
                <div className="insight-stat"><span className="stat-label">Avg Spend:</span> <span className="stat-val">£{insights.least_active.avg_monetary.toLocaleString()}</span></div>
                <div className="insight-stat"><span className="stat-label">Size:</span> <span className="stat-val">{insights.least_active.count.toLocaleString()} customers ({insights.least_active.percentage}%)</span></div>
              </div>
              <p className="insight-recommendation">
                <strong>Marketing Strategy:</strong> Deploy win-back emails, aggressive reactivation discount vouchers, and feedback surveys to understand attrition factors.
              </p>
            </div>
          </div>

          {/* Most Recent (Lowest Recency) */}
          <div className="insight-card">
            <div className="card-glass-effect"></div>
            <div className="insight-icon-wrapper green">
              <TrendIcon />
            </div>
            <div className="insight-content">
              <h4 className="insight-card-title">Most Recent Segment</h4>
              <p className="insight-segment-name">{insights.most_recent.segment_name} (Cluster {insights.most_recent.cluster_id})</p>
              <div className="insight-stats">
                <div className="insight-stat"><span className="stat-label">Avg Recency:</span> <span className="stat-val">{insights.most_recent.avg_recency} days</span></div>
                <div className="insight-stat"><span className="stat-label">Avg Spend:</span> <span className="stat-val">£{insights.most_recent.avg_monetary.toLocaleString()}</span></div>
                <div className="insight-stat"><span className="stat-label">Size:</span> <span className="stat-val">{insights.most_recent.count.toLocaleString()} customers ({insights.most_recent.percentage}%)</span></div>
              </div>
              <p className="insight-recommendation">
                <strong>Marketing Strategy:</strong> Provide welcoming email drip campaigns, digital onboarding tutorials, and prompt recommendations to capture secondary transactions.
              </p>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Analytics;
