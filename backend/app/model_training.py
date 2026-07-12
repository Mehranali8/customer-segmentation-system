import os
import pandas as pd
import joblib
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def train_final_model():
    # Resolve absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    scaled_data_path = os.path.join(base_dir, "datasets", "customer_rfm_scaled.csv")
    segments_output_path = os.path.join(base_dir, "datasets", "customer_segments.csv")
    model_output_path = os.path.join(base_dir, "models", "kmeans_model.joblib")
    
    # Ensure models directory exists
    os.makedirs(os.path.join(base_dir, "models"), exist_ok=True)
    
    print("=" * 65)
    print("CUSTOMER SEGMENTATION SYSTEM - K-MEANS MODEL TRAINING")
    print("=" * 65)
    print(f"Loading scaled RFM features from: {scaled_data_path}")
    
    if not os.path.exists(scaled_data_path):
        print(f"Error: Scaled RFM features file not found at {scaled_data_path}")
        return
        
    df = pd.read_csv(scaled_data_path)
    
    # Ignore CustomerID and select features for training
    features = ["Recency", "Frequency", "Monetary"]
    X = df[features]
    
    print("Training final K-Means model with K = 4...")
    # Initialize and fit K-Means
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    kmeans.fit(X)
    
    # Assign cluster labels to every customer
    labels = kmeans.labels_
    df["Cluster"] = labels
    
    # Save the clustered dataset
    print(f"Saving clustered dataset to: {segments_output_path}")
    df.to_csv(segments_output_path, index=False)
    
    # Save the trained model using joblib
    print(f"Saving trained model to: {model_output_path}")
    joblib.dump(kmeans, model_output_path)
    
    # Calculate metrics
    num_customers = len(df)
    cluster_counts = df["Cluster"].value_counts().sort_index()
    cluster_pcts = df["Cluster"].value_counts(normalize=True).sort_index() * 100
    inertia = kmeans.inertia_
    sil_score = silhouette_score(X, labels)
    
    print("\n--- Training Results ---")
    print(f"Number of Customers: {num_customers:,}")
    print(f"Model Inertia: {inertia:.4f}")
    print(f"Silhouette Score: {sil_score:.4f}")
    
    print("\nCluster Distribution:")
    print("Cluster | Count | Percentage")
    print("-" * 28)
    for cluster_id in range(4):
        count = cluster_counts.get(cluster_id, 0)
        pct = cluster_pcts.get(cluster_id, 0.0)
        print(f"   {cluster_id}    | {count:5d} | {pct:6.2f}%")
        
    print("\nFirst 10 rows:")
    print(df.head(10))
    
    print("\nLast 10 rows:")
    print(df.tail(10))
    print("=" * 65)

if __name__ == "__main__":
    train_final_model()
