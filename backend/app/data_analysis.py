import os
import pandas as pd

def analyze_dataset():
    # Resolve the absolute path to the dataset
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    dataset_path = os.path.join(base_dir, "datasets", "online_retail_II.csv")
    
    print("=" * 70)
    print("CUSTOMER SEGMENTATION SYSTEM - INITIAL DATASET INSPECTION & PROFILING")
    print("=" * 70)
    print(f"Loading dataset from: {dataset_path}")
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file not found at {dataset_path}")
        return

    # Load the dataset using pandas with latin1 (ISO-8859-1) encoding
    df = pd.read_csv(dataset_path, encoding="ISO-8859-1")
    
    # ------------------ STEP 1: INITIAL INSPECTION ------------------
    # 1. Dataset Shape
    print("\n[PART A: DATASET INSPECTION]")
    print("\n--- 1. Dataset Shape ---")
    print(f"Number of Rows: {df.shape[0]:,}")
    print(f"Number of Columns: {df.shape[1]}")
    
    # 2. First 10 Rows
    print("\n--- 2. First 10 Rows ---")
    print(df.head(10))
    
    # 3. Last 10 Rows
    print("\n--- 3. Last 10 Rows ---")
    print(df.tail(10))
    
    # 4. Complete Column List
    print("\n--- 4. Complete Column List ---")
    print(df.columns.tolist())
    
    # 5. Data Types
    print("\n--- 5. Column Data Types ---")
    print(df.dtypes)
    
    # 6. Missing Values Count Per Column
    print("\n--- 6. Missing Values Count Per Column ---")
    missing_counts = df.isnull().sum()
    for col, count in missing_counts.items():
        pct = (count / df.shape[0]) * 100
        print(f"  {col}: {count:,} ({pct:.2f}%)")
        
    # 7. Duplicate Rows Count
    print("\n--- 7. Duplicate Rows Count ---")
    duplicate_count = df.duplicated().sum()
    pct_dup = (duplicate_count / df.shape[0]) * 100
    print(f"Number of Duplicate Rows: {duplicate_count:,} ({pct_dup:.2f}%)")
    
    # ------------------ STEP 2: STATISTICAL PROFILING ------------------
    print("\n[PART B: STATISTICAL PROFILING]")
    
    # 1. Numerical Statistics
    print("\n--- 1. Numerical Statistics (Quantity & Price) ---")
    # Custom description to ensure count, mean, std, min, 25%, 50% (median), 75%, max are included
    numerical_cols = ["Quantity", "Price"]
    desc_stats = df[numerical_cols].describe(percentiles=[0.25, 0.50, 0.75])
    # Add median explicitly if 50% is not shown as median
    desc_stats.loc["median"] = df[numerical_cols].median()
    print(desc_stats)
    
    # 2. Categorical Statistics
    print("\n--- 2. Categorical Statistics ---")
    unique_countries = df["Country"].nunique()
    unique_customers = df["Customer ID"].nunique(dropna=True)
    unique_products = df["StockCode"].nunique()
    print(f"Number of Unique Countries: {unique_countries:,}")
    print(f"Number of Unique Customers (excluding NaN): {unique_customers:,}")
    print(f"Number of Unique Products (Stock Codes): {unique_products:,}")
    
    # 3. Sales Statistics
    print("\n--- 3. Sales Statistics ---")
    df["Revenue"] = df["Quantity"] * df["Price"]
    total_revenue = df["Revenue"].sum()
    
    # Calculate Order-level statistics
    order_totals = df.groupby("Invoice")["Revenue"].sum()
    avg_order_value = order_totals.mean()
    highest_order_value = order_totals.max()
    lowest_order_value = order_totals.min()
    
    print(f"Total Revenue: £{total_revenue:,.2f}")
    print(f"Average Order Value: £{avg_order_value:,.2f}")
    print(f"Highest Order Value: £{highest_order_value:,.2f}")
    print(f"Lowest Order Value: £{lowest_order_value:,.2f}")
    
    # 4. Date Statistics
    print("\n--- 4. Date Statistics ---")
    # Convert InvoiceDate into proper datetime format
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    earliest_date = df["InvoiceDate"].min()
    latest_date = df["InvoiceDate"].max()
    time_span = latest_date - earliest_date
    
    print(f"Earliest Invoice Date: {earliest_date}")
    print(f"Latest Invoice Date: {latest_date}")
    print(f"Total Time Span: {time_span}")
    
    # 5. Professional Summary
    print("\n" + "=" * 70)
    print("PROFESSIONAL STATISTICAL PROFILE SUMMARY")
    print("=" * 70)
    print(f"Dataset Overview: The retail dataset captures {df.shape[0]:,} records over a period of {time_span.days} days,")
    print(f"spanning from {earliest_date.strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')}.")
    
    print(f"\nCustomer & Product Metrics:")
    print(f"  - Active across {unique_countries} countries with {unique_customers:,} registered customers.")
    print(f"  - Serving a catalog of {unique_products:,} unique products (Stock Codes).")
    
    print(f"\nRevenue & Order Performance:")
    print(f"  - Cumulative raw revenue reaches £{total_revenue:,.2f}.")
    print(f"  - The average order value sits at £{avg_order_value:,.2f}, with transaction extremes ranging")
    print(f"    from a minimum of £{lowest_order_value:,.2f} to a maximum of £{highest_order_value:,.2f}.")
    
    print(f"\nData Quality Notes:")
    print(f"  - Quantity stats show a mean of {df['Quantity'].mean():.2f} units, min of {df['Quantity'].min():,}, and max of {df['Quantity'].max():,}.")
    print(f"  - Price stats show a mean of £{df['Price'].mean():.2f}, min of £{df['Price'].min():.2f}, and max of £{df['Price'].max():.2f}.")
    print(f"  - Missing value counts: 'Customer ID' has {missing_counts['Customer ID']:,} (NaN) entries.")
    print(f"  - Duplicate row counts: {duplicate_count:,} duplicate transactions represent {pct_dup:.2f}% of the data.")
    print(f"  - All negative/zero prices and quantities (cancellations/corrections) remain in the dataset")
    print(f"    as no cleaning, filtering, or modifications were performed.")
    print("=" * 70)

if __name__ == "__main__":
    analyze_dataset()
