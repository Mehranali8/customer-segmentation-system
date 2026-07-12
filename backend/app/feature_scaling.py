import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

def scale_features():
    # Resolve absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    rfm_path = os.path.join(base_dir, "datasets", "customer_rfm.csv")
    output_path = os.path.join(base_dir, "datasets", "customer_rfm_scaled.csv")
    
    print("=" * 65)
    print("CUSTOMER SEGMENTATION SYSTEM - FEATURE SCALING")
    print("=" * 65)
    print(f"Loading RFM features from: {rfm_path}")
    
    if not os.path.exists(rfm_path):
        print(f"Error: RFM features file not found at {rfm_path}")
        return
        
    rfm = pd.read_csv(rfm_path)
    
    original_shape = rfm.shape
    
    # Initialize StandardScaler
    scaler = StandardScaler()
    
    # Select features to scale
    features = ["Recency", "Frequency", "Monetary"]
    
    # Fit and transform
    scaled_values = scaler.fit_transform(rfm[features])
    
    # Create the new dataframe
    scaled_df = rfm.copy()
    scaled_df[features] = scaled_values
    
    scaled_shape = scaled_df.shape
    
    # Save the scaled dataset
    print(f"Saving scaled dataset to: {output_path}")
    scaled_df.to_csv(output_path, index=False)
    
    # Calculate Mean and Std
    means = scaled_df[features].mean()
    stds = scaled_df[features].std()
    
    print("\n--- Feature Scaling Results ---")
    print(f"Original Dataset Shape: {original_shape}")
    print(f"Scaled Dataset Shape: {scaled_shape}")
    
    print("\nFirst 10 rows:")
    print(scaled_df.head(10))
    
    print("\nLast 10 rows:")
    print(scaled_df.tail(10))
    
    print("\nMean of each feature (scaled):")
    for feat, val in means.items():
        print(f"  {feat}: {val:.4e}")
        
    print("\nStandard Deviation of each feature (scaled):")
    for feat, val in stds.items():
        print(f"  {feat}: {val:.6f}")
    print("=" * 65)

if __name__ == "__main__":
    scale_features()
