import os
import pandas as pd
from typing import Dict, Any

def analyze_clusters():
    # Resolve absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    segments_path = os.path.join(base_dir, "datasets", "customer_segments.csv")
    rfm_path = os.path.join(base_dir, "datasets", "customer_rfm.csv")
    
    print("=" * 70)
    print("CUSTOMER SEGMENTATION SYSTEM - CUSTOMER SEGMENT ANALYSIS")
    print("=" * 70)
    
    if not os.path.exists(segments_path) or not os.path.exists(rfm_path):
        print("Error: Required datasets (customer_segments.csv or customer_rfm.csv) not found.")
        return
        
    # Load clustered data and raw RFM features
    segments_df = pd.read_csv(segments_path)
    rfm_df = pd.read_csv(rfm_path)
    
    # Merge on CustomerID to get original scale RFM features for clustered customers
    merged_df = pd.merge(rfm_df, segments_df[["CustomerID", "Cluster"]], on="CustomerID")
    
    total_customers = len(merged_df)
    
    # Group by Cluster and calculate true RFM means, count, and percentage
    summary = merged_df.groupby("Cluster").agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean",
        "CustomerID": "count"
    }).rename(columns={"CustomerID": "Count"})
    
    summary["Percentage"] = (summary["Count"] / total_customers) * 100
    
    # Sort the summary table by Cluster ID
    summary = summary.sort_index()
    
    # Print the summary table
    print("\n--- Cluster Metrics (Original Scale Averages) ---")
    print(f"{'Cluster':<8} | {'Avg Recency':<12} | {'Avg Frequency':<13} | {'Avg Monetary':<12} | {'Count':<6} | {'Percentage':<10}")
    print("-" * 75)
    for cid, row in summary.iterrows():
        print(f"   {cid:1d}     | {row['Recency']:10.1f} d | {row['Frequency']:11.2f}   | £{row['Monetary']:10.2f} | {int(row['Count']):5d} | {row['Percentage']:8.2f}%")
    
    # Dynamic interpretation values
    max_monetary_cluster = summary["Monetary"].idxmax()
    max_frequency_cluster = summary["Frequency"].idxmax()
    least_active_cluster = summary["Recency"].idxmax()
    most_recent_cluster = summary["Recency"].idxmin()
    
    print("\n" + "=" * 70)
    print("BEHAVIORAL INTERPRETATION & OBSERVATIONS")
    print("=" * 70)
    
    # 1. Spends the most
    print(f"1. Highest Spending Segment: Cluster {max_monetary_cluster}")
    print(f"   - Average monetary value: £{summary.loc[max_monetary_cluster, 'Monetary']:,.2f}")
    print(f"   - Average purchase frequency: {summary.loc[max_monetary_cluster, 'Frequency']:.2f} orders")
    print(f"   - Average recency: {summary.loc[max_monetary_cluster, 'Recency']:.1f} days")
    
    # 2. Purchases most frequently
    print(f"\n2. Most Frequent Purchasing Segment: Cluster {max_frequency_cluster}")
    print(f"   - Average purchase frequency: {summary.loc[max_frequency_cluster, 'Frequency']:.2f} orders")
    print(f"   - Average monetary value: £{summary.loc[max_frequency_cluster, 'Monetary']:,.2f}")
    
    # 3. Least active (highest recency)
    print(f"\n3. Least Active Segment: Cluster {least_active_cluster}")
    print(f"   - Average recency (days since last order): {summary.loc[least_active_cluster, 'Recency']:.1f} days")
    print(f"   - Average purchase frequency: {summary.loc[least_active_cluster, 'Frequency']:.2f} orders")
    print(f"   - Average monetary value: £{summary.loc[least_active_cluster, 'Monetary']:,.2f}")
    
    # 4. Most recent customers
    print(f"\n4. Most Recent Segment: Cluster {most_recent_cluster}")
    print(f"   - Average recency (days since last order): {summary.loc[most_recent_cluster, 'Recency']:.1f} days")
    print(f"   - Average purchase frequency: {summary.loc[most_recent_cluster, 'Frequency']:.2f} orders")
    print(f"   - Average monetary value: £{summary.loc[most_recent_cluster, 'Monetary']:,.2f}")
    
    print("\nGeneral Insights:")
    print(f"  - Cluster 2 represents an extreme outlier customer group ({int(summary.loc[2, 'Count'])} customers)")
    print(f"    with massive spending (average £{summary.loc[2, 'Monetary']:,.2f}) and high buying frequency.")
    print(f"  - Cluster 3 represents high-value premium customers ({int(summary.loc[3, 'Count'])} customers) that purchase often.")
    print(f"  - Cluster 0 covers the primary active base ({int(summary.loc[0, 'Count'])} customers) with moderate spending.")
    print(f"  - Cluster 1 contains slipping/at-risk customers ({int(summary.loc[1, 'Count'])} customers) with very high recency.")
    print("=" * 70)

