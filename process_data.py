import pandas as pd

# Read the three CSV files
df1 = pd.read_csv("data/daily_sales_data_0.csv")
df2 = pd.read_csv("data/daily_sales_data_1.csv")
df3 = pd.read_csv("data/daily_sales_data_2.csv")

# Combine them into one DataFrame
df = pd.concat([df1, df2, df3], ignore_index=True)

# Keep only Pink Morsel products
df = df[df["product"] == "Pink Morsel"]

# Convert price from "$2.50" to 2.50
df["price"] = df["price"].replace("[$]", "", regex=True).astype(float)

# Create Sales column
df["Sales"] = df["quantity"] * df["price"]

# Keep only the required columns
output = df[["Sales", "date", "region"]]

# Save the output
output.to_csv("output.csv", index=False)

print("✅ output.csv created successfully!")