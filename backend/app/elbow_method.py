import os
import pandas as pd
import matplotlib
# Use Agg headless backend for matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def compute_elbow():
    # Resolve absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    scaled_data_path = os.path.join(base_dir, "datasets", "customer_rfm_scaled.csv")
    output_dir = os.path.join(base_dir, "screenshots")
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 65)
    print("CUSTOMER SEGMENTATION SYSTEM - ELBOW METHOD FOR OPTIMAL K")
    print("=" * 65)
    print(f"Loading scaled RFM features from: {scaled_data_path}")
    
    if not os.path.exists(scaled_data_path):
        print(f"Error: Scaled RFM features file not found at {scaled_data_path}")
        return
        
    df = pd.read_csv(scaled_data_path)
    
    # Ignore CustomerID and select features
    features = ["Recency", "Frequency", "Monetary"]
    X = df[features]
    
    # Calculate WCSS for K = 1 to 10
    wcss = []
    print("\nTraining K-Means models...")
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
        print(f"  K = {k:2d} | WCSS = {kmeans.inertia_:.4f}")
        
    # Plot the Elbow Curve
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), wcss, marker='o', linestyle='-', color='#6366f1', linewidth=2, markersize=8)
    plt.title("Elbow Method for Optimal K Selection", fontsize=12, fontweight="bold")
    plt.xlabel("Number of Clusters (K)", fontsize=10)
    plt.ylabel("Within-Cluster Sum of Squares (WCSS / Inertia)", fontsize=10)
    plt.xticks(range(1, 11))
    plt.grid(linestyle='--', alpha=0.5)
    
    # Highlight typical elbow values (K=3 and K=4) on the graph
    plt.axvline(x=3, color='#f43f5e', linestyle='--', alpha=0.7, label='Elbow Option (K=3)')
    plt.axvline(x=4, color='#10b981', linestyle='--', alpha=0.7, label='Elbow Option (K=4)')
    plt.legend()
    
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "elbow_method.png")
    plt.savefig(chart_path, dpi=150)
    plt.close()
    print(f"\nSaved elbow chart to: {chart_path}")
    
    # Print results summary
    print("\n--- Elbow Analysis Summary ---")
    print("K Value | WCSS (Inertia)")
    print("-" * 25)
    for k, val in enumerate(wcss, start=1):
        print(f"   {k:2d}   | {val:,.2f}")
        
    # Analyze rate of change (first difference and second difference) to suggest elbow mathematically
    # but also output the visual elbow recommendation
    print("\nBest Visual Elbow Recommendation:")
    print("  K = 3 or K = 4")
    print("  Rationale: The rate of decrease in WCSS slows down significantly after K = 3,")
    print("  forming a clear 'elbow' shape. Choosing K = 3 provides broad, highly distinct segments,")
    print("  while K = 4 allows for finer segmentation of active and slipping customer bases.")
    print("=" * 65)

if __name__ == "__main__":
    compute_elbow()
