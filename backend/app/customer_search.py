"""
Customer query service that checks for CustomerID presence and maps values.
"""
import os
import pandas as pd
from typing import Dict, Any, Optional

def get_customer_details(customer_id: int) -> Optional[Dict[str, Any]]:
    """
    Searches for a customer by their CustomerID and returns their unscaled RFM features,
    cluster ID, and segment label.
    
    Args:
        customer_id: The ID of the customer to search for.
    Returns:
        A dictionary containing the customer details, or None if the customer is not found.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    rfm_path = os.path.join(base_dir, "datasets", "customer_rfm.csv")
    segments_path = os.path.join(base_dir, "datasets", "customer_segments_labeled.csv")
    
    if not os.path.exists(rfm_path) or not os.path.exists(segments_path):
        raise FileNotFoundError("Customer database files are missing. Please complete prior modules.")
        
    rfm_df = pd.read_csv(rfm_path)
    segments_df = pd.read_csv(segments_path)
    
    # Query customer row in both tables
    customer_rfm = rfm_df[rfm_df["CustomerID"] == customer_id]
    customer_segment = segments_df[segments_df["CustomerID"] == customer_id]
    
    if customer_rfm.empty or customer_segment.empty:
        return None
        
    r_row = customer_rfm.iloc[0]
    s_row = customer_segment.iloc[0]
    
    return {
        "customer_id": int(customer_id),
        "recency": float(r_row["Recency"]),
        "frequency": float(r_row["Frequency"]),
        "monetary": float(r_row["Monetary"]),
        "cluster": int(s_row["Cluster"]),
        "segment": str(s_row["CustomerSegment"])
    }
