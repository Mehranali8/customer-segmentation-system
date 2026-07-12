"""
Customer detailed profile service that checks details and assigns status.
"""
import os
import pandas as pd
from typing import Dict, Any, Optional

def get_detailed_customer_profile(customer_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves detailed customer profile including unscaled RFM features,
    cluster ID, segment label, and recency-based customer status.
    
    Args:
        customer_id: The ID of the customer to fetch details for.
    Returns:
        A dictionary containing the customer details and status, or None if not found.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    rfm_path = os.path.join(base_dir, "datasets", "customer_rfm.csv")
    segments_path = os.path.join(base_dir, "datasets", "customer_segments_labeled.csv")
    
    if not os.path.exists(rfm_path) or not os.path.exists(segments_path):
        raise FileNotFoundError("Customer database files are missing.")
        
    rfm_df = pd.read_csv(rfm_path)
    segments_df = pd.read_csv(segments_path)
    
    # Query customer in both datasets
    c_rfm = rfm_df[rfm_df["CustomerID"] == customer_id]
    c_seg = segments_df[segments_df["CustomerID"] == customer_id]
    
    if c_rfm.empty or c_seg.empty:
        return None
        
    r_val = c_rfm.iloc[0]
    s_val = c_seg.iloc[0]
    
    recency = float(r_val["Recency"])
    
    # Determine customer status based on unscaled Recency days
    if recency <= 30:
        status = "Active"
    elif 31 <= recency <= 90:
        status = "Recent"
    elif 91 <= recency <= 180:
        status = "Inactive"
    else:
        status = "Dormant"
        
    return {
        "customer_id": int(customer_id),
        "recency": float(r_val["Recency"]),
        "frequency": float(r_val["Frequency"]),
        "monetary": float(r_val["Monetary"]),
        "cluster": int(s_val["Cluster"]),
        "segment": str(s_val["CustomerSegment"]),
        "customer_status": status
    }
