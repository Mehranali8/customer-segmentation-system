import os
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

def predict_new_customer():
    # Resolve absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    model_path = os.path.join(base_dir, "models", "customer_segmentation_model.joblib")
    rfm_path = os.path.join(base_dir, "datasets", "customer_rfm.csv")
    
    print("=" * 65)
    print("CUSTOMER SEGMENTATION SYSTEM - NEW CUSTOMER SEGMENT PREDICTION")
    print("=" * 65)
    
    # 1. Load the K-Means model
    print(f"Loading K-Means model from: {model_path}")
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}. Run save_model.py first.")
        return
    kmeans = joblib.load(model_path)
    
    # 2. Fit standard scaler using raw RFM features to get matching scaling parameters
    print(f"Loading raw RFM reference features from: {rfm_path}")
    if not os.path.exists(rfm_path):
        print(f"Error: Raw RFM dataset not found at {rfm_path}.")
        return
    rfm = pd.read_csv(rfm_path)
    
    scaler = StandardScaler()
    scaler.fit(rfm[["Recency", "Frequency", "Monetary"]])
    
    # 3. Create a sample customer manually
    recency = 15
    frequency = 25
    monetary = 8500
    sample_raw = np.array([[recency, frequency, monetary]], dtype=float)
    
    # 4. Standardize the sample features using the fit scaler
    sample_scaled = scaler.transform(sample_raw)
    
    # 5. Predict the cluster
    predicted_cluster = int(kmeans.predict(sample_scaled)[0])
    
    # 6. Map cluster to segment name
    segment_mapping = {
        0: "Regular Customers",
        1: "At Risk Customers",
        2: "VIP Customers",
        3: "Premium Customers"
    }
    segment_name = segment_mapping.get(predicted_cluster, "Unknown Segment")
    
    # Print results
    print("\n--- Prediction Results ---")
    print("Input Features (Raw RFM):")
    print(f"  - Recency: {recency} days since last purchase")
    print(f"  - Frequency: {frequency} unique orders")
    print(f"  - Monetary Value: £{monetary:,.2f}")
    
    print("\nInput Features (Standardized Scale):")
    print(f"  - Recency (Scaled): {sample_scaled[0][0]:.6f}")
    print(f"  - Frequency (Scaled): {sample_scaled[0][1]:.6f}")
    print(f"  - Monetary (Scaled): {sample_scaled[0][2]:.6f}")
    
    print(f"\nPredicted Cluster ID: {predicted_cluster}")
    print(f"Customer Segment Name: {segment_name}")
    print("=" * 65)

if __name__ == "__main__":
    predict_new_customer()
