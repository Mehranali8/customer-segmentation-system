"""
Dashboard statistics service to aggregate datasets for display in the admin panel.
"""
import os
import pandas as pd
from typing import Dict, Any

def get_dashboard_stats() -> Dict[str, Any]:
    """
    Calculates summary statistics and segment distributions for the Customer Segmentation System.
    Loads raw RFM values for unscaled averages and labeled segments for distribution counts.
    
    Returns:
        A dictionary containing dashboard metrics.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    labeled_path = os.path.join(base_dir, "datasets", "customer_segments_labeled.csv")
    rfm_path = os.path.join(base_dir, "datasets", "customer_rfm.csv")
    
    if not os.path.exists(labeled_path):
        raise FileNotFoundError(f"Labeled segments dataset not found at expected path: {labeled_path}")
    if not os.path.exists(rfm_path):
        raise FileNotFoundError(f"Reference RFM dataset not found at expected path: {rfm_path}")
        
    # Load files
    labeled_df = pd.read_csv(labeled_path)
    rfm_df = pd.read_csv(rfm_path)
    
    total_customers = int(labeled_df.shape[0])
    total_segments = int(labeled_df["CustomerSegment"].nunique())
    
    # Calculate overall averages from unscaled RFM data
    avg_recency = float(rfm_df["Recency"].mean())
    avg_frequency = float(rfm_df["Frequency"].mean())
    avg_monetary = float(rfm_df["Monetary"].mean())
    
    # Calculate Segment Distribution
    counts_dict = labeled_df["CustomerSegment"].value_counts().to_dict()
    
    # Ensure expected segments are present with proper formatting
    expected_segments = ["Regular Customers", "At Risk Customers", "Premium Customers", "VIP Customers"]
    segment_distribution = {seg: int(counts_dict.get(seg, 0)) for seg in expected_segments}
    
    return {
        "total_customers": total_customers,
        "total_segments": total_segments,
        "average_recency": round(avg_recency, 2),
        "average_frequency": round(avg_frequency, 2),
        "average_monetary": round(avg_monetary, 2),
        "segment_distribution": segment_distribution
    }
