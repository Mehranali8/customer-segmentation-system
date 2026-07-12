import React, { useState } from 'react';
import api from '../services/api';
import './Prediction.css';

/**
 * Prediction Component
 * Renders the Customer Segment Prediction page. Interfaces with the pre-trained FastAPI
 * ML model using live input parameters to perform segment classification.
 */
const Prediction = () => {
  const [recency, setRecency] = useState('');
  const [frequency, setFrequency] = useState('');
  const [monetary, setMonetary] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (recency === '' || frequency === '' || monetary === '') return;

    try {
      setLoading(true);
      setError(null);
      setSuccessMessage(null);

      // Validate inputs locally (must be non-negative)
      const r = parseFloat(recency);
      const f = parseFloat(frequency);
      const m = parseFloat(monetary);

      if (isNaN(r) || r < 0 || isNaN(f) || f < 0 || isNaN(m) || m < 0) {
        throw new Error('All input values must be positive numbers.');
      }

      // Build payload for validation
      const payload = {
        recency: r,
        frequency: f,
        monetary: m,
      };

      // POST request to prediction endpoint
      const response = await api.post('/predict', payload);
      setResult(response.data);
      setSuccessMessage('Customer segment classification calculated successfully.');
      setShowResult(true);
    } catch (err) {
      console.error('Prediction request failed:', err);
      setShowResult(false);
      
      // Parse backend and network errors
      if (err.data && err.data.detail) {
        if (Array.isArray(err.data.detail)) {
          // Format Pydantic field validation errors
          const validationErrors = err.data.detail
            .map((item) => `${item.loc[item.loc.length - 1]}: ${item.msg}`)
            .join(', ');
          setError(`Validation Error: ${validationErrors}`);
        } else {
          setError(`API Error: ${err.data.detail}`);
        }
      } else {
        setError(err.message || 'Failed to communicate with prediction service. Please ensure the backend server is running.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setRecency('');
    setFrequency('');
    setMonetary('');
    setShowResult(false);
    setError(null);
    setSuccessMessage(null);
    setResult(null);
  };

  // Dynamic recommendation mapping based on predicted segment name
  const getRecommendation = (segment) => {
    switch (segment) {
      case 'VIP Customers':
        return 'This customer is highly active and spends heavily. Target with exclusive VIP rewards, high-tier early access, and customized loyalty initiatives.';
      case 'Premium Customers':
        return 'This customer is highly valuable and should receive loyalty offers.';
      case 'Regular Customers':
        return 'This customer shows standard shopping behavior. Consider regular engagement campaigns, general promotions, and seasonal retention reminders.';
      case 'At Risk Customers':
        return 'This customer has high recency (dormant period). Urgent reactivation campaigns, exclusive reactivation coupons, and survey triggers are recommended.';
      default:
        return 'This customer is evaluated under standard model behaviors. Deploy standard digital marketing campaigns.';
    }
  };

  return (
    <div className="prediction-page">
      <div className="prediction-header">
        <h2 className="prediction-title">Customer Segment Prediction</h2>
        <p className="prediction-subtitle">
          Input RFM (Recency, Frequency, Monetary) metrics below to forecast customer segment assignment via the machine learning engine.
        </p>
      </div>

      {/* Alert Banners */}
      {error && <div className="prediction-alert error">{error}</div>}
      {successMessage && <div className="prediction-alert success">{successMessage}</div>}

      {/* Prediction Inputs Card */}
      <div className="prediction-card">
        <div className="card-glass-effect"></div>
        <form onSubmit={handleSubmit} className="prediction-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="recency" className="form-label">Recency (Days)</label>
              <input
                type="number"
                id="recency"
                className="form-input"
                placeholder="e.g., 15"
                min="0"
                step="any"
                value={recency}
                onChange={(e) => setRecency(e.target.value)}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="frequency" className="form-label">Frequency (Orders)</label>
              <input
                type="number"
                id="frequency"
                className="form-input"
                placeholder="e.g., 25"
                min="0"
                step="any"
                value={frequency}
                onChange={(e) => setFrequency(e.target.value)}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="monetary" className="form-label">Monetary Value (£)</label>
              <input
                type="number"
                id="monetary"
                className="form-input"
                placeholder="e.g., 8500"
                min="0"
                step="any"
                value={monetary}
                onChange={(e) => setMonetary(e.target.value)}
                disabled={loading}
                required
              />
            </div>
          </div>
          
          <div className="form-actions">
            <button 
              type="submit" 
              className="btn btn-primary" 
              disabled={loading || recency === '' || frequency === '' || monetary === ''}
            >
              {loading ? 'Predicting...' : 'Predict Segment'}
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

      {/* Prediction Result Card */}
      {showResult && result && (
        <div className="prediction-result-card fade-in">
          <div className="card-glass-effect"></div>
          
          <div className="result-header">
            <div className="result-title-group">
              <span className="result-badge">Model Output</span>
              <h3 className="result-segment-name">{result.segment}</h3>
            </div>
            <div className="cluster-tag">Cluster {result.cluster}</div>
          </div>

          {/* Conditional Confidence rendering (if returned by backend API) */}
          {result.confidence !== undefined && (
            <div className="result-metrics">
              <div className="metric-box">
                <span className="metric-label">Prediction Confidence</span>
                <div className="confidence-wrapper">
                  <span className="metric-value font-accent">{result.confidence}%</span>
                  <div className="confidence-bar-bg">
                    <div className="confidence-bar-fill" style={{ width: `${result.confidence}%` }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div className="recommendation-box">
            <h4 className="recommendation-title">Strategic Recommendation</h4>
            <p className="recommendation-text">
              {getRecommendation(result.segment)}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Prediction;
