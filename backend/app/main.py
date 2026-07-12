"""
Main application controller initializing FastAPI, loading model and features at startup,
and defining backend routes for the Customer Segmentation System.
"""
import os
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from sklearn.preprocessing import StandardScaler

from app.model_loader import load_kmeans_model, kmeans_model
from app.schemas import CustomerInput
from app.dashboard import get_dashboard_stats
from app.customer_search import get_customer_details
from app.customer_details import get_detailed_customer_profile

app = FastAPI(
    title="Customer Segmentation API",
    description="Machine Learning Customer Segmentation Backend",
    version="1.0.0",

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model status and scaler
model_status = {
    "loaded": False,
    "error": None
}
scaler = StandardScaler()

@app.on_event("startup")
def startup_event():
    """
    Startup event handler that loads the trained K-Means model
    and fits the standard scaler using raw RFM reference features.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    # 1. Load the K-Means Model
    try:
        load_kmeans_model()
        model_status["loaded"] = True
        print("Customer Segmentation Model Loaded Successfully")
    except Exception as e:
        model_status["loaded"] = False
        model_status["error"] = str(e)
        print(f"Error loading Customer Segmentation Model: {str(e)}")
        
    # 2. Fit standard scaler using reference customer RFM features
    try:
        rfm_path = os.path.join(base_dir, "datasets", "customer_rfm.csv")
        if os.path.exists(rfm_path):
            rfm = pd.read_csv(rfm_path)
            scaler.fit(rfm[["Recency", "Frequency", "Monetary"]])
            print("Feature StandardScaler initialized successfully")
        else:
            print(f"Warning: Reference RFM features file not found at: {rfm_path}")
    except Exception as e:
        print(f"Error fitting reference scaler: {str(e)}")

@app.get("/")
def read_root() -> Dict[str, str]:
    """
    Root endpoint that returns basic details and health status of the Customer Segmentation API.
    """
    return {
        "message": "Customer Segmentation API",
        "status": "healthy"
    }

@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    Health check endpoint returning the status of the backend and the loaded state of the model.
    """
    model_state = "loaded" if model_status["loaded"] else "not_loaded"
    return {
        "backend": "running",
        "model": model_state,
        "version": "1.0.0"
    }

@app.get("/model-info")
def get_model_info() -> Dict[str, Any]:
    """
    Returns metadata about the loaded customer segmentation model.
    """
    if not model_status["loaded"]:
        return {
            "model_loaded": False,
            "error": model_status["error"] or "Model not loaded"
        }
        
    try:
        from app.model_loader import kmeans_model
        if kmeans_model is None:
            return {
                "model_loaded": False,
                "error": "Model object is None"
            }
            
        return {
            "model_loaded": True,
            "algorithm": type(kmeans_model).__name__,
            "clusters": int(kmeans_model.n_clusters)
        }
    except Exception as e:
        return {
            "model_loaded": False,
            "error": f"Failed to retrieve model information: {str(e)}"
        }

@app.post("/predict")
def predict_segment(customer_in: CustomerInput) -> Dict[str, Any]:
    """
    Predicts the customer segment for a given set of Recency, Frequency, and Monetary values.
    Standardizes the input features before K-Means prediction, returning the Cluster ID and Segment Label.
    """
    from app.model_loader import kmeans_model
    
    if not model_status["loaded"] or kmeans_model is None:
        raise HTTPException(
            status_code=503,
            detail="Prediction service unavailable: Customer segmentation model is not loaded."
        )
        
    try:
        # Convert input features to a 2D numpy array format
        raw_features = np.array([[customer_in.recency, customer_in.frequency, customer_in.monetary]], dtype=float)
        
        # Standardize the features using the scaler fitted during startup
        scaled_features = scaler.transform(raw_features)
        
        # Predict the cluster using the loaded K-Means model
        predicted_cluster = int(kmeans_model.predict(scaled_features)[0])
        
        # Map cluster ID to descriptive business segment name
        segment_mapping = {
            0: "Regular Customers",
            1: "At Risk Customers",
            2: "VIP Customers",
            3: "Premium Customers"
        }
        segment_name = segment_mapping.get(predicted_cluster, "Unknown Segment")
        
        return {
            "cluster": predicted_cluster,
            "segment": segment_name
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference error during segment calculation: {str(e)}"
        )

@app.get("/dashboard")
def get_dashboard_data() -> Dict[str, Any]:
    """
    Dashboard endpoint that calculates and returns summary statistics
    and segment distribution counts of the customer base.
    """
    try:
        stats = get_dashboard_stats()
        return stats
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate dashboard statistics: {str(e)}"
        )

@app.get("/customer/{customer_id}")
def search_customer(customer_id: int) -> Dict[str, Any]:
    """
    Searches the labeled database by Customer ID and returns their details.
    Throws a 404 error if the customer is not found.
    """
    try:
        details = get_customer_details(customer_id)
        if details is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )
        return details
    except HTTPException:
        # Re-raise standard HTTPExceptions to preserve status codes
        raise
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute customer search: {str(e)}"
        )

@app.get("/customer-details/{customer_id}")
def get_customer_details_profile(customer_id: int) -> Dict[str, Any]:
    """
    Fetches detailed customer profiles and calculates customer status (Active, Recent, Inactive, Dormant)
    relying on unscaled Recency. Throws a 404 error if the customer does not exist.
    """
    try:
        profile = get_detailed_customer_profile(customer_id)
        if profile is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )
        return profile
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch customer profile details: {str(e)}"
        )
