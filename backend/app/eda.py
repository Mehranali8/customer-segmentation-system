import os
import pandas as pd
import matplotlib
# Use the non-interactive Agg backend to prevent GUI windows from opening
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_eda_charts():
    # Resolve absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    dataset_path = os.path.join(base_dir, "datasets", "online_retail_II.csv")
    output_dir = os.path.join(base_dir, "screenshots")
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("CUSTOMER SEGMENTATION SYSTEM - EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 60)
    print(f"Loading dataset from: {dataset_path}")
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file not found at {dataset_path}")
        return
        
    df = pd.read_csv(dataset_path, encoding="ISO-8859-1")
    
    # Pre-calculate Revenue and proper InvoiceDate format for internal plotting use
    # (Leaving original dataframe structure intact without cleaning)
    df["Revenue"] = df["Quantity"] * df["Price"]
    df["InvoiceDate_dt"] = pd.to_datetime(df["InvoiceDate"])
    
    print("\nGenerating charts...")
    
    # ------------------ Chart 1: Missing Values Chart ------------------
    plt.figure(figsize=(10, 5))
    missing_pct = (df.isnull().sum() / len(df)) * 100
    missing_pct.plot(kind="bar", color="#aa3bff", edgecolor="black")
    plt.title("Missing Values Percentage per Column", fontsize=12, fontweight="bold")
    plt.ylabel("Missing Percentage (%)", fontsize=10)
    plt.xlabel("Columns", fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "missing_values.png")
    plt.savefig(chart1_path, dpi=150)
    plt.close()
    print(f"Saved: {chart1_path}")
    
    # ------------------ Chart 2: Top 10 Countries by Revenue ------------------
    plt.figure(figsize=(10, 5))
    top_countries = df.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10)
    top_countries.plot(kind="bar", color="#10b981", edgecolor="black")
    plt.title("Top 10 Countries by Revenue", fontsize=12, fontweight="bold")
    plt.ylabel("Revenue (£)", fontsize=10)
    plt.xlabel("Country", fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "top_countries.png")
    plt.savefig(chart2_path, dpi=150)
    plt.close()
    print(f"Saved: {chart2_path}")
    
    # ------------------ Chart 3: Top 10 Products Sold ------------------
    plt.figure(figsize=(12, 6))
    # Fill NA temporarily for description grouping without changing raw df
    temp_df = df.copy()
    temp_df["Description"] = temp_df["Description"].fillna("UNKNOWN PRODUCT")
    top_products = temp_df.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(10)
    top_products.plot(kind="barh", color="#6366f1", edgecolor="black").invert_yaxis()
    plt.title("Top 10 Products Sold by Quantity", fontsize=12, fontweight="bold")
    plt.xlabel("Quantity Sold", fontsize=10)
    plt.ylabel("Product Description", fontsize=10)
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "top_products.png")
    plt.savefig(chart3_path, dpi=150)
    plt.close()
    print(f"Saved: {chart3_path}")
    
    # ------------------ Chart 4: Quantity Distribution Histogram ------------------
    plt.figure(figsize=(10, 5))
    # Filter only visually for plotting purposes so histogram makes sense due to extreme outliers,
    # without cleaning or changing the source data
    visual_quantity = df[(df["Quantity"] > -50) & (df["Quantity"] < 100)]["Quantity"]
    plt.hist(visual_quantity, bins=50, color="#f43f5e", edgecolor="black", alpha=0.7)
    plt.title("Quantity Distribution (Visual Range: -50 to 100)", fontsize=12, fontweight="bold")
    plt.xlabel("Quantity", fontsize=10)
    plt.ylabel("Frequency", fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "quantity_distribution.png")
    plt.savefig(chart4_path, dpi=150)
    plt.close()
    print(f"Saved: {chart4_path}")
    
    # ------------------ Chart 5: Price Distribution Histogram ------------------
    plt.figure(figsize=(10, 5))
    # Filter only visually for plotting purposes (price <= 30) due to outlier prices,
    # without cleaning or changing the source data
    visual_price = df[(df["Price"] > 0) & (df["Price"] < 30)]["Price"]
    plt.hist(visual_price, bins=50, color="#fbbf24", edgecolor="black", alpha=0.7)
    plt.title("Price Distribution (Visual Range: £0 to £30)", fontsize=12, fontweight="bold")
    plt.xlabel("Unit Price (£)", fontsize=10)
    plt.ylabel("Frequency", fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    chart5_path = os.path.join(output_dir, "price_distribution.png")
    plt.savefig(chart5_path, dpi=150)
    plt.close()
    print(f"Saved: {chart5_path}")
    
    # ------------------ Chart 6: Monthly Sales Trend ------------------
    plt.figure(figsize=(12, 5))
    monthly_sales = df.groupby(df["InvoiceDate_dt"].dt.to_period("M"))["Revenue"].sum()
    monthly_sales.index = monthly_sales.index.astype(str)
    plt.plot(monthly_sales.index, monthly_sales.values, marker='o', color="#06b6d4", linewidth=2)
    plt.title("Monthly Sales Revenue Trend", fontsize=12, fontweight="bold")
    plt.ylabel("Total Revenue (£)", fontsize=10)
    plt.xlabel("Month", fontsize=10)
    plt.xticks(rotation=45)
    plt.grid(linestyle='--', alpha=0.5)
    plt.tight_layout()
    chart6_path = os.path.join(output_dir, "monthly_sales.png")
    plt.savefig(chart6_path, dpi=150)
    plt.close()
    print(f"Saved: {chart6_path}")
    
    # ------------------ Chart 7: Orders per Country ------------------
    plt.figure(figsize=(12, 5))
    orders_country = df.groupby("Country")["Invoice"].nunique().sort_values(ascending=False).head(10)
    orders_country.plot(kind="bar", color="#a855f7", edgecolor="black")
    plt.title("Top 10 Countries by Number of Unique Orders", fontsize=12, fontweight="bold")
    plt.ylabel("Number of Unique Orders", fontsize=10)
    plt.xlabel("Country", fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart7_path = os.path.join(output_dir, "orders_country.png")
    plt.savefig(chart7_path, dpi=150)
    plt.close()
    print(f"Saved: {chart7_path}")
    
    # ------------------ Chart 8: Customer Purchase Distribution ------------------
    plt.figure(figsize=(10, 5))
    # Frequency of purchases per customer
    customer_freq = df.dropna(subset=["Customer ID"]).groupby("Customer ID")["Invoice"].nunique()
    # Filter visually to focus on typical range (orders < 30) for plotting
    visual_freq = customer_freq[customer_freq < 30]
    plt.hist(visual_freq, bins=range(1, 30), color="#14b8a6", edgecolor="black", align='left', alpha=0.8)
    plt.title("Customer Purchase Frequency Distribution (Orders < 30)", fontsize=12, fontweight="bold")
    plt.xlabel("Number of Unique Orders", fontsize=10)
    plt.ylabel("Number of Customers", fontsize=10)
    plt.xticks(range(1, 30, 2))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    chart8_path = os.path.join(output_dir, "customer_distribution.png")
    plt.savefig(chart8_path, dpi=150)
    plt.close()
    print(f"Saved: {chart8_path}")
    
    print("\n" + "=" * 60)
    print("EDA ANALYSIS COMPLETED")
    print(f"All 8 charts successfully saved to the '{output_dir}/' directory.")
    print("=" * 60)

if __name__ == "__main__":
    generate_eda_charts()
