import os
import pandas as pd

def preprocess_dataset():
    # Resolve absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    dataset_path = os.path.join(base_dir, "datasets", "online_retail_II.csv")
    output_path = os.path.join(base_dir, "datasets", "online_retail_clean.csv")
    
    print("=" * 65)
    print("CUSTOMER SEGMENTATION SYSTEM - DATA CLEANING & PREPROCESSING")
    print("=" * 65)
    print(f"Loading dataset from: {dataset_path}")
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file not found at {dataset_path}")
        return
        
    df = pd.read_csv(dataset_path, encoding="ISO-8859-1")
    
    original_shape = df.shape
    
    # Track rows removed sequentially
    # 1. Duplicates
    prev_rows = len(df)
    df = df.drop_duplicates()
    duplicates_removed = prev_rows - len(df)
    
    # 2. Missing Customer ID
    prev_rows = len(df)
    df = df.dropna(subset=["Customer ID"])
    missing_customers_removed = prev_rows - len(df)
    
    # 3. Missing Description
    prev_rows = len(df)
    df = df.dropna(subset=["Description"])
    missing_descriptions_removed = prev_rows - len(df)
    
    # 4. Cancelled Invoices (Invoice starts with "C")
    prev_rows = len(df)
    df = df[~df["Invoice"].astype(str).str.startswith("C")]
    cancelled_orders_removed = prev_rows - len(df)
    
    # 5. Invalid Quantity (Quantity <= 0)
    prev_rows = len(df)
    df = df[df["Quantity"] > 0]
    invalid_quantity_removed = prev_rows - len(df)
    
    # 6. Invalid Price (Price <= 0)
    prev_rows = len(df)
    df = df[df["Price"] > 0]
    invalid_price_removed = prev_rows - len(df)
    
    # 7. Convert InvoiceDate into datetime format
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    
    # 8. Create TotalAmount = Quantity x Price
    df["TotalAmount"] = df["Quantity"] * df["Price"]
    
    final_shape = df.shape
    
    # Save the cleaned dataset
    print(f"Saving cleaned dataset to: {output_path}")
    df.to_csv(output_path, index=False)
    
    # Get final file size on disk
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    
    print("\n--- Preprocessing Results ---")
    print(f"Original Shape: {original_shape}")
    print(f"Final Shape: {final_shape}")
    print(f"Duplicates Removed: {duplicates_removed:,}")
    print(f"Missing Customer IDs Removed: {missing_customers_removed:,}")
    print(f"Missing Descriptions Removed: {missing_descriptions_removed:,}")
    print(f"Cancelled Orders Removed: {cancelled_orders_removed:,}")
    print(f"Invalid Quantity Removed: {invalid_quantity_removed:,}")
    print(f"Invalid Price Removed: {invalid_price_removed:,}")
    print(f"Final Dataset Size: {final_shape[0]:,} rows ({file_size_mb:.2f} MB)")
    print("=" * 65)

if __name__ == "__main__":
    preprocess_dataset()
