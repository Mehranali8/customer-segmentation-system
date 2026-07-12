import os
import joblib
from sklearn.cluster import KMeans

def save_model_for_prediction():
    # Resolve absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    input_model_path = os.path.join(base_dir, "models", "kmeans_model.joblib")
    output_model_path = os.path.join(base_dir, "models", "customer_segmentation_model.joblib")
    
    print("=" * 65)
    print("CUSTOMER SEGMENTATION SYSTEM - PERSIST MODEL FOR PRODUCTION")
    print("=" * 65)
    print(f"Loading trained K-Means model from: {input_model_path}")
    
    if not os.path.exists(input_model_path):
        print(f"Error: Trained model not found at {input_model_path}. Run model_training.py first.")
        return
        
    # Load the existing model
    kmeans = joblib.load(input_model_path)
    
    # Save the model under the new requested name
    print(f"Saving persistent model to: {output_model_path}")
    joblib.dump(kmeans, output_model_path)
    
    # Retrieve properties for display
    model_type = type(kmeans).__name__
    num_clusters = kmeans.n_clusters
    centers_shape = kmeans.cluster_centers_.shape
    
    print("\n--- Model Serialization Summary ---")
    print("Model successfully saved: Yes")
    print(f"Save location: {output_model_path}")
    print(f"Model type: {model_type}")
    print(f"Number of clusters: {num_clusters}")
    print(f"Cluster centers shape: {centers_shape}")
    print("=" * 65)

if __name__ == "__main__":
    save_model_for_prediction()
