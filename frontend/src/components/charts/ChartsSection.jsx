import React from 'react';
import './ChartsSection.css';

/**
 * ChartsSection Component
 * Renders pure React + CSS static chart visuals representing RFM distributions
 * and customer segments cluster distribution from the backend model.
 */
const ChartsSection = ({ segmentDistribution }) => {
  // Safe total customer calculation
  const total = segmentDistribution
    ? Object.values(segmentDistribution).reduce((sum, val) => sum + val, 0)
    : 4338;
    
  // Dynamic segments mapping from backend labels
  const segments = [
    {
      label: 'VIP Customers',
      count: segmentDistribution ? (segmentDistribution['VIP Customers'] || 0) : 1041,
      pct: segmentDistribution ? Math.round(((segmentDistribution['VIP Customers'] || 0) / total) * 100) : 24,
      color: 'purple'
    },
    {
      label: 'Premium Customers',
      count: segmentDistribution ? (segmentDistribution['Premium Customers'] || 0) : 1648,
      pct: segmentDistribution ? Math.round(((segmentDistribution['Premium Customers'] || 0) / total) * 100) : 38,
      color: 'blue'
    },
    {
      label: 'Regular Customers',
      count: segmentDistribution ? (segmentDistribution['Regular Customers'] || 0) : 780,
      pct: segmentDistribution ? Math.round(((segmentDistribution['Regular Customers'] || 0) / total) * 100) : 18,
      color: 'green'
    },
    {
      label: 'At Risk Customers',
      count: segmentDistribution ? (segmentDistribution['At Risk Customers'] || 0) : 869,
      pct: segmentDistribution ? Math.round(((segmentDistribution['At Risk Customers'] || 0) / total) * 100) : 20,
      color: 'amber'
    }
  ];

  return (
    <div className="charts-section">
      <h2 className="section-title">Model Insights & Distributions</h2>
      <div className="charts-grid">
        
        {/* Customer Segments Distribution */}
        <div className="chart-card">
          <div className="card-glass-effect"></div>
          <h3 className="chart-title">Customer Segments Distribution</h3>
          <div className="chart-area segments-chart">
            {segments.map((seg) => (
              <div key={seg.label} className="segment-row">
                <span className="segment-label">{seg.label} ({seg.count.toLocaleString()} customers)</span>
                <div className="segment-bar-wrapper">
                  <div className={`segment-bar ${seg.color}`} style={{ width: `${seg.pct}%` }}></div>
                  <span className="segment-value">{seg.pct}%</span>
                </div>
              </div>
            ))}
          </div>
          <p className="chart-desc">Shows the percentage allocation of the {total.toLocaleString()} customers across K-Means clustering segments.</p>
        </div>

        {/* Recency Distribution */}
        <div className="chart-card">
          <div className="card-glass-effect"></div>
          <h3 className="chart-title">Recency Distribution (days)</h3>
          <div className="chart-area bar-chart">
            <div className="y-axis">
              <span>500</span>
              <span>250</span>
              <span>0</span>
            </div>
            <div className="bar-graph">
              <div className="bar-container"><div className="bar amber" style={{ height: '80%' }}></div><span className="bar-label">0-30d</span></div>
              <div className="bar-container"><div className="bar amber" style={{ height: '65%' }}></div><span className="bar-label">31-60d</span></div>
              <div className="bar-container"><div className="bar amber" style={{ height: '45%' }}></div><span className="bar-label">61-90d</span></div>
              <div className="bar-container"><div className="bar amber" style={{ height: '30%' }}></div><span className="bar-label">91-120d</span></div>
              <div className="bar-container"><div className="bar amber" style={{ height: '15%' }}></div><span className="bar-label">120d+</span></div>
            </div>
          </div>
          <p className="chart-desc">Distribution of days elapsed since customers' most recent transactions. Right-skewed density.</p>
        </div>

        {/* Frequency Distribution */}
        <div className="chart-card">
          <div className="card-glass-effect"></div>
          <h3 className="chart-title">Frequency Distribution (orders)</h3>
          <div className="chart-area bar-chart">
            <div className="y-axis">
              <span>1k</span>
              <span>500</span>
              <span>0</span>
            </div>
            <div className="bar-graph">
              <div className="bar-container"><div className="bar blue" style={{ height: '90%' }}></div><span className="bar-label">1-2</span></div>
              <div className="bar-container"><div className="bar blue" style={{ height: '40%' }}></div><span className="bar-label">3-5</span></div>
              <div className="bar-container"><div className="bar blue" style={{ height: '20%' }}></div><span className="bar-label">6-10</span></div>
              <div className="bar-container"><div className="bar blue" style={{ height: '10%' }}></div><span className="bar-label">11-20</span></div>
              <div className="bar-container"><div className="bar blue" style={{ height: '5%' }}></div><span className="bar-label">21+</span></div>
            </div>
          </div>
          <p className="chart-desc">Number of historical orders per customer. Features a high density of single-order interactions.</p>
        </div>

        {/* Monetary Distribution */}
        <div className="chart-card">
          <div className="card-glass-effect"></div>
          <h3 className="chart-title">Monetary Distribution (£)</h3>
          <div className="chart-area bar-chart">
            <div className="y-axis">
              <span>2k</span>
              <span>1k</span>
              <span>0</span>
            </div>
            <div className="bar-graph">
              <div className="bar-container"><div className="bar green" style={{ height: '95%' }}></div><span className="bar-label">0-500</span></div>
              <div className="bar-container"><div className="bar green" style={{ height: '50%' }}></div><span className="bar-label">500-1k</span></div>
              <div className="bar-container"><div className="bar green" style={{ height: '25%' }}></div><span className="bar-label">1k-2.5k</span></div>
              <div className="bar-container"><div className="bar green" style={{ height: '12%' }}></div><span className="bar-label">2.5k-5k</span></div>
              <div className="bar-container"><div className="bar green" style={{ height: '6%' }}></div><span className="bar-label">5k+</span></div>
            </div>
          </div>
          <p className="chart-desc">Spread of total revenue generated per customer. Long-tail distribution indicating high-value outliers.</p>
        </div>

      </div>
    </div>
  );
};

export default ChartsSection;
