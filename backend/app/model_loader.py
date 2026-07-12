"""
Model loading module that deserializes and hosts the trained K-Means model for inference.
"""
import os
import joblib
from typing import Any, Optional

# Global variable to hold the loaded K-Means model
kmeans_model: Optional[Any] = None

def load_kmeans_model() -> Optional[Any]:
    """
    Loads the K-Means clustering model from disk using joblib and stores it in the global variable.
    
    Returns:
        The loaded K-Means model object, or None if load fails.
    """
    global kmeans_model
    if kmeans_model is not None:
        return kmeans_model
        
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    model_path = os.path.join(base_dir, "models", "customer_segmentation_model.joblib")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at expected path: {model_path}")
        
    kmeans_model = joblib.load(model_path)
    return kmeans_model