def get_cluster_analytics() -> Dict[str, Any]:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    labeled_path = os.path.join(base_dir, "datasets", "customer_segments_labeled.csv")
    rfm_path = os.path.join(base_dir, "datasets", "customer_rfm.csv")
    
    if not os.path.exists(labeled_path):
        raise FileNotFoundError(f"Labeled segments dataset not found at: {labeled_path}")
    if not os.path.exists(rfm_path):
        raise FileNotFoundError(f"Reference RFM dataset not found at: {rfm_path}")
        
    labeled_df = pd.read_csv(labeled_path)
    rfm_df = pd.read_csv(rfm_path)
    
    # Merge on CustomerID to get unscaled Recency, Frequency, Monetary values
    merged_df = pd.merge(rfm_df, labeled_df[["CustomerID", "Cluster", "CustomerSegment"]], on="CustomerID")
    
    total_customers = len(merged_df)
    
    # Group by Cluster and CustomerSegment and calculate true RFM means, count
    summary = merged_df.groupby(["Cluster", "CustomerSegment"]).agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean",
        "CustomerID": "count"
    }).reset_index()
    
    summary["Percentage"] = (summary["CustomerID"] / total_customers) * 100
    
    # Convert summary dataframe to dictionary list
    cluster_metrics = []
    for _, row in summary.iterrows():
        cluster_metrics.append({
            "cluster_id": int(row["Cluster"]),
            "segment_name": str(row["CustomerSegment"]),
            "avg_recency": round(float(row["Recency"]), 2),
            "avg_frequency": round(float(row["Frequency"]), 2),
            "avg_monetary": round(float(row["Monetary"]), 2),
            "count": int(row["CustomerID"]),
            "percentage": round(float(row["Percentage"]), 2)
        })
        
    # Sort cluster metrics by cluster_id
    cluster_metrics = sorted(cluster_metrics, key=lambda x: x["cluster_id"])
    
    # Calculate index pointers for insights
    summary_indexed = summary.set_index("Cluster")
    max_monetary_cluster = int(summary_indexed["Monetary"].idxmax())
    max_frequency_cluster = int(summary_indexed["Frequency"].idxmax())
    least_active_cluster = int(summary_indexed["Recency"].idxmax())
    most_recent_cluster = int(summary_indexed["Recency"].idxmin())
    
    # Locate row dictionaries for observations
    find_metrics = lambda cid: next(item for item in cluster_metrics if item["cluster_id"] == cid)
    
    insights = {
        "highest_spending": find_metrics(max_monetary_cluster),
        "most_frequent": find_metrics(max_frequency_cluster),
        "least_active": find_metrics(least_active_cluster),
        "most_recent": find_metrics(most_recent_cluster)
    }
    
    return {
        "cluster_metrics": cluster_metrics,
        "insights": insights
    }

if __name__ == "__main__":
    analyze_clusters()
