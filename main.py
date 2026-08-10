
import os
import pandas as pd
import matplotlib.pyplot as plt


DATA_FILE = "data/sales_data.csv"
OUTPUT_FOLDER = "visualizations"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"Error: Dataset not found at '{DATA_FILE}'.")
    print("Make sure sales_data.csv is inside the data folder.")
    exit()


print("=" * 65)
print("E-COMMERCE SALES ANALYSIS & VISUALIZATION")
print("=" * 65)


print("\n--- DATASET OVERVIEW ---")

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn Data Types:")
print(df.dtypes)


print("\n--- DATA CLEANING ---")

missing_before = df.isnull().sum().sum()
duplicates_before = df.duplicated().sum()

print(f"Missing values before cleaning : {missing_before}")
print(f"Duplicate rows before cleaning: {duplicates_before}")

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

numeric_columns = df.select_dtypes(include="number").columns

for column in numeric_columns:
    if df[column].isnull().any():
        df[column] = df[column].fillna(df[column].median())

text_columns = df.select_dtypes(include="object").columns

for column in text_columns:
    if df[column].isnull().any():
        df[column] = df[column].fillna(df[column].mode()[0])

df = df.drop_duplicates()

df = df.dropna(subset=["Date"])

missing_after = df.isnull().sum().sum()

print(f"Missing values after cleaning  : {missing_after}")
print(f"Rows after cleaning            : {len(df)}")


print("\n--- SALES METRICS ---")

total_sales = df["Total_Sales"].sum()
average_sale = df["Total_Sales"].mean()
highest_sale = df["Total_Sales"].max()
lowest_sale = df["Total_Sales"].min()
total_quantity = df["Quantity"].sum()

print(f"Total Sales       : {total_sales:,.2f}")
print(f"Average Sale      : {average_sale:,.2f}")
print(f"Highest Sale      : {highest_sale:,.2f}")
print(f"Lowest Sale       : {lowest_sale:,.2f}")
print(f"Total Quantity    : {total_quantity}")


product_sales = (
    df.groupby("Product")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
)

best_product = product_sales.index[0]

print("\n--- SALES BY PRODUCT ---")
print(product_sales)

print(f"\nBest-selling product: {best_product}")


region_sales = (
    df.groupby("Region")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
)

best_region = region_sales.index[0]

print("\n--- SALES BY REGION ---")
print(region_sales)

print(f"\nBest-performing region: {best_region}")


monthly_sales = (
    df.groupby(df["Date"].dt.to_period("M"))["Total_Sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

print("\n--- MONTHLY SALES ---")
print(monthly_sales)


plt.figure(figsize=(9, 6))

product_sales.plot(kind="bar")

plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_FOLDER, "sales_by_product.png"),
    dpi=300
)

plt.close()


plt.figure(figsize=(9, 6))

region_sales.plot(kind="bar")

plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_FOLDER, "sales_by_region.png"),
    dpi=300
)

plt.close()


plt.figure(figsize=(9, 6))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_FOLDER, "monthly_sales_trend.png"),
    dpi=300
)

plt.close()


print("\n" + "=" * 65)
print("VISUALIZATIONS CREATED SUCCESSFULLY")
print("=" * 65)

print("\nFiles created:")

print("- visualizations/sales_by_product.png")
print("- visualizations/sales_by_region.png")
print("- visualizations/monthly_sales_trend.png")

print("\nAnalysis completed successfully.")
