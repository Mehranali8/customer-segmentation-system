import React from 'react';
import './CustomerTable.css';

// SVG Search Icon for table search bar
const TableSearchIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="table-search-icon">
    <circle cx="11" cy="11" r="8" />
    <line x1="21" y1="21" x2="16.65" y2="16.65" />
  </svg>
);

/**
 * CustomerTable Component
 * Displays a professional, responsive table with static mock customer segment records,
 * visual badges, hover highlights, and UI-only search controls.
 */
const CustomerTable = () => {
  const customers = [
    { id: '17850', segment: 'Premium', recency: 15, frequency: 25, monetary: '£8,500', status: 'Active' },
    { id: '14911', segment: 'VIP', recency: 3, frequency: 72, monetary: '£18,000', status: 'Active' },
    { id: '13047', segment: 'Regular', recency: 65, frequency: 8, monetary: '£900', status: 'Inactive' },
    { id: '15890', segment: 'At Risk', recency: 190, frequency: 3, monetary: '£250', status: 'Dormant' },
  ];

  return (
    <div className="customer-table-card">
      <div className="card-glass-effect"></div>
      
      {/* Table Header Section */}
      <div className="table-header">
        <h3 className="table-title">Recent Customer Profiles</h3>
        
        {/* Table Search Bar */}
        <div className="table-search">
          <TableSearchIcon />
          <input 
            type="text" 
            placeholder="Filter customers..." 
            className="table-search-input"
            disabled
          />
        </div>
      </div>

      {/* Responsive Table Wrapper */}
      <div className="table-responsive-container">
        <table className="customer-data-table">
          <thead>
            <tr>
              <th>Customer ID</th>
              <th>Segment</th>
              <th>Recency</th>
              <th>Frequency</th>
              <th>Monetary</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((cust) => (
              <tr key={cust.id}>
                <td className="cust-id">#{cust.id}</td>
                <td>
                  <span className={`segment-badge ${cust.segment.toLowerCase().replace(' ', '-')}`}>
                    {cust.segment}
                  </span>
                </td>
                <td>{cust.recency} days ago</td>
                <td>{cust.frequency} purchases</td>
                <td className="monetary-val">{cust.monetary}</td>
                <td>
                  <span className={`status-badge ${cust.status.toLowerCase()}`}>
                    {cust.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CustomerTable;
