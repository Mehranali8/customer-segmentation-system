import os
import pandas as pd

def calculate_rfm_features():
    # Resolve absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    clean_dataset_path = os.path.join(base_dir, "datasets", "online_retail_clean.csv")
    output_path = os.path.join(base_dir, "datasets", "customer_rfm.csv")
    
    print("=" * 65)
    print("CUSTOMER SEGMENTATION SYSTEM - RFM FEATURE ENGINEERING")
    print("=" * 65)
    print(f"Loading cleaned dataset from: {clean_dataset_path}")
    
    if not os.path.exists(clean_dataset_path):
        print(f"Error: Cleaned dataset file not found at {clean_dataset_path}")
        return
        
    df = pd.read_csv(clean_dataset_path)
    
    # Ensure InvoiceDate is datetime format
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    
    # Find the latest InvoiceDate in the dataset
    max_date = df["InvoiceDate"].max()
    print(f"Latest InvoiceDate in dataset: {max_date}")
    
    # Group by Customer ID and calculate RFM
    # - Recency: Days since last purchase relative to max_date
    # - Frequency: Number of unique invoices per customer
    # - Monetary: Sum of TotalAmount per customer
    rfm = df.groupby("Customer ID").agg({
        "InvoiceDate": lambda x: (max_date - x.max()).days,
        "Invoice": "nunique",
        "TotalAmount": "sum"
    }).reset_index()
    
    # Rename columns to matches requirements exactly
    rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]
    
    # Convert CustomerID to integer
    rfm["CustomerID"] = rfm["CustomerID"].astype(int)
    
    # Save the output CSV
    print(f"Saving RFM dataset to: {output_path}")
    rfm.to_csv(output_path, index=False)
    
    # Print metrics
    num_customers = len(rfm)
    avg_recency = rfm["Recency"].mean()
    avg_frequency = rfm["Frequency"].mean()
    avg_monetary = rfm["Monetary"].mean()
    shape = rfm.shape
    
    print("\n--- RFM Features Summary ---")
    print(f"Number of Customers: {num_customers:,}")
    print(f"Average Recency: {avg_recency:.2f} days")
    print(f"Average Frequency: {avg_frequency:.2f} unique orders")
    print(f"Average Monetary: £{avg_monetary:,.2f}")
    print(f"Dataset Shape: {shape}")
    
    print("\nFirst 10 rows:")
    print(rfm.head(10))
    
    print("\nLast 10 rows:")
    print(rfm.tail(10))
    print("=" * 65)

if __name__ == "__main__":
    calculate_rfm_features()
