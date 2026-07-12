import os
import pandas as pd

def label_segments():
    # Resolve absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    segments_path = os.path.join(base_dir, "datasets", "customer_segments.csv")
    output_path = os.path.join(base_dir, "datasets", "customer_segments_labeled.csv")
    
    print("=" * 65)
    print("CUSTOMER SEGMENTATION SYSTEM - CUSTOMER SEGMENT LABELING")
    print("=" * 65)
    print(f"Loading clustered dataset from: {segments_path}")
    
    if not os.path.exists(segments_path):
        print(f"Error: Clustered dataset file not found at {segments_path}")
        return
        
    df = pd.read_csv(segments_path)
    
    # Mapping of Cluster IDs to meaningful business labels
    segment_mapping = {
        0: "Regular Customers",
        1: "At Risk Customers",
        2: "VIP Customers",
        3: "Premium Customers"
    }
    
    # Create the new column CustomerSegment by mapping the Cluster column
    df["CustomerSegment"] = df["Cluster"].map(segment_mapping)
    
    # Save the updated labeled dataset
    print(f"Saving labeled dataset to: {output_path}")
    df.to_csv(output_path, index=False)
    
    # Calculate counts and percentages
    counts = df["CustomerSegment"].value_counts()
    percentages = df["CustomerSegment"].value_counts(normalize=True) * 100
    
    print("\n--- Segment Distribution Summary ---")
    print(f"{'Segment Name':<20} | {'Customer Count':<14} | {'Percentage':<10}")
    print("-" * 52)
    for seg_name in ["Regular Customers", "At Risk Customers", "Premium Customers", "VIP Customers"]:
        cnt = counts.get(seg_name, 0)
        pct = percentages.get(seg_name, 0.0)
        print(f"{seg_name:<20} | {cnt:14,d} | {pct:8.2f}%")
        
    print("\nFirst 10 rows:")
    print(df.head(10))
    
    print("\nLast 10 rows:")
    print(df.tail(10))
    print("=" * 65)

if __name__ == "__main__":
    label_segments()
